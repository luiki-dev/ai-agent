# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A CLI coding agent (Boot.dev course project) that gives an LLM four file-system tools scoped to a sandbox directory. Python >= 3.13, managed with `uv`. The OpenAI SDK is pointed at OpenRouter via `OPENAI_BASE_URL`.

## Commands

```bash
uv sync                                    # install deps
uv run main.py "your prompt"               # run the agent
uv run main.py "your prompt" --verbose     # + token counts, model, tool args, tool results

uv run python -m test_get_files_info       # run one tool test script (from repo root)
cd calculator && uv run python tests.py    # unittest suite of the sample app (imports `pkg.*`, so cwd must be calculator/)
```

The test scripts at the repo root (`test_*.py`) are ad-hoc `print` scripts, not assertions — they exercise each tool against `calculator/` including the out-of-sandbox cases, and you verify output by eye. They must be run as modules from the repo root so `functions.*`/`utils.*` resolve. (The comment inside `test_get_files_info.py` says `tests.test_...`; that path is stale — the files live at the root now.)

Requires a `.env` (git-ignored) with `OPENROUTER_API_KEY`, `OPENAI_BASE_URL`, `AI_MODEL`; `load_dotenv()` reads it at startup.

## Architecture

**Agent loop** — [main.py](main.py) builds `[system_prompt, user_prompt]`, then loops up to 20 turns: `get_response` → `process_response`. A response with `tool_calls` dispatches each call and appends the results; a response without tool calls prints the text and ends the conversation. Exhausting 20 turns exits with status 1.

**Tool dispatch** — [functions/call_function.py](functions/call_function.py) is the single registry. Each tool is registered **twice**: in `available_functions` (the schema list sent to the model) and in `function_map` (name → callable). Adding a tool means touching both. It converts every result — success, exception, or unknown-function — into a `{"role": "tool", ...}` message, so the model always gets a reply.

**Sandbox model** — this is the core invariant. `WORKING_DIRECTORY` in [config.py](config.py) (`./calculator`) is injected into `function_args` by `call_function`, and the tool schemas deliberately do **not** expose a `working_directory` parameter — the model can never choose it. Enforcement lives in [utils/file_utils.py](utils/file_utils.py): `get_directory` and `get_file` resolve the path and reject anything not under the resolved working directory. `get_file` also takes a `File_mode` (READ/WRITE/EXECUTTE — note the spelling) that decides how a missing path is handled (error vs. `mkdir -p` the parent) and an optional extension whitelist (`run_python_file` requires `.py`).

**Tool modules** — [functions/](functions/) holds one file per tool, each pairing its JSON `schema_<name>` dict with its implementation. Convention: tool functions never raise — they catch and `return f"Error: {e}"` so the failure reaches the LLM as tool output rather than killing the loop. Path/permission checks raise inside `utils/file_utils.py` and are caught at the tool boundary.

**Other limits** — `MAX_CHARS_TO_SEND_TO_LLM` (10000) truncates file reads with an explicit `[...truncated]` marker; `run_python_file` uses a 30s subprocess timeout.

**[calculator/](calculator/)** is the sample app the agent operates on — target data, not agent code. Editing it is expected (the tests overwrite `calculator/lorem.txt`).

## Conventions

Suppressions are inline per-line: `# noqa: <rule>` for ruff, `# nosec: <id>` for bandit. Neither tool is configured in `pyproject.toml`, so they run from the editor/externally — keep the markers when moving code.
