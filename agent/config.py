"""
Configuration loader for the Lead Magnet Agent.
Reads .env from the project root and validates API keys.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# No keys are strictly required when running via Claude Code.
# Notion and Gemini are optional features that degrade gracefully.
_OPTIONAL_KEYS = ["GEMINI_API_KEY", "NOTION_API_KEY", "NOTION_PARENT_PAGE_ID"]


def load_and_validate_env(project_root: Path) -> None:
    """Load .env from project_root and warn about missing optional keys."""
    load_dotenv(project_root / ".env")

    import warnings
    missing_optional = [k for k in _OPTIONAL_KEYS if not os.getenv(k)]
    if missing_optional:
        warnings.warn(
            f"Optional environment variables not set: {', '.join(missing_optional)}. "
            f"Some features (infographics, Notion push) will be unavailable.",
            stacklevel=2,
        )
