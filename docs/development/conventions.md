# Conventions

The judgement-based style guide for this project. Agents read it before writing code (see [AGENTS.md](../../AGENTS.md)).

`CONSTRAINTS.md` is the measured, enforced bar (coverage, type errors, security checks). This file is the style
guide that tools can't check. A new rule belongs here if it is a judgement call, and in `CONSTRAINTS.md` if a tool
enforces it. Change either file only with the owner's approval.

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
- Use the [CONTEXT.md](../../CONTEXT.md) terms in code, docs and commits; add a term there when you
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
  `docs/development/<roadmap>.md`, must also update [docs/<user guide>.md](../<user guide>.md) and the Usage
  section of [README.md](../../README.md#usage).
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
