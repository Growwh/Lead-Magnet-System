"""
Tool definitions and executors for the Lead Magnet Agent.

Each tool wraps one existing Python script via subprocess.
Scripts are never modified - this layer only translates between
the Claude tool-call interface and each script's CLI interface.
"""
import base64
import ipaddress
import socket
import subprocess
import sys
from pathlib import Path

import requests


# -- Private IP filter (SSRF protection) --

def _is_private_url(url: str) -> bool:
    """Return True if the URL resolves to a private/loopback/link-local address."""
    try:
        host = url.split("//", 1)[1].split("/")[0].split(":")[0]
        ip = ipaddress.ip_address(socket.gethostbyname(host))
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except Exception:
        return True  # fail closed


_MEDIA_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


# -- Tool JSON schemas (sent to Claude API) --

TOOL_DEFINITIONS = [
    {
        "name": "fetch_content",
        "description": (
            "Fetch content from a URL (Notion, Google Doc, Google Drive, YouTube) or a local PDF file path. "
            "Saves the content to output/fetched_raw.txt and returns the file path. "
            "Use read_file to access the content after fetching."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "input_source": {
                    "type": "string",
                    "description": "URL or file path to fetch content from",
                },
            },
            "required": ["input_source"],
        },
    },
    {
        "name": "generate_infographic",
        "description": (
            "Generate a single infographic PNG using Google Gemini Imagen. "
            "Always use 1:1 aspect ratio for lead magnet infographics. "
            "Follow the brand style guide in .infographic/brand.md. "
            "No logo, no URL, no branding. Output goes into output/."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Full Gemini image generation prompt following the brand style guide",
                },
                "output_filename": {
                    "type": "string",
                    "description": "PNG filename (no path) inside output/, e.g. 'infographic-1-framework.png'",
                },
                "aspect_ratio": {
                    "type": "string",
                    "description": "Aspect ratio. Use 1:1 for all lead magnet infographics.",
                    "enum": ["1:1", "16:9", "9:16", "4:3", "3:4"],
                },
            },
            "required": ["prompt", "output_filename"],
        },
    },
    {
        "name": "generate_pdf",
        "description": (
            "Generate a branded PDF from a markdown file using Playwright/Chromium. "
            "subtitle is always passed as empty string."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Document title shown on the cover page"},
                "doc_type": {"type": "string", "description": "Document type: Playbook, Framework, Audit, Guide, Template, Checklist"},
                "content_path": {"type": "string", "description": "Path to the markdown source file"},
                "output_path": {"type": "string", "description": "Output PDF path"},
                "images_dir": {"type": "string", "description": "Directory containing infographic PNGs. Always pass 'output'."},
            },
            "required": ["title", "doc_type", "content_path", "output_path"],
        },
    },
    {
        "name": "generate_docx",
        "description": "Generate a branded Word document (.docx) from a markdown file. subtitle is always passed as empty string.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Document title"},
                "doc_type": {"type": "string", "description": "Document type: Playbook, Framework, Audit, Guide, Template, Checklist"},
                "content_path": {"type": "string", "description": "Path to the markdown source file"},
                "output_path": {"type": "string", "description": "Output DOCX path"},
                "images_dir": {"type": "string", "description": "Directory containing infographic PNGs. Always pass 'output'."},
            },
            "required": ["title", "doc_type", "content_path", "output_path"],
        },
    },
    {
        "name": "push_to_notion",
        "description": (
            "Create a new Notion page from a markdown file under the configured parent page. "
            "Uploads infographic images to Notion's file API and embeds them inline. "
            "Returns the URL of the created Notion page."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Notion page title"},
                "content_path": {"type": "string", "description": "Path to the markdown source file"},
                "icon_emoji": {"type": "string", "description": "Emoji for the Notion page icon"},
                "cover_url": {"type": "string", "description": "Unsplash cover image URL"},
                "images_dir": {"type": "string", "description": "Directory containing images. Pass 'output'."},
            },
            "required": ["title", "content_path"],
        },
    },
    {
        "name": "analyze_image",
        "description": (
            "Fetch an image from a URL or local file path and return it for visual analysis. "
            "Use on every [Image: URL_OR_PATH] found in fetched content BEFORE auditing. "
            "Also use after each generate_infographic call to quality-check the output."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Image URL (http/https) or file path"},
            },
            "required": ["source"],
        },
    },
    {
        "name": "read_file",
        "description": "Read a file from disk and return its text content.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path relative to the project root"},
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "write_file",
        "description": "Write text content to a file on disk. Creates parent directories if needed.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path relative to the project root"},
                "content": {"type": "string", "description": "Text content to write"},
            },
            "required": ["file_path", "content"],
        },
    },
]


