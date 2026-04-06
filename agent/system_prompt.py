"""
Builds the agent system prompt at runtime from the existing skill file and brand context files.
The source files remain the single source of truth - nothing is duplicated here.
"""
from pathlib import Path


def build_system_prompt(project_root: Path, brand_text: str = None, voice_text: str = None) -> str:
    skill_file = project_root / ".claude" / "commands" / "repurpose-lead-magnet.md"
    brand_file = project_root / "brand" / "brand-context.md"
    voice_file = project_root / "brand" / "voice-context.md"

    if not skill_file.exists():
        raise FileNotFoundError(
            f"Skill file not found: {skill_file}\n"
            "Ensure .claude/commands/repurpose-lead-magnet.md exists."
        )

    parts = [skill_file.read_text(encoding="utf-8")]

    # Use the variable if provided, otherwise fallback to the file
    if brand_text:
        parts.append(f"\n\n---\n\n## Brand Context\n\n{brand_text}")
    elif brand_file.exists():
        parts.append("\n\n---\n\n## Brand Context\n\n")
        parts.append(brand_file.read_text(encoding="utf-8"))
        
    if voice_text:
        parts.append(f"\n\n---\n\n## Voice Context\n\n{voice_text}")
    elif voice_file.exists():
        parts.append("\n\n---\n\n## Voice Context\n\n")
        parts.append(voice_file.read_text(encoding="utf-8"))

    return "".join(parts)
