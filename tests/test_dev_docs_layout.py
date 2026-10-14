import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
DEV_DOCS = ROOT / "docs" / "development"
SUBFOLDERS = ["requirements", "rfcs", "adr", "architecture", "testing", "operations", "tasks"]


def test_dev_docs_index_readme_exists() -> None:
    assert (DEV_DOCS / "README.md").is_file()


@pytest.mark.parametrize("folder", SUBFOLDERS)
def test_dev_docs_subfolder_readme_exists(folder: str) -> None:
    assert (DEV_DOCS / folder / "README.md").is_file()


def test_dev_docs_no_spec_or_constraints_created() -> None:
    # Created later by the agent workflows, not shipped.
    assert not (DEV_DOCS / "SPEC.md").exists()
    assert not (DEV_DOCS / "CONSTRAINTS.md").exists()


def test_mkdocs_excludes_development_folder() -> None:
    text = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    assert "exclude_docs: |\n  development/" in text.replace("\r\n", "\n")


def test_adr_dir_points_at_adr_folder() -> None:
    assert (ROOT / ".adr-dir").read_text(encoding="utf-8").strip() == "docs/development/adr"


def test_claude_md_imports_agents_md() -> None:
    assert (ROOT / "CLAUDE.md").read_text(encoding="utf-8").strip() == "@AGENTS.md"


def test_agents_md_documents_dev_docs_paths() -> None:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "## Development docs location" in text
    assert "`docs/development/SPEC.md`" in text
    assert "You may edit and add MkDocs pages" in text


def test_hook_settings_register_guard_script() -> None:
    settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    (entry,) = settings["hooks"]["PreToolUse"]
    assert entry["matcher"] == "Write|Edit|MultiEdit"
    assert "guard_docs.py" in entry["hooks"][0]["command"]
    assert (ROOT / ".claude" / "hooks" / "guard_docs.py").is_file()
