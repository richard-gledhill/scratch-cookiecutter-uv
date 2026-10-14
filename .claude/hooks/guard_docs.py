"""Claude Code PreToolUse hook: keep development docs under docs/development/.

Reads the tool call as JSON on stdin. Exit 2 (with a message on stderr) blocks the write and tells the
agent where to write instead; exit 0 allows it. Edits to MkDocs content and mkdocs.yml are allowed.
Shell-command edits (mv, sed) are not seen by this hook.
"""

import json
import os
import sys
from pathlib import Path

data = json.load(sys.stdin)
path = data.get("tool_input", {}).get("file_path")
if not path:
    sys.exit(0)

root = Path(os.environ.get("CLAUDE_PROJECT_DIR", data.get("cwd", "."))).resolve()
try:
    rel = (root / path).resolve().relative_to(root).as_posix().lower()
except ValueError:
    sys.exit(0)  # outside the repo

if rel in ("spec.md", "constraints.md") or rel.startswith("tasks/"):
    print(
        f"Blocked: {rel} belongs under docs/development/ (see AGENTS.md). Write it there instead.",
        file=sys.stderr,
    )
    sys.exit(2)
