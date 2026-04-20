# Sidekick Setup — Step-by-step

End-to-end setup for installing `sidekick-agent-mcp` and wiring it into a
Claude Code (or other MCP client) workflow. ~10 minutes.

## 0. What you need before starting

- Python 3.10+ installed and on PATH
- An Anthropic-compatible LLM endpoint + API key. Options:
  - **MiniMax direct:** `https://api.minimax.io/anthropic` (native)
  - **LiteLLM / LiteLLM-proxy gateway** routing to MiniMax, Claude Haiku,
    Gemini, Llama, etc. Any model exposed via `/v1/messages`
  - **OpenRouter** Anthropic-compatible proxy
  - **Self-hosted vLLM / sglang / Ollama** that speaks the Anthropic protocol
- Claude Code installed (or any MCP client that supports `stdio` transport)
- A project directory you want to use as the sidekick's "workspace"

---

## 1. Install Python deps (MCP source is shipped with this skill)

After `npx skills add duylamle/product-collection@sidekick-agent-mcp-setup -y`, the MCP
Python source lives inside the skill at `skills/sidekick-agent-mcp-setup/mcp/`. No
`git clone` required.

### Option A — Install from requirements (simplest)

```bash
# Find where the skill landed — usually under ~/.claude/skills/ or
# <project>/.claude/skills/sidekick-agent-mcp-setup/
cd /abs/path/to/skills/sidekick-agent-mcp-setup/mcp
pip install -r requirements.txt
```

### Option B — Editable pip install

```bash
cd /abs/path/to/skills/sidekick-agent-mcp-setup/mcp
pip install -e .
```

Editable install gives you the `sidekick-agent-mcp` console script as an
alternate entrypoint.

> **Upgrading the MCP?** Re-run `npx skills add duylamle/product-collection@sidekick-agent-mcp-setup -y` — the MCP source inside the skill is refreshed along with the docs.

### Verify install

```bash
python -c "import mcp, httpx, pydantic; print('deps OK')"
```

---

## 2. Smoke test the server

Without any real API key, confirm the server loads and registers its tools:

```bash
SIDEKICK_API_KEY=x \
SIDEKICK_API_BASE=http://localhost:9999 \
SIDEKICK_WORKSPACE_ROOT="." \
  python -c "
import sys; sys.path.insert(0, '.')
from sidekick_agent.server import mcp
print([t.name for t in mcp._tool_manager.list_tools()])
"
```

Expected:

```
['sidekick_summarize', 'sidekick_translate', 'sidekick_task', 'sidekick_agent_run']
```

If this fails, the Python install is wrong — fix before moving on.

---

## 3. Live test against your real endpoint

Pick a small, boring file in your workspace and confirm the full round-trip:

```bash
SIDEKICK_API_KEY="sk-your-real-key" \
SIDEKICK_API_BASE="https://your-endpoint/v1" \
SIDEKICK_MODEL="minimax/MiniMax-M2.7-highspeed" \
SIDEKICK_WORKSPACE_ROOT="/abs/path/to/your/workspace" \
SIDEKICK_MAX_TOKENS=4000 \
  python -c "
import sys; sys.path.insert(0, '.')
from sidekick_agent import client
r = client.call_llm('You are a reasoner.', 'Reply in 1 short sentence: 2+2=?')
print('TEXT:', r['text'][:100])
print('USAGE:', r['usage'])
"
```

If you see a short answer and non-zero token usage → endpoint works.

Common failure modes:
- `http_401` → key invalid
- `http_404` → `SIDEKICK_API_BASE` wrong (did you include `/v1` or trailing `/messages`?)
- `empty_messages` → `SIDEKICK_API_BASE` OK but endpoint returned empty
  `messages` field. Usually a provider config issue upstream
- `does not support max tokens > ...` → provider rejected `max_tokens`.
  Lower `SIDEKICK_MAX_TOKENS`

---

## 4. Register with Claude Code

Edit `~/.claude.json` (Claude Code config) and add under `mcpServers`:

```json
{
  "mcpServers": {
    "sidekick-agent": {
      "type": "stdio",
      "command": "python",
      "args": ["/abs/path/to/skills/sidekick-agent-mcp-setup/mcp/server.py"],
      "env": {
        "SIDEKICK_API_KEY": "sk-your-real-key",
        "SIDEKICK_API_BASE": "https://your-endpoint/v1",
        "SIDEKICK_MODEL": "minimax/MiniMax-M2.7-highspeed",
        "SIDEKICK_MAX_TOKENS": "16000",
        "SIDEKICK_WORKSPACE_ROOT": "/abs/path/to/workspace",
        "SIDEKICK_EXTRA_BLACKLIST": "secrets/**,_logs/**"
      }
    }
  }
}
```

