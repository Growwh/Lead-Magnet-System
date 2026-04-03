# Agent Folder

This folder contains the standalone Python agent that runs the full lead magnet pipeline autonomously.

## How It Works

The agent uses the Anthropic Python SDK directly (no Claude Code CLI required). It receives a user input (URL, file path, or text), runs the full pipeline, and returns generated files.

### Files

- `agent.py` - The `LeadMagnetAgent` class. Agentic loop with tool calling.
- `config.py` - Environment validation. Loads `.env` and checks required keys.
- `system_prompt.py` - Builds the system prompt from the skill file + brand context.
- `tools.py` - Tool definitions and executors. Each tool wraps a Python script via subprocess.

### Running the Agent

```python
# Async
from agent import LeadMagnetAgent
agent = LeadMagnetAgent()
result = await agent.run("https://example.com/article")

# Sync
from agent import run_sync
result = run_sync("https://example.com/article")

# CLI
python agent_runner.py "https://example.com/article"
```

### Adding a New Tool

1. Add the tool schema to `TOOL_DEFINITIONS` in `tools.py`
2. Add a `_run_<tool_name>` method to `ToolExecutor`
3. The agent will automatically discover and use it

## Pipeline Flow

```
Input (URL/text/file)
  > fetch_content (extract text)
  > write_file (generate markdown in brand voice)
  > validate (deterministic checks)
  > generate_pdf (HTML > screenshot > PDF)
  > push_to_notion (optional)
  > Return result with file paths
```
