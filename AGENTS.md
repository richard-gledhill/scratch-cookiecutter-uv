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
- Conventions: `docs/development/conventions.md` — the style guide. Don't change `conventions.md` or `CONSTRAINTS.md`
  without asking, and never to make them match code you just wrote
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

Read [`docs/development/conventions.md`](docs/development/conventions.md) before writing code.

In `SPEC.md`, reference `docs/development/conventions.md` instead of restating code style. Only record
feature-specific deviations.

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
