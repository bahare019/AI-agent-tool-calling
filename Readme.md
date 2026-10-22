# AI Agent with Tool Calling

A small AI agent built **from scratch** (no agent framework) using the OpenAI-compatible API of [OpenRouter](https://openrouter.ai). The model decides on its own when to call a tool, the program executes it, and the result goes back to the model until it can answer.

The main design goal: **let an LLM run code without trusting it.**

## Features

- **Tool-calling loop** written by hand (~50 lines in `agent.py`)
- **Sandboxed Python execution**: model-written code runs inside a throwaway Docker container
- **File tools** confined to a `workspace/` folder (read, write, list)
- **Web search** via DuckDuckGo (no API key needed)
- **Safe calculator** built on Python's `ast` module instead of `eval`
- **Persistent memory**: conversation history survives restarts (`history.json`)
- **Tool-call logging** with timestamps (`agent_log.txt`)
- **Modular tools**: adding a tool means adding one file

## How it works

```
user message ──► model ──► wants a tool? ──yes──► run tool ──► result back to model ─┐
                   ▲                                                                │
                   └────────────────────────────────────────────────────────────────┘
                              no ──► final answer
```

The loop is capped at a maximum number of turns so a confused model cannot loop forever.

## Security design

Code written by the model is untrusted. `run_python_code` executes it like this:

| Protection | How |
|---|---|
| No network | `--network none` |
| No writes | `--read-only` root filesystem (small `tmpfs` for `/tmp`) |
| Resource limits | `--memory 256m`, `--cpus 0.5`, `--pids-limit 64` |
| Time limit | 15 s timeout; the container is force-removed if it hangs |
| Non-root | the sandbox image runs as an unprivileged user |
| Isolated files | only `workspace/` is mounted, **read-only** |
| Disposable | `--rm`: every run starts from a clean container |

The file tools (`read_file`, `write_file`, `list_files`) resolve every path and reject anything outside `workspace/`, including `../` tricks.

The sandbox image ships with `pandas` and `numpy`, installed at build time, so the container never needs internet access.

## Project structure

```
.
├── agent.py            # the agent loop and CLI
├── config.py           # settings, paths, system prompt, API client
├── history.py          # load/save conversation memory
├── logger.py           # tool-call logging
├── tools/
│   ├── __init__.py     # registry of all tools
│   ├── calculator.py
│   ├── code_runner.py  # Docker sandbox
│   ├── file_tools.py
│   └── web_search.py
├── sandbox/
│   ├── Dockerfile      # image used to run model-written code
│   └── requirements.txt
├── requirements.txt
└── .env.example
```

## Getting started

**Requirements:** Python 3.10+, Docker Desktop (running), an [OpenRouter](https://openrouter.ai) API key.

```bash
# 1. install dependencies
pip install -r requirements.txt

# 2. configure the API key
cp .env.example .env          # Windows PowerShell: copy .env.example .env
# then edit .env and set OPENROUTER_API_KEY

# 3. build the sandbox image (once)
docker build -t agent-sandbox:latest sandbox

# 4. run
python agent.py
```

The default model is set in `config.py`. Pick one that supports tool calling (many free OpenRouter models do, but quality varies).

## Example

<!-- Replace this with a real transcript or screenshot from your own run -->
```
You: Read data.csv with pandas and compute the total revenue (price * qty)
[tool called: run_python_code(...)]
Agent: The total revenue is 209000.
```

Files placed in `workspace/` are visible to the sandboxed code at `/workspace`.

## Adding a tool

1. Create `tools/my_tool.py` with the function, a `SCHEMAS` list (the description the model sees) and a `FUNCTIONS` dict (name → function).
2. Register it in `tools/__init__.py`.

That's all. `agent.py` does not change.

## Limitations

- Tool-calling reliability depends on the model; free models sometimes pick the wrong tool or give up early.
- Conversation history is not trimmed or summarized yet, so very long sessions will grow the context.
- Code in the sandbox cannot write files; it prints results and the agent saves them with `write_file`.
- Web search uses an unofficial DuckDuckGo client and can be rate-limited.
- This is a learning project, not a hardened production sandbox.

## Roadmap

- History summarization
- Retrieval tool backed by a vector store (RAG)
- Human confirmation before sensitive tool calls
- Automated tests and a small evaluation set

## License

MIT
