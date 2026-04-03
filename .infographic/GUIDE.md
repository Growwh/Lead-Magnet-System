# Infographic Style Guide Folder

This folder contains `brand.md`, which controls how AI-generated infographics look.

## What It Does

When the system generates infographics (via Gemini API), it reads this style guide to construct image generation prompts that match your brand.

## What to Customize

- **Background color** - Match your brand's background
- **Accent colors** - Your primary and secondary accents
- **Typography style** - What font style to request
- **Layout tiers** - Which layouts work reliably (Tier 1 vs. Tier 2)
- **Anti-hallucination rules** - Prompt construction rules to avoid garbled text

## Requirements

- A paid Gemini API key (free tier does not support image generation via API)
- Set `pipeline.infographic_count` to 2 or 3 in `config.yaml`
- Set `GEMINI_API_KEY` in `.env`
