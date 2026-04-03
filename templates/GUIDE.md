# Templates Folder

This folder stores reusable HTML templates for rendering lead magnets into branded PDFs.

## How It Works

1. The writing pipeline generates content (markdown)
2. Content is injected into an HTML template from this folder
3. Playwright renders the HTML as high-quality screenshots
4. Screenshots are combined into a PDF

## Template Types

### Playbook Template (slide deck)
- Square format (1080x1080px) for LinkedIn-friendly output
- One concept per slide
- Dark theme with glass morphism cards
- Uses brand colors, fonts, and neumorphic styles from `config.yaml`

### Future Templates
- **Infographic template** - Single-page visual data presentation
- **Guide template** - Sequential, step-by-step layout
- **Checklist template** - Action-dense, checkbox-heavy format

## Customization

Templates read CSS variables from `config.yaml`:
- Colors (accent, background, text)
- Fonts (display, body, mono)
- Corner radius, shadows, spacing

To add a new template:
1. Create an HTML file in this folder
2. Use CSS variables for all brand tokens
3. Add `page-break-after: always` on each slide/page div
4. The screenshot-to-PDF script handles the rest