Or via CLI:

```bash
claude mcp add sidekick-agent -- \
  python /abs/path/to/skills/sidekick-agent-mcp-setup/mcp/server.py
# then set env vars by editing ~/.claude.json directly
```

Restart Claude Code (close + reopen). Verify:

```bash
claude mcp list
```

Expected line:

```
sidekick-agent: python /abs/path/... - ✓ Connected
```

Not connected? Common fixes:
- `ModuleNotFoundError: sidekick_agent` → `args[0]` path is wrong OR you
  moved the folder without updating the config
- `ERROR: Missing required env var` → check `env` block in JSON has
  `SIDEKICK_API_KEY` and `SIDEKICK_API_BASE`
- Silent disconnect → run the server manually (`python server.py`) and
  read stderr. Most startup issues print before the MCP handshake

---

## 5. Install the rule into your project

The delegation rule tells Claude **when** to shift work to sidekick (and when
not to). Copy it into your Claude Code project's rules area so it applies
automatically in every session.

For a Lamber-style layout (`.claude/rules/`):

```bash
# Adjust SKILL to wherever npx skills add landed the skill
SKILL=/abs/path/to/skills/sidekick-setup
PROJECT=/path/to/your/project
cp "$SKILL/docs/rules/rule-sidekick-delegation.md" "$PROJECT/.claude/rules/"
```

Then update your rules index file so the rule is auto-loaded (or referenced
on demand). For Lamber this is `.claude/rules/CLAUDE.md`; for other setups
follow your project's convention.

> **Note:** The companion `sidekick-call` skill is already bundled inside
> this skill at `docs/skills/sidekick-call/` — Claude Code reads it directly
> from there, no copy needed.

---

## 6. First real call

In Claude Code, ask Claude to do something small via sidekick:

> "Use `sidekick_summarize` to condense `README.md` into 5 bullets."

Claude should call `mcp__sidekick-agent__sidekick_summarize` with
`file_paths=["README.md"]` and `max_bullets=5`. You'll get 5 bullets back.

Check the audit log landed correctly:

```bash
ls "$SIDEKICK_LOG_DIR"  # default: <workspace>/_logs/_sidekick-pending/
```

You should see a `<session-id>.jsonl` file with one entry per call.

---

## 7. Tune env vars to your workload

| Knob | Default | When to change |
|---|---|---|
| `SIDEKICK_MAX_TOKENS` | 8000 | Bump to 16000-32000 for long drafts / translations |
| `SIDEKICK_THINKING` | 1 (on) | Set `0` to disable thinking — saves tokens for simple tasks |
| `SIDEKICK_AGENT_MAX_ITERATIONS` | 15 | Lower (e.g. 5) for narrow agent_run tasks; higher for broad exploration |
| `SIDEKICK_FILE_SIZE_KB` | 500 | Raise if you need to feed larger files (caps individual reads) |
| `SIDEKICK_WRITE_ALLOWLIST` | "" (read-only) | Comma-separated globs — set when you want agent_run to write |
| `SIDEKICK_EXTRA_BLACKLIST` | "" | Comma-separated globs — add project-specific secret paths |

---

## 8. Common post-setup checks

- **Writes blocked even though I set the allowlist** — the blacklist always
  wins. Check your path isn't matching a default pattern (`.env`, `*secret*`,
  `.git/**`, `node_modules/**`, etc.)
- **Sidekick hallucinates** — lower `SIDEKICK_TEMPERATURE` (try 0.01-0.1)
  and make the `task` prompt more specific. Keep `safeguards=True` so the
  junior marks `[ASSUMPTION: ...]` / `[TBD: ...]` inline
- **Cost spikes** — inspect the `_logs/_sidekick-pending/*.jsonl`. If
  `prompt_tokens` grows across a conversation, you're hitting the conversation
  store without compaction. Either call without `conversation_id` or
  compact manually (see `SKILL.md` multi-turn pattern)
- **Tool not showing in Claude** — restart Claude Code. MCP tools load at
  session start; live-reload isn't supported

---

## 9. Uninstall

```bash
# 1. Remove the MCP entry from ~/.claude.json
# 2. If installed via editable pip install:
pip uninstall sidekick-agent-mcp
# 3. Remove the skill (this also removes the bundled MCP source):
npx skills remove duylamle/product-collection@sidekick-agent-mcp-setup
# 4. (Optional) delete the delegation rule you copied in step 5:
rm /path/to/your/project/.claude/rules/rule-sidekick-delegation.md
```

Logs under `$SIDEKICK_LOG_DIR` are safe to delete any time.

Logs under `$SIDEKICK_LOG_DIR` are safe to delete any time.
