"""
screenshot_to_pdf.py
Renders branded HTML via Playwright, takes per-slide screenshots,
and combines them into a high-quality PDF.

Usage:
    python scripts/screenshot_to_pdf.py --html "output/playbook.html" --output "output/playbook.pdf"
"""
import argparse
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("playwright not installed. Run: pip install playwright && python -m playwright install chromium")

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow not installed. Run: pip install Pillow")


def html_to_pdf(html_path: str, output_path: str):
    html_path = Path(html_path).resolve()
    output_path = Path(output_path).resolve()

    if not html_path.exists():
        sys.exit(f"HTML file not found: {html_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Rendering: {html_path}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": 1080, "height": 1080},  # Square slide format
            device_scale_factor=2,  # 2x for crisp rendering
        )

        page.goto(f"file:///{html_path}", wait_until="networkidle", timeout=30000)
        # Wait for Google Fonts to load
        page.wait_for_timeout(2000)

        # Find all slide sections
        page_elements = page.query_selector_all(".slide, .cover, .page")

        if not page_elements:
            print("No .slide, .cover, or .page elements found. Taking full page screenshot.")
            page.screenshot(path=str(output_path.with_suffix(".png")), full_page=True)
            browser.close()
            return

        print(f"Found {len(page_elements)} pages. Screenshotting each...")

        screenshots = []
        for i, element in enumerate(page_elements):
            img_path = output_path.parent / f"_page_{i+1}.png"
            element.screenshot(path=str(img_path))
            screenshots.append(img_path)
            print(f"  Page {i+1}: {img_path.name}")

        browser.close()

    # Combine screenshots into PDF
    print(f"Combining {len(screenshots)} pages into PDF...")

    images = []
    for ss_path in screenshots:
        img = Image.open(ss_path).convert("RGB")
        images.append(img)

    if images:
        images[0].save(
            str(output_path),
            "PDF",
            save_all=True,
            append_images=images[1:],
            resolution=150.0,
        )
        size_kb = output_path.stat().st_size // 1024
        print(f"\nSUCCESS: {output_path} ({size_kb} KB, {len(images)} pages)")

    # Clean up temp screenshots
    for ss_path in screenshots:
        ss_path.unlink(missing_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert branded HTML to PDF via screenshots")
    parser.add_argument("--html", required=True, help="Path to the HTML file")
    parser.add_argument("--output", required=True, help="Output PDF path")
    args = parser.parse_args()
    html_to_pdf(args.html, args.output)
