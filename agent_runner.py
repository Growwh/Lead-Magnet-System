"""
Lead Magnet System In A Box - CLI Entry Point

Usage:
    python agent_runner.py "https://example.com/article"
    python agent_runner.py "path/to/file.pdf"
    python agent_runner.py --json "https://example.com/article"

The --json flag outputs structured JSON with file paths instead of text.
"""
import argparse
import asyncio
import json
import sys

try:
    from agent.agent import LeadMagnetAgent
except ImportError:
    sys.exit(
        "Agent module not found. Make sure agent/__init__.py and agent/agent.py exist.\n"
        "Run: pip install -r requirements.txt"
    )


async def main():
    parser = argparse.ArgumentParser(
        description="Generate a branded lead magnet from any content source."
    )
    parser.add_argument(
        "input",
        help="URL, file path, or text content to transform into a lead magnet",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output structured JSON with file paths instead of text",
    )
    parser.add_argument(
        "--no-notion",
        action="store_true",
        help="Skip Notion push even if configured",
    )

    args = parser.parse_args()

    agent = LeadMagnetAgent()

    async def on_message(text: str):
        if not args.json:
            print(text, end="", flush=True)

    result = await agent.run(
        args.input,
        on_message=on_message,
        push_to_notion=not args.no_notion,
    )

    if args.json:
        # Remove raw_output from JSON (too large)
        output = {k: v for k, v in result.items() if k != "raw_output"}
        print(json.dumps(output, indent=2))
    else:
        print("\n\n--- Result ---")
        for key, value in result.items():
            if key != "raw_output" and value:
                print(f"  {key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())
