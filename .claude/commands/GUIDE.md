# Claude Commands Folder

This folder contains Claude Code command definitions that define the interactive pipeline.

## What It Does

When you run `/repurpose-lead-magnet` in Claude Code, it reads the command file from this folder. The command file defines the step-by-step pipeline:

1. Get input (URL, file, or pasted text)
2. Identify the lead magnet type
3. Load brand context
4. Run the enhancement engine (audit > remove > write > rebrand)
5. Generate infographics (if enabled)
6. Run validation checks
7. Generate PDF + DOCX
8. Push to Notion (if configured)

## Customization

Edit the command `.md` file to change:
- Pipeline stages and their order
- Which outputs to generate
- Approval gates (interactive vs. autonomous)
- Brand-specific writing rules
