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

- Constraints: `docs/development/constraints.md` — project-wide; read before writing code; do not weaken it to make a change pass
- Conventions: `docs/development/conventions.md` — the style guide. Don't change `conventions.md` or `constraints.md`
  without asking, and never to make them match code you just wrote. The hook blocks edits to both once they exist;
  describe the change you want in your summary and let the user make or approve it
- Requirements (PRDs, product briefs, user stories) live in `docs/development/requirements/`. Don't edit an existing
  requirements doc without asking. Create a new one only when the user asks.
- Spec: `docs/development/plan/SPEC.md` (not root SPEC.md)
- Plan: `docs/development/plan/plan.md`
- Task list: `docs/development/plan/todo.md`
- SPEC.md is the technical spec for the current work. Link to its source in `requirements/`, and reference
  `conventions.md`, `constraints.md` and `testing/` instead of restating them. Record only what's specific to this work.
- ADRs: `docs/development/adr/`, format `ADR-NNN-title.md`; continue the existing sequence
- When work ships, move `SPEC.md`, `plan.md` and `todo.md` together into
  `docs/development/plan/archive/<YYYY-MM-feature>/`, and update the requirement's Status.
  If `plan/` already has an unfinished plan for different work, stop and ask.
- RFCs: if the project uses a GitHub Project, GitHub Issues or another tracker for RFCs, that tracker is the single
  source of truth. Don't create or copy RFCs into `docs/development/rfcs/`; refer to the issue instead. When an RFC is
  decided, record it as an ADR and link the ADR and issue both ways. Use `rfcs/` files only if no tracker exists;
  [`docs/development/rfcs/README.md`](docs/development/rfcs/README.md) says which mode the project uses and gives the
  local `RFC-NNN-title.md` format.
- Never write development docs into the MkDocs content under `docs/` outside `development/`
- You may edit and add MkDocs pages (user-facing docs under `docs/`, outside `development/`) and `mkdocs.yml`
  when a change needs it. Add new pages to `nav:` and run `make docs-test` to check the site still builds.
- A hook enforces the development paths and protects `conventions.md`, `constraints.md` and existing
  files in `requirements/`. If a write is blocked,
  follow the redirect in the hook's message, or ask the user if the file is protected.

## Tracking work

This repository is tied only to the `scratch-cookiecutter-uv` project. Don't link to, reference, or create issues or
pull requests in any other repository, including any cookiecutter-uv fork or template.

- Track work as GitHub issues in this repository. Label each one `issue`, `bugfix` or `rfc` (a request for change,
  discussed before it is built).
- Create, edit, close or move issues and project items only when the user asks.
- A decided `rfc` is recorded as an ADR in `docs/development/adr/`; link the issue and the ADR to each other.
- Reference the issue in commits and PRs (`Closes #N`).

### When a GitHub Project is linked to the repository

This repository's project is the user's GitHub project 6, `scratch-cookiecutter-uv`
(<https://github.com/users/richard-gledhill/projects/6>). Check it is still linked with
`gh repo view --json projectsV2`; if no project is linked, skip this section.

- **Access.** `gh project` commands need the `project` token scope (`gh auth status` lists it). If it is missing, ask
  the user to run `gh auth refresh -s project`; never handle the token yourself.
- **Don't change the project's setup.** Leave its fields, field options and views alone. Setting a value on an item
  (Status, Iteration, Priority) is fine; adding or renaming a field or option is not.
- **Every new issue goes on the board.** After `gh issue create`, add it with
  `gh project item-add 6 --owner richard-gledhill --url <issue url> --format json`, then set its Status to `Backlog`
  explicitly with `gh project item-edit` (look up the field and option IDs with
  `gh project field-list 6 --owner richard-gledhill --format json`). Don't rely on a default status.
- **Built-in workflows are on**: auto-add to project, item added, item closed, auto-close issue, pull request
  linked, pull request merged. Still add each new issue and set `Backlog` yourself (`item-add` returns the existing
  item if auto-add got there first), but leave the rest of the status changes the workflows make to them.
- **Backlog vs sprint.** New issues belong in the backlog: Status `Backlog`, no Iteration, no Priority. The
  "Prioritized backlog" board shows them. "Current iteration" and "Next iteration" are sprint boards filtered to
  `iteration:@current` and `iteration:@next`, so an issue appears there only once the user plans it by setting its
  Iteration. If the user can't see new items, explain the filter; don't set an iteration to make them appear.
- **Planning only when asked.** Setting Iteration, Priority or `Ready` is the user's call, and so is rolling
  unfinished work over to the next iteration. When asked, set Iteration with
  `gh project item-edit --iteration-id` and Priority with `--single-select-option-id`, taking the IDs from
  `gh project field-list 6 --owner richard-gledhill --format json`.
- **Status follows the work**, for an issue the user has asked you to work on: set `In progress` when you start and
  `In review` when its PR is open. Don't set `Done` by hand: merging a PR with `Closes #N` closes the issue and the
  workflow sets `Done`. After the merge, check the status and fix it only if the workflow didn't.
- **Verify, then report.** `gh project` calls occasionally fail or lag. Retry a failed call, check the result with
  `gh project item-list 6 --owner richard-gledhill --format json` (an item can take a few seconds to appear), and
  list the issue numbers, labels and status you set.

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

- The quality bar, including what never to silence or weaken, is in
  [`docs/development/constraints.md`](docs/development/constraints.md). Fix the code, not the check.
- If you believe a test is wrong, explain why in your final response before changing it.
- If a failure persists that you can't fix, or that existed before your change, or is caused by the
  environment (network, missing tools), stop. Don't report the task as complete. Say what failed and why.

### Final report

List each verification command you ran with pass/fail. For any failure, include the relevant output.
Don't report a command as passing unless you ran it after your last change.
