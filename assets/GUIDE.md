# Assets Folder

This folder stores brand assets used by the system.

## What Goes Here

- **Logo files** - PNG format (standard + converted versions)
- **Logo base64** - Pre-encoded logo for embedding in PDFs without external dependencies
- **Brand images** - Any static images used in templates

## Logo Setup

1. Place your logo PNG in this folder (e.g., `logo.png`)
2. Generate a base64 version: `base64 logo.png > logo_b64.txt`
3. Update `config.yaml` with: `logo.has_logo: true` and `logo.file: "assets/logo.png"`
4. The PDF template will automatically embed the logo on cover pages

## No Logo?

That's fine. The system works without a logo. It uses your brand name (from `config.yaml`) as text instead.
