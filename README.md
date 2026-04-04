<p align="center">
  <img src="https://img.shields.io/badge/version-v1.5-blue?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Claude-Anthropic-orange?style=flat-square" alt="Claude">
  <img src="https://img.shields.io/badge/Playwright-Chromium-2EAD33?style=flat-square&logo=playwright&logoColor=white" alt="Playwright">
</p>

<h1 align="center">Lead Magnet System In A Box</h1>

<p align="center">
  <strong>AI-powered content repurposing system.</strong><br>
  Feed it any URL, PDF, YouTube video, LinkedIn post, or raw text.<br>
  Get branded playbooks, infographics, scripts, posts, guides, and checklists.<br><br>
  <em>Your voice. Your brand. Your design system.</em>
</p>

<p align="center">
  <code>Paste a link &rarr; Get your repurposed content</code>
</p>

---

> **v1.5** ships the full working pipeline. **v2** will bring batch processing, visual slide-deck templates, and expanded platform support.

<details>
<summary><strong>v1.5 Changelog</strong> (click to expand)</summary>

### What's New in v1.5

**Core Pipeline (now fully implemented):**
- `agent/agent.py` - Full async agent using the Anthropic SDK with 30-turn agentic loop, streaming output, and parallel tool execution
- `agent/config.py` - Environment loader with graceful degradation (no required API keys when using Claude Code)
- `agent/system_prompt.py` - Dynamic prompt builder that loads your skill file + brand context + voice context at runtime
- `agent/tools.py` - 8 tool definitions with SSRF protection, path safety, and subprocess-based script execution

**Scripts (all new):**
- `scripts/fetch_content.py` - Universal content fetcher: Notion, Google Docs/Drive, YouTube transcripts, PDFs (text + images), any URL with Playwright fallback for JS-rendered pages, 15-minute caching
- `scripts/generate_pdf_playwright.py` - Branded A4 PDF generation via Playwright/Chromium with Google Fonts, callout styling, CTA sections, and PyMuPDF footer post-processing
- `scripts/generate_doc.py` - Branded Word document generation with cover page, styled callout boxes, code blocks, tables, and inline markdown parsing
- `scripts/push_to_notion.py` - Full Notion publisher with parallel image uploads via Files API, markdown-to-blocks conversion, rate limiting, and cover image support
- `scripts/generate_infographic.py` - AI infographic generation via Google Gemini (Flash Image with Imagen 4 fallback)

**Quality of Life:**
- YouTube transcript integration via `youtube-transcript-api` (no API key needed)
- Graceful API key handling: only warns on missing optional keys, never crashes
- `ANTHROPIC_API_KEY` removed from `.env.example` (not needed when running via Claude Code)
- Updated `requirements.txt` with `youtube-transcript-api`
- Improved `agent_runner.py` with `--project-root` flag and proper exit codes

</details>

---

## Before You Start

The system works out of the box, but it works **significantly better** with two things set up:

### 1. Brand Bible (Visual Design System)
**File:** `brand/brand-context.md`

This is your complete visual identity: colors, fonts, shadows, components, spacing, do's and don'ts. When this file is filled out, every output (PDFs, HTML slide decks, infographics) automatically matches your exact visual brand. Without it, the system uses generic defaults.

### 2. Voice Context (How You Write)
**File:** `brand/voice-context.md`

This is your personality on paper: how you talk, your speech patterns, banned words, writing rules, voice examples, content structure. When this file is filled out, every piece of content sounds like **you** actually wrote it. Without it, the system writes in a generic professional tone.

> Both files are optional. The system runs without them. But the difference in output quality is night and day.

---

## Table of Contents

