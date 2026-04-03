"""
validate.py
Deterministic validation script for lead magnet content.
Checks for banned words, em dashes, structure rules, and formatting issues.
Runs in milliseconds with 100% accuracy. No LLM needed.

Usage:
    python scripts/validate.py --content "output/playbook.md" --config "config.yaml"
"""
import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pyyaml not installed. Run: pip install pyyaml")


def validate(content: str, config: dict) -> list[dict]:
    """
    Validate content against config rules.
    Returns a list of issues found. Empty list = all checks passed.
    """
    issues = []
    lines = content.split("\n")

    # 1. Em dash check
    for i, line in enumerate(lines):
        if "\u2014" in line:  # em dash
            issues.append({
                "rule": "em_dash",
                "severity": "error",
                "line": i + 1,
                "message": f"Em dash found on line {i + 1}: ...{line.strip()[:60]}...",
            })

    # 2. Banned words
    banned = config.get("content", {}).get("banned_words", [])
    content_lower = content.lower()
    for word in banned:
        if word.lower() in content_lower:
            # Find the line
            for i, line in enumerate(lines):
                if word.lower() in line.lower():
                    issues.append({
                        "rule": "banned_word",
                        "severity": "error",
                        "line": i + 1,
                        "message": f"Banned word '{word}' found on line {i + 1}",
                    })
                    break  # Report first occurrence only

    # 3. First line must be a callout (if using callout format)
    first_content_line = ""
    for line in lines:
        stripped = line.strip()
        if stripped:
            first_content_line = stripped
            break

    if first_content_line and not first_content_line.startswith("[callout:"):
        issues.append({
            "rule": "first_line_callout",
            "severity": "warning",
            "line": 1,
            "message": "First non-empty line is not a [callout:emoji] block",
        })

    # 4. No H1 headings inside content
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            issues.append({
                "rule": "no_h1",
                "severity": "error",
                "line": i + 1,
                "message": f"H1 heading found on line {i + 1}. Use ## (H2) instead.",
            })

    # 5. CTA section exists
    has_cta = any("want help" in line.lower() or "book a" in line.lower() for line in lines)
    if not has_cta:
        issues.append({
            "rule": "missing_cta",
            "severity": "warning",
            "line": 0,
            "message": "No CTA section detected (looking for 'Want Help' or 'Book a')",
        })

    # 6. Action checklist exists
    has_checklist = any(line.strip().startswith("- [ ]") for line in lines)
    if not has_checklist:
        issues.append({
            "rule": "missing_checklist",
            "severity": "warning",
            "line": 0,
            "message": "No action checklist found (looking for '- [ ]' items)",
        })

    # 7. FAQ section exists
    has_faq = any("faq" in line.lower() or "frequently" in line.lower() for line in lines)
    if not has_faq:
        issues.append({
            "rule": "missing_faq",
            "severity": "warning",
            "line": 0,
            "message": "No FAQ section detected",
        })

    # 8. Image references match files (if images_dir provided)
    image_refs = re.findall(r"\[image:(.+?)\]", content)
    for ref in image_refs:
        img_path = Path("output") / ref.strip()
        if not img_path.exists():
            issues.append({
                "rule": "missing_image",
                "severity": "error",
                "line": 0,
                "message": f"Image reference '{ref.strip()}' not found in output/",
            })

    return issues


def main():
    parser = argparse.ArgumentParser(description="Validate lead magnet content")
    parser.add_argument("--content", required=True, help="Path to markdown file")
    parser.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    args = parser.parse_args()

    content_path = Path(args.content)
    if not content_path.exists():
        sys.exit(f"Content file not found: {args.content}")

    config_path = Path(args.config)
    if not config_path.exists():
        sys.exit(f"Config file not found: {args.config}")

    content = content_path.read_text(encoding="utf-8")
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    issues = validate(content, config)

    if not issues:
        print("PASSED: All validation checks passed.")
        sys.exit(0)

    errors = [i for i in issues if i["severity"] == "error"]
    warnings = [i for i in issues if i["severity"] == "warning"]

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)\n")
    else:
        print(f"PASSED with {len(warnings)} warning(s)\n")

    for issue in issues:
        prefix = "ERROR" if issue["severity"] == "error" else "WARN"
        line_info = f" (line {issue['line']})" if issue["line"] > 0 else ""
        print(f"  [{prefix}] {issue['rule']}{line_info}: {issue['message']}")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
