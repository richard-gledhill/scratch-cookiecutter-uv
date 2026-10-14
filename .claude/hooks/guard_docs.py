"""Claude Code PreToolUse hook: keep development docs under docs/development/.

Reads the tool call as JSON on stdin. Exit 2 (with a message on stderr) blocks the write and tells the
agent where to write instead; exit 0 allows it. Edits to MkDocs content and mkdocs.yml are allowed.
Shell-command edits (mv, sed) are not seen by this hook.
"""

import json
import os
import sys
from pathlib import Path

BUILD_PLAN = "docs/development/build-plan"
# Default locations used by the agent workflows (and old layouts) mapped to where the file belongs.
REDIRECTS = {
    "spec.md": f"{BUILD_PLAN}/SPEC.md",
    "constraints.md": "docs/development/CONSTRAINTS.md",
    "plan.md": f"{BUILD_PLAN}/plan.md",
    "todo.md": f"{BUILD_PLAN}/todo.md",
    "tasks/plan.md": f"{BUILD_PLAN}/plan.md",
    "tasks/todo.md": f"{BUILD_PLAN}/todo.md",
    "docs/development/spec.md": f"{BUILD_PLAN}/SPEC.md",
}
PREFIX_REDIRECTS = {
    "tasks/": f"{BUILD_PLAN}/",
    "docs/development/tasks/": f"{BUILD_PLAN}/",
    "docs/development/requirements/": f"{BUILD_PLAN}/archive/YYYY-MM-<name>/",
}

data = json.load(sys.stdin)
path = data.get("tool_input", {}).get("file_path")
if not path:
    sys.exit(0)

root = Path(os.environ.get("CLAUDE_PROJECT_DIR", data.get("cwd", "."))).resolve()
try:
    rel = (root / path).resolve().relative_to(root).as_posix().lower()
except ValueError:
    sys.exit(0)  # outside the repo

target = REDIRECTS.get(rel) or next((t for prefix, t in PREFIX_REDIRECTS.items() if rel.startswith(prefix)), None)
if target:
    print(f"Blocked: {rel} is not a development docs path (see AGENTS.md). Write {target} instead.", file=sys.stderr)
    sys.exit(2)
