# Lead Magnet System In A Box (v1)

An AI-powered content repurposing system. Feed it anything (a URL, a PDF, a YouTube video, a LinkedIn post, raw text) and it transforms that into branded, visually polished output: playbooks, infographics, scripts, social posts, guides, checklists.

Paste a link. Get a playbook. Your voice, your brand, your design system.

> v1 ships the core pipeline. v2 will bring batch processing, more output templates, and expanded platform support.

## What It Generates

| Output Type | Description |
|---|---|
| **Playbooks** | Strategic, multi-slide visual playbooks (PDF + HTML) |
| **Infographics** | One-page branded visual data cards (requires Gemini API key) |
| **Scripts** | Email scripts, DM templates, outreach sequences |
| **Social Posts** | LinkedIn posts, X threads, repurposed from long-form content |
| **Guides** | Sequential, step-by-step how-to documents |
| **Checklists** | Action-dense, checkbox-heavy quick-reference sheets |

All output is branded with your colors, fonts, voice, and design system. Not generic templates. Your brand, every time.

## What It Does

1. **Fetches content** from any source (LinkedIn posts, YouTube videos, Notion pages, PDFs, blog URLs, or pasted text)
2. **Auto-detects the platform** (LinkedIn, YouTube, Notion, Google Docs, any URL) and extracts content the right way
3. **Identifies the core idea** and the best output format (Playbook, Guide, Infographic, Script, etc.)
4. **Rewrites everything from scratch** in your brand voice using a Write > Critique > Revise loop
5. **Generates AI infographics** matching your brand's visual style (requires Gemini API key, paid tier)
6. **Validates deterministically** using a Python script (banned words, structure checks, formatting rules)
7. **Renders branded visual output** (HTML slide deck > Playwright screenshots > PDF)
8. **Optionally pushes to Notion** with embedded images

## Architecture

```
Input (URL / PDF / YouTube / LinkedIn / text)
    |
    v
[Fetch] Auto-detect platform, extract content
    |
    v
[Identify] Detect content type + best output format
    |
    v
[Write] Claude writes in your voice (brand + voice context)
    |
    v
[Critique] Claude re-reads as editor, flags weak sections
    |
    v
[Revise] Claude fixes only what was flagged
    |
    v
[Infographics] AI generates branded visuals (Gemini API, optional)
    |
    v
[Validate] Python script checks banned words, structure, formatting
    |
    v
[Render] Content > branded HTML > Playwright screenshots > PDF
    |
    v
[Publish] Push to Notion (optional)
```

## Infographic Generation

The system generates branded AI infographics using Google's Gemini image models. Each infographic follows your brand's visual style guide (colors, typography, layout rules).

**Requirements:**
- A Google Gemini API key on a **paid tier** (free tier does not support image generation via API)
- Set `GEMINI_API_KEY` in your `.env` file
- Set `pipeline.infographic_count` to 2 or 3 in `config.yaml`

**Without a Gemini key:** Everything else works perfectly. Playbooks, scripts, posts, guides, checklists, PDFs, Notion push. Infographics are the only feature that requires the paid Gemini key. The system skips infographic generation gracefully when no key is configured.

**How it works:**
1. After writing the content, the system identifies 2-3 concepts best suited for visual representation
2. It constructs prompts following your brand's infographic style guide (`.infographic/brand.md`)
3. Gemini generates the images, which are quality-checked and embedded into the output
4. Failed images get one retry; if still broken, they're dropped (2 clean > 3 broken)

## Folder Structure

```
.
├── config.yaml              # Single source of truth for all settings
├── requirements.txt         # Python dependencies
├── agent_runner.py          # CLI entry point for standalone agent
├── .env.example             # Template for API keys
├── LICENSE                  # MIT License
├── brand/
│   ├── brand-context.md     # Full visual design system
│   ├── voice-context.md     # How you write and speak
│   └── GUIDE.md             # How this folder works
├── .infographic/
│   ├── brand.md             # AI infographic style rules
│   └── GUIDE.md
├── templates/
│   └── GUIDE.md             # HTML template documentation
├── scripts/
│   ├── screenshot_to_pdf.py # HTML > screenshots > PDF renderer
│   ├── validate.py          # Deterministic content validation
│   └── GUIDE.md             # All scripts documented
├── agent/
│   ├── __init__.py
│   └── GUIDE.md             # Standalone agent documentation
├── assets/
│   └── GUIDE.md             # Logo and brand assets
├── .claude/
│   ├── commands/            # Claude Code slash commands (autonomous)
│   └── skills/              # Claude Code interactive skills
├── output/                  # Generated files land here
└── README.md
```

