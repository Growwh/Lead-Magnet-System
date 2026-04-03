# Scripts Folder

This folder contains the Python utilities that power the lead magnet pipeline.

## Scripts

### `fetch_content.py`
Universal content fetcher. Takes any URL or file path and returns clean text.

**Supports:** Notion pages, Google Docs, Google Drive, PDFs, generic URLs, pasted text.

**Usage:**
```bash
python scripts/fetch_content.py --input "URL_OR_PATH" --output "output/fetched_raw.txt"
```

### `validate.py`
Deterministic validation script. Checks for banned words, em dashes, structure rules, and formatting issues. Runs in milliseconds with 100% accuracy (no LLM needed).

**Usage:**
```bash
python scripts/validate.py --content "output/playbook.md" --config "config.yaml"
```

### `generate_infographic.py`
AI image generation via Gemini API. Generates branded infographics following the style guide.

**Requires:** Paid Gemini API key.

### `screenshot_to_pdf.py`
Renders branded HTML via Playwright (Chromium), takes per-slide screenshots, and combines them into a PDF.

**Usage:**
```bash
python scripts/screenshot_to_pdf.py --html "output/playbook.html" --output "output/playbook.pdf"
```

### `push_to_notion.py`
Creates a Notion page from markdown content with embedded images.

**Requires:** Notion API key and parent page ID in `.env`.

## Adding a New Script

1. Create the Python file in this folder
2. Accept CLI arguments via `argparse`
3. Read config from `config.yaml` or `.env` as needed
4. Output to the `output/` directory
5. Add a tool definition in `agent/tools.py` if it should be callable by the agent