- [Before You Start](#before-you-start)
- [What It Generates](#-what-it-generates)
- [How It Works](#-how-it-works)
- [Architecture](#-architecture)
- [Folder Structure](#-folder-structure)
- [Setup](#-setup)
- [API Keys](#-api-keys)
- [Pipeline Deep Dive](#-pipeline-deep-dive)
- [Infographic Generation](#-infographic-generation)
- [Improvements Over Traditional Systems](#-improvements-over-traditional-systems)
- [License](#-license)

---

## What It Generates

| Output | Description |
|:-------|:-----------|
| **Playbooks** | Strategic, multi-slide visual playbooks (PDF + HTML). One concept per slide. |
| **Infographics** | One-page branded visual data cards. *Requires Gemini API key (paid tier).* |
| **Scripts** | Email scripts, DM templates, outreach sequences. |
| **Social Posts** | LinkedIn posts, X threads, repurposed from long-form content. |
| **Guides** | Sequential, step-by-step how-to documents. |
| **Checklists** | Action-dense, checkbox-heavy quick-reference sheets. |

> All output is branded with **your** colors, fonts, voice, and design system. Not generic templates. Your brand, every time.

---

## How It Works

```
1. Fetch      Paste any URL, PDF, or text. System auto-detects the platform.
2. Identify   Detects the core idea and best output format.
3. Write      Claude writes in your voice using brand + voice context.
4. Critique   Claude re-reads as an editor. Flags weak sections.
5. Revise     Fixes only what was flagged. Surgical improvements.
6. Validate   Python script checks banned words, structure, formatting.
7. Render     Branded HTML slide deck > Playwright screenshots > PDF.
8. Publish    Push to Notion (optional).
```

---

## Architecture

```
Input (URL / PDF / YouTube / LinkedIn / text)
  |
  v
+------------------+
|      FETCH       |  Auto-detect platform, extract content
+------------------+
  |
  v
+------------------+
|     IDENTIFY     |  Content type + best output format
+------------------+
  |
  v
+------------------+
|      WRITE       |  Claude + brand context + voice rules
+------------------+
  |
  v
+------------------+
|    CRITIQUE      |  Claude as editor, flags weak spots
+------------------+
  |
  v
+------------------+
|     REVISE       |  Fix only what was flagged
+------------------+
  |
  v
+------------------+
|  INFOGRAPHICS    |  AI visuals via Gemini (optional)
+------------------+
  |
  v
+------------------+
|    VALIDATE      |  Python: banned words, structure, formatting
+------------------+
  |
  v
+------------------+
|     RENDER       |  HTML > Playwright > screenshots > PDF
+------------------+
  |
  v
+------------------+
|    PUBLISH       |  Notion (optional)
+------------------+
```

---

## Folder Structure

```
lead-magnet-system-in-a-box/
|
|-- config.yaml                  # Single source of truth for ALL settings
|-- requirements.txt             # Python dependencies
|-- agent_runner.py              # CLI entry point
|-- .env.example                 # API key template (never commit .env)
|-- LICENSE                      # MIT
|
|-- brand/
|   |-- brand-context.md         # Your visual design system
|   |-- voice-context.md         # How you write and speak
|   +-- GUIDE.md                 # How this folder works
|
|-- .infographic/
|   |-- brand.md                 # AI infographic style rules
|   +-- GUIDE.md
|
|-- scripts/
|   |-- fetch_content.py         # Universal content fetcher (Notion, Google, YouTube, PDF, URL)
|   |-- generate_pdf_playwright.py  # Branded A4 PDF via Playwright/Chromium
|   |-- generate_doc.py          # Branded Word document (.docx)
|   |-- generate_infographic.py  # AI infographic generation (Gemini)
|   |-- push_to_notion.py        # Publish to Notion with image uploads
|   |-- screenshot_to_pdf.py     # HTML slide deck > screenshots > PDF
|   |-- validate.py              # Deterministic content validation
|   +-- GUIDE.md                 # All scripts documented
|
|-- agent/
|   |-- __init__.py              # Public API: LeadMagnetAgent, run_sync
|   |-- agent.py                 # Async agentic loop (Anthropic SDK)
|   |-- config.py                # Environment loader + validation
|   |-- system_prompt.py         # Dynamic prompt builder
|   |-- tools.py                 # 8 tool definitions + executors
|   +-- GUIDE.md                 # Standalone agent docs
|
|-- templates/
|   +-- GUIDE.md                 # HTML template docs
|
|-- assets/
|   +-- GUIDE.md                 # Logo + brand assets
|
|-- .claude/
|   |-- commands/                # Autonomous pipeline (no approval gates)
|   |   |-- repurpose-lead-magnet.md
|   |   +-- GUIDE.md
|   +-- skills/                  # Interactive pipeline (user checkpoints)
|       |-- repurpose-lead-magnet.md
|       +-- GUIDE.md
|
+-- output/                      # Generated files land here
    +-- .gitkeep
```

> Every folder has a `GUIDE.md` explaining what it does, how to customize it, and how it fits into the pipeline.

---

## Setup

### 1. Clone

```bash
git clone https://github.com/z1fex/Lead-Magnet-System-In-A-Box.git
cd Lead-Magnet-System-In-A-Box
```

### 2. Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Dependencies

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 4. Brand Customization

| Step | File | What to do |
|:-----|:-----|:-----------|
| 1 | `config.yaml` | Brand name, colors, fonts, CTA link |
| 2 | `brand/brand-context.md` | Your full visual design system |
| 3 | `brand/voice-context.md` | How you talk, write, and think |
| 4 | `assets/` | Drop your logo here (optional) |
| 5 | `.infographic/brand.md` | AI image generation style (optional) |

### 5. Run

**Interactive (Claude Code):**
```
/repurpose-lead-magnet
```

**Standalone agent (CLI):**
```bash
python agent_runner.py "https://example.com/article"
```

**Autonomous with JSON output:**
```bash
python agent_runner.py --json "https://example.com/article"
```

---

## API Keys

| Key | Required | Purpose |
|:----|:---------|:--------|
| `GEMINI_API_KEY` | Optional | AI infographic generation (paid tier) |
| `NOTION_API_KEY` | Optional | Publishing to Notion |
| `NOTION_PARENT_PAGE_ID` | Optional | Target Notion page for publishing |

> **No API keys are required when running via Claude Code** (`/repurpose-lead-magnet`). Keys are only needed for the standalone agent mode (`python agent_runner.py`), and even then only `ANTHROPIC_API_KEY` is needed. Gemini and Notion keys unlock optional features.
>
> **About Gemini:** The free API key does **not** support image generation (0 image quota). You need a paid tier. Without it, infographics are skipped gracefully. Everything else works fine.

---

## Pipeline Deep Dive

### Fetching

The universal fetcher auto-detects the source from the URL:

| Platform | How it fetches |
|:---------|:--------------|
| **LinkedIn** | Scrapes public posts. Falls back to manual paste or attached PDF/screenshots. |
| **YouTube** | Pulls transcript via YouTube Transcript API. |
| **Notion** | Unofficial API (public pages) or official API (connected pages). |
| **Google Docs/Drive** | Export URL trick. |
| **PDF** | pdfplumber (text) + PyMuPDF (images). |
| **Any URL** | Static fetch + Playwright fallback for JS-rendered pages. |

**Multi-input:** You can combine a URL (for platform context) + a file attachment (for actual content). Useful when scraping fails or when repurposing a downloaded playbook.

### Writing: The Critique Loop

Most systems write in one pass. This system uses three:

| Pass | Role | What happens |
|:-----|:-----|:-------------|
| **Write** | Writer | Full draft using brand context + voice rules |
| **Critique** | Editor | Re-reads with a different prompt. Flags weak sections. |
| **Revise** | Rewriter | Fixes only what was flagged. Surgical, not wholesale. |

**Result:** The quality floor goes up. Instead of outputs ranging 6/10 to 9/10, they range 7.5/10 to 9/10. More consistent.

### Validation

`validate.py` handles every deterministic check in Python. No LLM tokens burned on regex work.

| Check | Method |
|:------|:-------|
| Em dashes | String scan (banned everywhere) |
| Banned words | List match from `config.yaml` |
| Structure | First line is callout, no H1 inside content, CTA exists |
| Checklist | `- [ ]` items present |
| FAQ section | Section detected |
| Image refs | Files exist in `output/` |

### Rendering

The HTML > Screenshot > PDF approach produces pixel-perfect output:

1. Content is injected into a branded HTML template (slide deck, 1080x1080px)
2. Playwright renders each slide at **2x resolution** for crisp output
3. Each slide is screenshotted individually
4. Screenshots are stitched into a PDF via Pillow

---

## Infographic Generation

AI-generated branded infographics using Google Gemini image models.

**How it works:**
1. System identifies 2-3 concepts best suited for visual representation
2. Constructs prompts following your `.infographic/brand.md` style guide
3. Gemini generates images, each is quality-checked
4. Passing images are embedded into the output. Failed images get one retry; if still broken, they're dropped

**Requirements:**
- `GEMINI_API_KEY` in `.env` (paid tier)
- `pipeline.infographic_count` set to `2` or `3` in `config.yaml`

**Without a key:** Everything else works. Playbooks, scripts, posts, guides, checklists, PDFs, Notion. Infographics are the only feature behind the paid Gemini key.

---

## Improvements Over Traditional Systems

| | Traditional | This System |
|:--|:-----------|:------------|
| **Content types** | Playbooks only | Playbooks, infographics, scripts, posts, guides, checklists |
| **Writing** | Single pass, inconsistent | Write > Critique > Revise loop |
| **Validation** | LLM scans for issues (slow, $$$) | Python regex (instant, free, 100% accurate) |
| **Brand config** | Hardcoded across 15+ files | Single `config.yaml` |
| **Output format** | A4 text document | Visual slide deck (1080x1080, one idea per slide) |
| **PDF quality** | Markdown-to-PDF | HTML > Playwright screenshot > PDF (pixel-perfect) |
| **Voice** | Generic professional tone | Your actual voice, personality, speech patterns |
| **Infographics** | Fragile, one style | Matches your brand system (Gemini API) |
| **Input sources** | URLs only | URLs, PDFs, YouTube, LinkedIn, images, text |

---

## Contributing

Found a bug? Want to add a feature? PRs are welcome.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push and open a PR

---

## License

MIT. Use it however you want.

---

<p align="center">
  <strong>Built by <a href="https://github.com/z1fex">z1fex</a></strong><br>
  <sub>If this helped you, drop a star.</sub>
</p>
