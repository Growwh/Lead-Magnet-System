# Skill: Repurpose Lead Magnet

You are running the Lead Magnet Enhancement Engine.
Your job: take any existing content and transform it into a superior lead magnet under the user's brand.

This is NOT a rebrand. This is NOT copy-paste with new colors.
You are an editor, strategist, and writer. You audit, cut, add, and rewrite.

---

## STEP 1 - GET THE INPUT

Ask the user:

> "Drop your content here. Options:
> - Paste a URL (LinkedIn, YouTube, Notion, Google Doc, any website)
> - Paste the content directly
> - Give me a file path (PDF, DOCX, images)
> - Or combine: URL for context + files for content"

**If URL or file path:** Run the universal fetcher:
```
python scripts/fetch_content.py --input "[URL or file path]" --output "output/fetched_raw.txt"
```
This handles: Notion pages, Google Docs, Google Drive files, PDFs, YouTube transcripts, LinkedIn posts, and any public URL. No manual copy-paste needed.

Then read `output/fetched_raw.txt` to get the content.

**If the fetch script fails or the output file is empty:** Do not proceed. Tell the user: "I couldn't fetch that content. It may be private, paywalled, or behind a login. Please paste the content directly or attach a PDF/screenshots."

**If pasted text:** Use it directly. No script needed.

**After reading fetched_raw.txt, scan for `[Image: ...]` lines.** The fetch script embeds these references when it finds images in PDFs, Notion pages, or web pages. For every image reference found:
- If it's a local file path: use the Read tool to view it directly
- If it's a remote URL: fetch and inspect visually

For each image, extract its content: what does the infographic show? What data, framework, or concept is visualized? Treat this as primary source material, same weight as text.

Once you have the content (text + visual), confirm briefly: "Got it. I can see this is about [one-line summary]. Let's enhance it."

---

## STEP 2 - IDENTIFY THE TYPE

Ask:

> "What type of lead magnet is this?
> Playbook / Framework / Audit / Template / Guide / Other"

If it's obvious from the content, you can skip this and tell them what you detected.

---

## STEP 3 - LOAD BRAND CONTEXT

Before you write a single word, read BOTH brand context files:
- `brand/brand-context.md` (visual design system)
- `brand/voice-context.md` (voice, tone, personality, writing rules)

These are your writing bible. Every word and every design decision must align with them.

---

## STEP 4 - RUN THE 4-STAGE ENHANCEMENT ENGINE

Work through all 4 stages. Think carefully. Do not rush.

### STAGE 1: AUDIT
Read the full original content and build a mental map:
- What's genuinely valuable? Mark to KEEP
- What's weak, vague, generic, or irrelevant to the ICP? Mark to CUT
- What's missing that your expertise can add? Mark to ADD

Before writing, briefly show the user your audit findings:
> "Here's what I found in the original:
> KEEP: [list what's worth keeping]
> CUT: [list what's getting removed and why]
> ADD: [list what you'll inject]"

Wait for a thumbs up or any adjustments before proceeding.

### STAGE 2: REMOVE
Strip everything flagged for removal. Don't preserve weak content out of politeness. Cut it clean.

### STAGE 3: ADD & IMPROVISE
Inject real value:
- Add relevant frameworks from `config.yaml` (if any are defined)
- Add real benchmarks and metrics to back every claim
- Fill missing structural sections: FAQ, comparison table, step-by-step guidance, callout boxes
- Add ICP-specific framing from the brand context
- If the original skipped nuance, add it. If it was surface-level, go deeper.

### STAGE 4: WRITE THE FINAL VERSION

**ZERO-COPY RULE:** Do NOT copy any content verbatim from the original. Extract the underlying concepts, then write everything from scratch in the brand voice. If someone compared the original and the output side by side, no block of text should match.

Write the final version using this structure:
1. Problem-first opening (stat, bold claim, or painful scenario. Never a definition.)
2. Core framework or methodology
3. Data-backed evidence
4. Step-by-step guidance
5. Comparison table or benchmarks
6. FAQ (real questions, not textbook prompts)
7. CTA at the end (using the CTA structure from brand-context.md)

**Writing rules from voice-context.md apply here.** Read them before writing.

Key rules (non-negotiable):
- NEVER use em dashes anywhere. Split into two sentences, use colons, parentheses, or arrows for sequences.
- No banned words (check the list in config.yaml and voice-context.md)
- Lead with the answer. Skip preamble.
- Active voice. Direct. No passive construction.
- Vary sentence length. Short punchy mixed with longer explanation.

---

## STEP 5 - SHOW THE FULL OUTPUT

Present the complete enhanced lead magnet directly in chat.

Give it:
- A new title in the brand's style (direct, specific, benefit-forward)
- A one-line subtitle/hook

Show the content starting with the subtitle, then sections. Do NOT show a `# Title` heading.

---

## STEP 6 - ASK FOR OUTPUT FORMAT

After presenting the content, ask:

> "What format do you want this in?
> 1. PDF (branded slide deck)
> 2. Markdown file (saved to output/)
> 3. Notion page (pushed to your workspace)
> 4. HTML (open in browser)
> 5. All of the above"

**If PDF:**
- Save content as `.md` in `output/`
- Render into branded HTML slide deck template
- Screenshot each slide via Playwright and combine into PDF
- Confirm the PDF path

**If Markdown:**
- Write to `output/[slug]-branded.md`
- Confirm the file path

**If Notion:**
- Save content to a `.md` file
- Run: `python scripts/push_to_notion.py --title "[title]" --content "output/[filename].md"`
- Return the Notion page URL

**If HTML:**
- Render into branded HTML template
- Save to `output/[slug]-branded.html`
- Confirm the file path

**If all of the above:**
- Run all output handlers.

---

## STEP 7 - VALIDATION

Before generating any output files, run the deterministic validation script:
```
python scripts/validate.py --content "output/[filename].md" --config "config.yaml"
```

This checks:
- Em dashes (banned)
- Banned words from config
- Structure rules (no H1 inside content, CTA exists, checklist exists)
- Image reference validation

Fix any failures before proceeding to PDF/Notion generation.

---

## IMPORTANT NOTES

- Always read BOTH `brand/brand-context.md` and `brand/voice-context.md` before writing
- The audit step (showing keep/cut/add) is not optional. It keeps the user in control.
- If the input is behind a login or paywalled, ask the user to paste the content directly
- Output files go in the `output/` folder. Never anywhere else.
- Slugify titles for filenames: lowercase, spaces to hyphens, remove special chars
- All outputs use DARK THEME only (dark mode from brand-context.md)
