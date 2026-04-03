# Brand Folder

This folder contains all brand-related context files that the system reads before writing any content.

## Files

### `brand-context.md`
The complete visual design system. Colors, typography, shadows, components, corner radius, spacing, glass panels, do's and don'ts. Every script and template reads this to ensure visual consistency.

**When to edit:** When your brand colors, fonts, or visual style changes.

### `voice-context.md`
How you speak, write, and think. Speech patterns, writing rules, banned words, voice examples, content structure, and the pre-publish checklist. The writing pipeline reads this before producing any content.

**When to edit:** When your voice evolves, when you add new banned words, or when you want to adjust how the system writes.

## How It Works

1. The pipeline loads `brand-context.md` for visual decisions (PDF templates, HTML styling)
2. The pipeline loads `voice-context.md` for writing decisions (tone, structure, rules)
3. Both files are injected into the system prompt before Claude writes anything
4. `config.yaml` in the root has quick-reference tokens (hex codes, font names) that scripts read programmatically. The brand folder has the full narrative context.