## Key Improvements Over Traditional Systems

| Feature | Traditional | This System |
|---------|------------|-------------|
| Content types | Playbooks only | Playbooks, infographics, scripts, posts, guides, checklists |
| Writing | Single pass, inconsistent quality | Write > Critique > Revise loop |
| Validation | LLM scans for issues (slow, expensive, unreliable) | Python script with regex (instant, free, 100% accurate) |
| Brand config | Hardcoded across 15+ files | Single `config.yaml` |
| Output format | A4 document with text walls | Visual slide deck (1080x1080, one idea per slide) |
| PDF quality | Markdown-to-PDF (basic) | HTML > Playwright screenshot > PDF (pixel-perfect) |
| Voice | Generic professional tone | Your actual voice, personality, and speech patterns |
| Infographics | Fragile, one style fits all | Matches your brand design system (requires Gemini API) |
| Input sources | URLs only | URLs, PDFs, YouTube transcripts, LinkedIn posts, images, pasted text |

## Setup

### 1. Clone and Configure

```bash
git clone <repo-url>
cd lead-magnet-system-in-a-box
cp .env.example .env
# Edit .env with your API keys
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 3. Customize Your Brand

1. Edit `config.yaml` with your brand name, colors, fonts, CTA link
2. Replace `brand/brand-context.md` with your design system
3. Replace `brand/voice-context.md` with your voice guide
4. (Optional) Add your logo to `assets/`
5. (Optional) Set up `.infographic/brand.md` for AI image generation

### 4. Run

**Interactive (Claude Code):**
```
/repurpose-lead-magnet
```

**Standalone agent:**
```bash
python agent_runner.py "https://example.com/article"
```

## Required API Keys

| Key | Required | Purpose |
|-----|----------|---------|
| `ANTHROPIC_API_KEY` | Yes | Claude API for writing pipeline |
| `GEMINI_API_KEY` | Optional | AI infographic generation (**paid tier required**, free tier has 0 image quota) |
| `NOTION_API_KEY` | Optional | Publishing to Notion |
| `NOTION_PARENT_PAGE_ID` | Optional | Target Notion page |

**Note on Gemini:** The free Gemini API key does NOT support image generation. You need a paid tier. Without it, infographics are simply skipped. Everything else (playbooks, scripts, posts, PDFs, Notion) works without it.

## How the Pipeline Works

### Fetching
The universal fetcher auto-detects the source:
- **LinkedIn** - Scrapes public posts; falls back to manual paste or attached PDF/screenshots
- **YouTube** - Pulls transcript via YouTube Transcript API
- **Notion** - Fetches via unofficial API (public pages) or official API (connected pages)
- **Google Docs/Drive** - Export URL trick
- **PDF** - Text extraction via pdfplumber + image extraction via PyMuPDF
- **Any URL** - Static fetch + Playwright fallback for JS-rendered pages

### Multi-Input Support
You can combine inputs: a LinkedIn URL (for platform context) + a PDF attachment (for the actual content). The URL tells the system where it came from. The file gives it the content. Useful when LinkedIn scraping fails or when you want to repurpose a downloaded playbook.

### Writing
The Write > Critique > Revise loop:
1. **Write** - Claude produces a full draft using your brand context + voice rules
2. **Critique** - Claude re-reads as an editor with a different prompt, flags weak sections
3. **Revise** - Claude fixes only what was flagged, surgically improving weak spots

### Infographic Generation (Optional)
If a Gemini API key (paid tier) is configured:
1. System identifies 2-3 concepts best suited for visuals
2. Constructs prompts following `.infographic/brand.md` style guide
3. Generates images via Gemini, quality-checks each one
4. Embeds passing images into the output

### Validation
`validate.py` handles all deterministic checks:
- Em dashes (banned)
- Banned words list (from config.yaml)
- Structure rules (H1/H2, CTA format, checklist presence)
- Image reference validation

### Rendering
The HTML > Screenshot > PDF approach:
1. Content is injected into a branded HTML template (slide deck format, 1080x1080px)
2. Playwright renders each slide at 2x resolution
3. Each slide is screenshotted individually
4. Screenshots are combined into a single PDF via Pillow

## License

MIT
