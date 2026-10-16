# scratch-cookiecutter-uv

[![Release](https://img.shields.io/github/v/release/richard-gledhill/scratch-cookiecutter-uv)](https://img.shields.io/github/v/release/richard-gledhill/scratch-cookiecutter-uv)
[![Build status](https://img.shields.io/github/actions/workflow/status/richard-gledhill/scratch-cookiecutter-uv/main.yml?branch=main)](https://github.com/richard-gledhill/scratch-cookiecutter-uv/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/richard-gledhill/scratch-cookiecutter-uv/branch/main/graph/badge.svg)](https://codecov.io/gh/richard-gledhill/scratch-cookiecutter-uv)
[![Commit activity](https://img.shields.io/github/commit-activity/m/richard-gledhill/scratch-cookiecutter-uv)](https://img.shields.io/github/commit-activity/m/richard-gledhill/scratch-cookiecutter-uv)
[![License](https://img.shields.io/github/license/richard-gledhill/scratch-cookiecutter-uv)](https://img.shields.io/github/license/richard-gledhill/scratch-cookiecutter-uv)

This is a scratch Python project managed with [uv](https://docs.astral.sh/uv/). The purpose of this repository is to
provide a testing ground for developing a template repository structure. It also serves as a reference for new
repositories as it extends the functionality of the base uv cookiecutter template.
It is a self-contained project: its issues, pull requests, documentation and tooling all live in this repository and
are tracked in its own
GitHub project.

The Python package (`scratch_cookiecutter_uv`) is only a placeholder. The value of the repository is its tooling,
its documentation layout, and the `AGENTS.md` and `CONTEXT.md` templates for AI coding agents.

- **Github repository**: <https://github.com/richard-gledhill/scratch-cookiecutter-uv/>
- **Documentation**: <https://richard-gledhill.github.io/scratch-cookiecutter-uv/>

___

- [Features](#features)
- [Requirements](#requirements)
- [Development](#development)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

___

## Features

- Dependency and environment management with uv, with a committed `uv.lock`.
- Formatting and linting with ruff, static type checking with mypy, and unused-dependency checks with deptry, all run
  through pre-commit.
- Tests with pytest, run across Python versions with tox.
- Documentation site built with MkDocs Material and mkdocstrings.
- GitHub Actions workflows for checks, tests, docs and releases.
- Development docs under `docs/development/` (constraints, requirements, plan, ADRs, RFCs, architecture, testing and operations), excluded
  from the published site.
- `AGENTS.md` and `CONTEXT.md` templates for AI coding agents, with `CLAUDE.md` importing `AGENTS.md`.
- A Claude Code hook (`.claude/hooks/guard_docs.py`) that keeps spec, constraints and task files under
  `docs/development/` and blocks agent edits to `conventions.md` and `constraints.md`.

## Requirements

- Python 3.11 or later. `.python-version` pins development to 3.11, the minimum supported version, so `uv sync` and
  `uv run` use it (uv downloads it if it isn't installed). `tox` and CI still test 3.11 to 3.14.
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Git](https://git-scm.com/)
- `make` to run the shortcuts below. Windows doesn't ship it, so run the commands each target wraps (see the
  `Makefile`) or install it separately.

## Development

Install the environment and the pre-commit hooks:

```bash
make install
```

Day-to-day commands:

```bash
make check       # lock file consistency, pre-commit hooks, mypy, deptry
make test        # pytest, including doctests
make docs        # build and serve the documentation locally
make docs-test   # check the documentation builds without warnings or errors
make build       # build the sdist and wheel into dist/
```

Run `make` with no arguments to list every target.

## Testing

```bash
make test
```

Run a single test or a narrower selection:

```bash
uv run python -m pytest tests/test_foo.py -k some_case
```

`tox.ini` runs the same tests across the supported Python versions (3.10 to 3.14), and the GitHub Actions workflow in
`.github/workflows/main.yml` does the same on every pull request and push to `main`.

## Project Structure

```
├── .claude/              # Claude Code settings and the guard_docs.py hook
├── .github/              # GitHub Actions workflows and the Python setup action
├── docs/
│   ├── index.md          # MkDocs site content (published)
│   ├── modules.md
│   └── development/      # development docs, excluded from MkDocs
├── src/
│   └── scratch_cookiecutter_uv/
├── tests/
├── AGENTS.md             # rules for AI coding agents
├── CLAUDE.md             # imports AGENTS.md
├── CONTEXT.md            # domain language
├── CONTRIBUTING.md
├── LICENSE
├── Makefile
├── mkdocs.yml
├── pyproject.toml
└── tox.ini
```

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](https://github.com/richard-gledhill/scratch-cookiecutter-uv/blob/main/CONTRIBUTING.md) for how to report bugs, suggest features and submit
pull requests.

Work is tracked as GitHub issues in this repository, labelled `issue`, `bugfix` or `rfc` (a request for change,
discussed before it is built).

And if you are so inclined or use this for commercial work you can
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/richardgledhill)

## License

Released under the MIT License. See [LICENSE](https://github.com/richard-gledhill/scratch-cookiecutter-uv/blob/main/LICENSE) for the full text.

---

Repository initiated with [osprey-oss/cookiecutter-uv](https://github.com/osprey-oss/cookiecutter-uv).
