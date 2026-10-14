import io
import json
import runpy
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pytest

HOOK = Path(__file__).parent.parent / ".claude" / "hooks" / "guard_docs.py"


# region Test helpers
@dataclass
class HookResult:
    returncode: int
    stderr: str


HookRunner = Callable[[str | None], HookResult]


@pytest.fixture
def run_hook(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> HookRunner:
    """Run the hook script in-process the way Claude Code does: JSON on stdin, exit code and stderr out."""

    def _run(file_path: str | None) -> HookResult:
        tool_input = {} if file_path is None else {"file_path": file_path}
        payload = {"tool_name": "Write", "tool_input": tool_input, "cwd": str(tmp_path)}
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
        monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
        code = 0
        try:
            runpy.run_path(str(HOOK), run_name="__main__")
        except SystemExit as exit_:
            code = exit_.code if isinstance(exit_.code, int) else 0
        return HookResult(returncode=code, stderr=capsys.readouterr().err)

    return _run


# endregion


@pytest.mark.parametrize(
    "rel_path",
    ["SPEC.md", "CONSTRAINTS.md", "tasks/plan.md", "tasks/todo.md", "spec.md", "Tasks/Plan.md", "Constraints.MD"],
)
def test_guard_root_dev_docs_blocked_redirect(tmp_path: Path, rel_path: str, run_hook: HookRunner) -> None:
    result = run_hook(str(tmp_path / rel_path))
    assert result.returncode == 2
    assert "docs/development/" in result.stderr


@pytest.mark.parametrize(
    "rel_path",
    [
        "docs/development/SPEC.md",
        "docs/development/adr/ADR-001-x.md",
        "docs/development/tasks/plan.md",
        "Docs/Development/SPEC.md",
        "src/x.py",
        "docs/index.md",
        "docs/new-page.md",
        "mkdocs.yml",
    ],
)
def test_guard_allowed_paths_pass(tmp_path: Path, rel_path: str, run_hook: HookRunner) -> None:
    assert run_hook(str(tmp_path / rel_path)).returncode == 0


def test_guard_relative_path_resolved_against_root(run_hook: HookRunner) -> None:
    assert run_hook("SPEC.md").returncode == 2
    assert run_hook("docs/development/SPEC.md").returncode == 0


def test_guard_path_outside_repo_passes(tmp_path: Path, run_hook: HookRunner) -> None:
    outside = tmp_path.parent / "SPEC.md"
    assert run_hook(str(outside)).returncode == 0


def test_guard_no_file_path_passes(run_hook: HookRunner) -> None:
    assert run_hook(None).returncode == 0


@pytest.mark.skipif(sys.platform != "win32", reason="Windows paths are case-insensitive")
@pytest.mark.parametrize(
    ("rel_path", "expected"),
    [("SPEC.md", 2), ("tasks\\plan.md", 2), ("docs\\development\\SPEC.md", 0), ("DOCS\\Development\\Spec.md", 0)],
)
def test_guard_windows_mixed_case_paths_match(
    tmp_path: Path, rel_path: str, expected: int, run_hook: HookRunner
) -> None:
    mixed_root = str(tmp_path).swapcase()
    assert run_hook(f"{mixed_root}\\{rel_path}").returncode == expected
