# AGENTS.md

This file provides guidance to AI Agents and Claude Code (claude.ai/code) when working with code in this repository.

## What this is

<One paragraph: what the project does, who it is for, and its key guarantees or constraints.>
Full design rationale: [docs/development/architecture/](docs/development/architecture/README.md).
Domain language (<key terms>) is defined in [CONTEXT.md](CONTEXT.md) — use those terms.

**Before assuming a described feature is fully wired, check
[docs/development/<roadmap>.md](docs/development/<roadmap>.md)** — it tracks what's
actually implemented vs. still partial or deferred. See
[docs/development/README.md](docs/development/README.md) for the full doc index.

## Development docs location

All development documentation lives under `docs/development/`, which is excluded from the MkDocs site.
These paths override any default paths in skills or commands:

- Constraints: `docs/development/CONSTRAINTS.md` — project-wide; read before writing code; do not weaken it to make a change pass
- Spec: `docs/development/build-plan/SPEC.md` (not root SPEC.md)
- Plan: `docs/development/build-plan/plan.md`
- Task list: `docs/development/build-plan/todo.md`
- ADRs: `docs/development/adr/`, format `ADR-NNN-title.md`; continue the existing sequence
- When the work ships, move `SPEC.md`, `plan.md` and `todo.md` together into
  `docs/development/build-plan/archive/YYYY-MM-<short-name>/` before starting a new `SPEC.md`
- Never write development docs into the MkDocs content under `docs/` outside `development/`
- You may edit and add MkDocs pages (user-facing docs under `docs/`, outside `development/`) and `mkdocs.yml`
  when a change needs it. Add new pages to `nav:` and run `make docs-test` to check the site still builds.
- A hook enforces the development paths. If a write is blocked, follow the redirect in the hook's message.

## Commands

```bash
make install    # uv sync + install pre-commit hooks
make check      # uv lock --locked, pre-commit run -a, <type checker>, <dependency checker>
make test       # pytest --doctest-modules --cov --cov-report=term-missing
make docs       # <docs tool> serve
make <target>   # <project-specific target, e.g. regenerate a schema or diagram>
make build      # build the release artefacts into dist/ and check them
```

Single test / narrower run:

```bash
uv run pytest tests/<path>/test_<module>.py -k some_case
```

<If a uv workspace:> run one package's own checks (e.g. what `make check` does per-package for deptry):

```bash
cd packages/<package> && uv run deptry src
```

`tox.ini` runs the same pytest + type-check pass across Python <min>–<max>; `make check`/`make test` on
your local interpreter are what you want day to day.

## Architecture

<Layout in one sentence: single package, or a uv workspace and how the packages depend on each other.>

```
<src/package/>     # <what lives here>
<tests/>           # <how tests mirror the source layout>
```

**Names.** <Distribution vs import names, namespace packages, and any import rule agents must follow.>

<Tooling config that depends on the layout: coverage, mypy, deptry.>

### <Main flow or pipeline (entry point)>

1. **<Step / component>**: <what it does and the one thing to know about it.>
2. **<Step / component>**: <...>

### <Other major components>

- **`<module>`**: <what it owns, and what not to reintroduce.>

### Config resolution

<Where config lives, how defaults and overrides merge, and where each setting is documented.>

### <Subsystem, e.g. parsers, adapters, plugins>

<How it is structured, its public entry points, and how failures are handled.>

## Conventions

**Design**
- Prefer deep modules: a small interface with a lot of behaviour behind it.
- Before adding a module, apply the deletion test: if removing it would just move one line into its callers,
  don't add it.
- Locality: each concern lives in one place, so a fix is made once.
- Add a seam (a `Protocol` or swappable adapter) only where something actually varies. One implementation is not a seam.
- Test through the interface and fake at the seams (<the swappable parts, e.g. external services>). If a test needs to reach past the
  interface, the module is probably the wrong shape.

**Code**
- Docstrings: Google style (`Args:`/`Returns:`/`Raises:`) — `mkdocstrings` renders them for the
  published docs.
- Use the [CONTEXT.md](CONTEXT.md) terms in code, docs and commits; add a term there when you
  introduce a domain concept.
- Name a module's logger `_logger = logging.getLogger(__name__)`, among the module's constants below the imports.
  The underscore marks it private: never import another module's logger, so a record is always attributed to the
  module that emitted it. Only `<entry-point package>` configures logging (handlers and levels); `<library package>`
  just emits, and its `__init__.py` adds a `NullHandler` to the package logger and nothing else.
- `ruff` config lives only in the root `pyproject.toml`<; per-package `pyproject.toml` files carry
  just their own dependencies, if a workspace>. mypy is <strict> and covers `<source path>` (not tests).
- Code must import and type-check on <platforms, e.g. Linux (CI) and Windows>. Some names exist on one only
  (<examples>). Write such constants out, import platform modules inside the function that uses them, and guard the
  body with `if sys.platform == "<platform>":` so mypy skips it elsewhere. `make check` runs mypy for each
  platform for this reason.

