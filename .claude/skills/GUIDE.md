# Claude Skills Folder

This folder contains interactive skill definitions for Claude Code.

## Commands vs. Skills

- **Commands** (in `.claude/commands/`) are invoked via slash commands
- **Skills** (in `.claude/skills/`) are interactive versions with approval gates

Both define the same pipeline, but skills pause for user confirmation between stages.

## When to Use Skills

Use the interactive skill when you want to:
- Review the audit findings before proceeding
- Choose which output formats to generate
- Preview content before pushing to Notion