# -- Executor --

class ToolExecutor:
    """Executes tool calls by invoking the corresponding Python script via subprocess."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.python = sys.executable

    def execute(self, name: str, tool_input: dict) -> str | list:
        method = getattr(self, f"_run_{name}", None)
        if method is None:
            return f"Error: unknown tool '{name}'"
        try:
            return method(**tool_input)
        except TypeError as e:
            return f"Error: tool '{name}' received unexpected arguments: {e}"
        except Exception as e:
            return f"Error executing tool '{name}': {e}"

    def _safe_path(self, file_path: str, restrict_to: Path | None = None) -> tuple[Path, str | None]:
        path = Path(file_path)
        if not path.is_absolute():
            path = self.project_root / file_path
        resolved = path.resolve()
        root = (restrict_to or self.project_root).resolve()
        if not resolved.is_relative_to(root):
            return resolved, f"Error: path outside permitted directory: {file_path}"
        return resolved, None

    def _run_fetch_content(self, input_source: str) -> str:
        output_path = self.project_root / "output" / "fetched_raw.txt"
        output_path.parent.mkdir(exist_ok=True)
        cmd = [self.python, str(self.project_root / "scripts" / "fetch_content.py"), "--input", input_source, "--output", str(output_path)]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.project_root), timeout=60)
        except subprocess.TimeoutExpired:
            return "Fetch timed out after 60 seconds."
        if result.returncode != 0:
            return f"Fetch failed (exit {result.returncode}):\n{result.stderr.strip()}"
        if not output_path.exists() or output_path.stat().st_size == 0:
            return "Fetch failed: output file is empty or was not created."
        size = output_path.stat().st_size
        return f"Fetched successfully ({size:,} bytes). Content saved to: output/fetched_raw.txt. Call read_file with 'output/fetched_raw.txt' to access it."

    def _run_generate_infographic(self, prompt: str, output_filename: str, aspect_ratio: str = "1:1") -> str:
        safe_name = Path(output_filename).name
        if aspect_ratio not in ("1:1", "16:9", "9:16", "4:3", "3:4"):
            aspect_ratio = "1:1"
        output_path = self.project_root / "output" / safe_name
        output_path.parent.mkdir(exist_ok=True)
        cmd = [self.python, str(self.project_root / "scripts" / "generate_infographic.py"), "--prompt", prompt, "--output", str(output_path), "--aspect-ratio", aspect_ratio]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.project_root), timeout=120)
        except subprocess.TimeoutExpired:
            return "Infographic generation timed out after 120 seconds."
        if result.returncode != 0:
            return f"Infographic generation failed (exit {result.returncode}):\n{result.stderr.strip()}"
        if not output_path.exists() or output_path.stat().st_size == 0:
            return f"Infographic generation failed: '{safe_name}' not created."
        size_kb = output_path.stat().st_size // 1024
        return f"Infographic generated: output/{safe_name} ({size_kb} KB)"

    def _run_doc_script(self, script_name: str, label: str, title: str, doc_type: str, content_path: str, output_path: str, images_dir: str | None = None) -> str:
        content, err = self._safe_path(content_path)
        if err:
            return err
        out, err = self._safe_path(output_path)
        if err:
            return err
        cmd = [self.python, str(self.project_root / "scripts" / script_name), "--title", title, "--type", doc_type, "--subtitle", "", "--content", str(content), "--output", str(out)]
        if images_dir:
            img_dir, err = self._safe_path(images_dir)
            if err:
                return err
            cmd += ["--images-dir", str(img_dir)]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.project_root), timeout=180)
        except subprocess.TimeoutExpired:
            return f"{label} generation timed out after 180 seconds."
        if result.returncode != 0:
            return f"{label} generation failed (exit {result.returncode}):\n{result.stderr.strip()}"
        if not out.exists() or out.stat().st_size == 0:
            return f"{label} generation failed: '{output_path}' not created."
        size_kb = out.stat().st_size // 1024
        return f"{label} generated: {output_path} ({size_kb} KB)"

    def _run_generate_pdf(self, title: str, doc_type: str, content_path: str, output_path: str, images_dir: str | None = None) -> str:
        return self._run_doc_script("generate_pdf_playwright.py", "PDF", title, doc_type, content_path, output_path, images_dir)

    def _run_generate_docx(self, title: str, doc_type: str, content_path: str, output_path: str, images_dir: str | None = None) -> str:
        return self._run_doc_script("generate_doc.py", "DOCX", title, doc_type, content_path, output_path, images_dir)

    def _run_push_to_notion(self, title: str, content_path: str, icon_emoji: str = "\U0001f4d8", cover_url: str | None = None, images_dir: str | None = None) -> str:
        content, err = self._safe_path(content_path)
        if err:
            return err
        cmd = [self.python, str(self.project_root / "scripts" / "push_to_notion.py"), "--title", title, "--content", str(content), "--icon-emoji", icon_emoji]
        if cover_url:
            if _is_private_url(cover_url):
                return "Error: cover_url resolves to a private/internal address - blocked."
            cmd += ["--cover-url", cover_url]
        if images_dir:
            img_dir, err = self._safe_path(images_dir)
            if err:
                return err
            cmd += ["--images-dir", str(img_dir)]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.project_root), timeout=120)
        except subprocess.TimeoutExpired:
            return "Notion push timed out after 120 seconds."
        if result.returncode != 0:
            return f"Notion push failed (exit {result.returncode}):\n{result.stderr.strip()}"
        notion_url = result.stdout.strip()
        return f"Pushed to Notion: {notion_url}"

    def _run_analyze_image(self, source: str) -> list:
        _MAX_IMAGE_BYTES = 5 * 1024 * 1024
        raw: bytes = b""
        media_type = "image/jpeg"
        try:
            if source.startswith("http://") or source.startswith("https://"):
                if _is_private_url(source):
                    return [{"type": "text", "text": f"Blocked: private/internal URL not permitted: {source}"}]
                resp = requests.get(source, timeout=15, headers={"User-Agent": "Mozilla/5.0"}, stream=True)
                resp.raise_for_status()
                chunks = []
                total = 0
                for chunk in resp.iter_content(chunk_size=65_536):
                    total += len(chunk)
                    if total > _MAX_IMAGE_BYTES:
                        return [{"type": "text", "text": f"Image too large (>5 MB), skipped: {source}"}]
                    chunks.append(chunk)
                raw = b"".join(chunks)
                ct = resp.headers.get("content-type", "").split(";")[0].strip()
                if ct in ("image/jpeg", "image/png", "image/gif", "image/webp"):
                    media_type = ct
                else:
                    ext = "." + source.split("?")[0].rsplit(".", 1)[-1].lower()
                    media_type = _MEDIA_TYPES.get(ext, "image/jpeg")
            else:
                path, err = self._safe_path(source)
                if err:
                    return [{"type": "text", "text": err}]
                if not path.exists():
                    return [{"type": "text", "text": f"Image not found: {path}"}]
                raw = path.read_bytes()
                if len(raw) > _MAX_IMAGE_BYTES:
                    return [{"type": "text", "text": f"Image too large (>5 MB), skipped: {source}"}]
                media_type = _MEDIA_TYPES.get(path.suffix.lower(), "image/jpeg")
        except Exception as e:
            return [{"type": "text", "text": f"Failed to fetch image from '{source}': {e}"}]
        if not raw:
            return [{"type": "text", "text": f"Empty image data from: {source}"}]
        b64 = base64.standard_b64encode(raw).decode("utf-8")
        return [
            {"type": "text", "text": f"Image from: {source}"},
            {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": b64}},
        ]

    def _run_read_file(self, file_path: str) -> str:
        path, err = self._safe_path(file_path)
        if err:
            return err
        if not path.exists():
            return f"Error: file not found: {path}"
        return path.read_text(encoding="utf-8")

    def _run_write_file(self, file_path: str, content: str) -> str:
        path, err = self._safe_path(file_path)
        if err:
            return err
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        size_kb = path.stat().st_size // 1024
        return f"Written: {path} ({size_kb} KB)"