**Module layout**
- Order a module like this, omitting what it doesn't have:
  1. Module docstring.
  2. Imports: `from __future__`, then standard library, third-party, local (`ruff` sorts them).
  3. Module dunders (`__all__`, `__version__`). These go after the imports, unlike PEP 8, which puts them
     before; it matches `<example_module>.py` and `<example_package>/__init__.py`.
  4. Constants and types: constants, type aliases, `TypeVar`s, `Protocol`s and plain data models (dataclasses,
     Pydantic). Code further down uses them in signatures.
  5. Errors: custom exceptions.
  6. Public API: the functions and classes other modules import. High up, so a reader sees what the module offers first.
  7. Helpers: `_`-prefixed, module-private functions, kept last as implementation detail.
- Order matters only for names used at import time (constants, decorators, default arguments, class bodies):
  those must be defined above their use. A function body can call a helper defined below it.
- In a module of about 150+ lines with at least three of sections 4-7, wrap each in `# region <name>` ...
  `# endregion` (PyCharm and VS Code fold them), using exactly these names: `Constants and types`, `Errors`,
  `Public API`, `Helpers`. Shorter modules get no regions. Don't use `# ---` divider comments.
- A test file mirrors its module. It opens with a `Test helpers` region (shared constants, builders, fakes,
  fixtures; a helper used by one section stays in that section). Then come regions in the module's order with
  the module's names. Inside `Public API`, nest one region per function or class under test, or per behaviour
  when one class has many tests. If the module has no regions, use one top-level region per function, class or
  behaviour. Keep a decorator (`@pytest.mark.parametrize`) with its test, never a region marker between them.

**Tests**
- Use `tmp_path`; copy `tests/<fixture dir>` for integration tests. Use fakes for external
  services: no network or <external tools> in the suite.
- Lay test files out as described under Module layout.
- Name tests `test_<subject>_<scenario>_<result>`, in the present tense:
  - `<subject>` is the function, class, command or behaviour under test (`<function>`, `<class>`,
    `<command>`), so `pytest -k` and a failure's node id say what broke.
  - Leave out articles and filler (a, an, the, is, are, can, be, that, should) and keep it to about 50 characters
    after `test_`.
  - Leave out `<result>` when the scenario already implies it (`test_<subject>_<scenario>`).
  - Put anything that doesn't fit in a short comment in the test body. A parametrized test's name describes
    the whole family.
  - Don't reuse a name within a file; pytest runs only the last one.

**Docs**
- User docs track the <CLI / public interface>: any change to a <command, option or public API>, or its status in
  `docs/development/<roadmap>.md`, must also update [docs/<user guide>.md](docs/<user guide>.md) and the Usage
  section of [README.md](README.md#usage).
- <Generated docs, e.g. a CLI reference or schema> are generated from <source>: run `make <target>` after changing
  <the source>. A test fails if the committed file is stale.
- `README.md` and `docs/<user guide>.md` are published; `docs/development/` is not, so link to it
  by GitHub URL.
- Record a deferred or future item once, and link to it. A gap or small postponed item goes in
  `docs/development/<roadmap>.md`; a feature outside the current scope, or code removed from it, goes in
  `docs/development/<backlog>.md`.
- After a rename or behaviour change, grep the docs for the old name or number.
  `architecture/`, `<roadmap>.md` and any generated diagram go stale first. <Regenerate diagrams with
  `make <target>` when imports change.>

**Git**
- Branches follow `<type>/<short-description>`, `<type>` being a Conventional Commits type
  (`feat`/`feature`, `fix`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`,
  `revert`) — e.g. `feature/config-command`, `chore/refactor-configs`. Checked, advisory-only,
  by `<.github/workflows/branch-naming.yml, if present>`. One concern per branch, from an up-to-date `main`.
- Commit subjects use Conventional Commits (`feat:` or `feature:`, `fix:`, `refactor:`, `docs:`, `test:`,
  `chore:`): <the changelog is generated from them>.
- Stage by explicit path, never `git add <dir>` or `-A`; untracked local files get swept in.
- `make check` only sees tracked files: `git add -N` new files first, or they go unchecked.
- Local scratch files go in `<.temp/>` (gitignored).

## Verifying your work

Verify any change to code, tests, config, or dependencies before reporting the task complete.
Docs-only changes and questions don't need the full suite.

### While developing: targeted checks

Run the narrowest check that exercises what you changed, e.g.:
```bash
uv run pytest tests/<path>/test_<module>.py -k <test_name>
uv run <dependency checker> <source path>
```
These are for fast iteration; they don't replace full verification.

### Before reporting complete: full verification

```bash
make check   # uv lock --locked, pre-commit run -a, <type checker>, <dependency checker>
make test    # pytest --doctest-modules with coverage
```

- If pre-commit auto-fixes files, review the changes and rerun `make check`.
  If it still isn't clean after two reruns, stop and report.
- If `uv lock --locked` fails because you changed dependencies, run `uv lock` and include the lockfile in your change.

### Rules

- Fix the code, not the check. Never skip, delete, or weaken a test, and never silence a check:
  no `# type: ignore`, `# noqa`, `SKIP=`, `--no-verify`, or loosened <type checker>/<dependency checker>/pre-commit config,
  unless I've asked for it.
- If you believe a test is wrong, explain why in your final response before changing it.
- Add or update tests for any behavior you change.
- If a failure persists that you can't fix, or that existed before your change, or is caused by the
  environment (network, missing tools), stop. Don't report the task as complete. Say what failed and why.

### Final report

List each verification command you ran with pass/fail. For any failure, include the relevant output.
Don't report a command as passing unless you ran it after your last change.
