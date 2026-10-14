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
    ("rel_path", "target"),
    [
        ("SPEC.md", "docs/development/build-plan/SPEC.md"),
        ("spec.md", "docs/development/build-plan/SPEC.md"),
        ("CONSTRAINTS.md", "docs/development/CONSTRAINTS.md"),
        ("Constraints.MD", "docs/development/CONSTRAINTS.md"),
        ("tasks/plan.md", "docs/development/build-plan/plan.md"),
        ("Tasks/Plan.md", "docs/development/build-plan/plan.md"),
        ("tasks/todo.md", "docs/development/build-plan/todo.md"),
        ("tasks/notes.md", "docs/development/build-plan/"),
        ("plan.md", "docs/development/build-plan/plan.md"),
        ("todo.md", "docs/development/build-plan/todo.md"),
        ("docs/development/SPEC.md", "docs/development/build-plan/SPEC.md"),
        ("docs/development/tasks/plan.md", "docs/development/build-plan/"),
        ("docs/development/requirements/auth.md", "docs/development/build-plan/archive/"),
    ],
)
def test_guard_misplaced_dev_docs_blocked_redirect(
    tmp_path: Path, rel_path: str, target: str, run_hook: HookRunner
) -> None:
    result = run_hook(str(tmp_path / rel_path))
    assert result.returncode == 2
    assert f"Write {target}" in result.stderr


@pytest.mark.parametrize(
    "rel_path",
    ["docs/development/conventions.md", "docs/development/CONSTRAINTS.md", "Docs/Development/Conventions.MD"],
)
def test_guard_existing_protected_file_blocked(tmp_path: Path, rel_path: str, run_hook: HookRunner) -> None:
    for name in ("conventions.md", "CONSTRAINTS.md"):
        (tmp_path / "docs" / "development").mkdir(parents=True, exist_ok=True)
        (tmp_path / "docs" / "development" / name).write_text("x", encoding="utf-8")
    result = run_hook(str(tmp_path / rel_path))
    assert result.returncode == 2
    assert "protected" in result.stderr


@pytest.mark.parametrize("rel_path", ["docs/development/conventions.md", "docs/development/CONSTRAINTS.md"])
def test_guard_missing_protected_file_creation_passes(tmp_path: Path, rel_path: str, run_hook: HookRunner) -> None:
    assert run_hook(str(tmp_path / rel_path)).returncode == 0


@pytest.mark.parametrize(
    "rel_path",
    [
        "docs/development/build-plan/SPEC.md",
        "docs/development/build-plan/plan.md",
        "docs/development/build-plan/todo.md",
        "docs/development/build-plan/archive/2026-10-auth-flow/SPEC.md",
        "docs/development/CONSTRAINTS.md",
        "docs/development/adr/ADR-001-x.md",
        "Docs/Development/Build-Plan/SPEC.md",
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
    assert run_hook("docs/development/build-plan/SPEC.md").returncode == 0


def test_guard_path_outside_repo_passes(tmp_path: Path, run_hook: HookRunner) -> None:
    outside = tmp_path.parent / "SPEC.md"
    assert run_hook(str(outside)).returncode == 0


def test_guard_no_file_path_passes(run_hook: HookRunner) -> None:
    assert run_hook(None).returncode == 0


@pytest.mark.skipif(sys.platform != "win32", reason="Windows paths are case-insensitive")
@pytest.mark.parametrize(
    ("rel_path", "expected"),
    [
        ("SPEC.md", 2),
        ("tasks\\plan.md", 2),
        ("docs\\development\\build-plan\\SPEC.md", 0),
        ("DOCS\\Development\\Build-Plan\\Spec.md", 0),
    ],
)
def test_guard_windows_mixed_case_paths_match(
    tmp_path: Path, rel_path: str, expected: int, run_hook: HookRunner
) -> None:
    mixed_root = str(tmp_path).swapcase()
    assert run_hook(f"{mixed_root}\\{rel_path}").returncode == expected
