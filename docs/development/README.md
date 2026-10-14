# Development docs

Everything about *building* this project lives here. This folder is excluded from the MkDocs site
(`exclude_docs` in `mkdocs.yml`), so nothing in it is published. Anything users should read belongs in
the MkDocs part of `docs/`, one level up.

| Path | What goes there |
|---|---|
| `CONSTRAINTS.md` | The quality bar. Project-wide and long-lived. Read before writing code; never weaken it to make a change pass. Created by the agent workflows, then protected: the guard hook blocks agent edits once it exists. |
| `conventions.md` | The judgement-based style guide. Read before writing code. Protected: the guard hook blocks agent edits, so the owner changes it. |
| [`build-plan/`](build-plan/README.md) | The current piece of work: `SPEC.md`, `plan.md` and `todo.md`, plus an `archive/` of finished work. |
| [`rfcs/`](rfcs/README.md) | Design proposals, before a decision is made. Raised as `rfc` issues; long ones live here. |
| [`adr/`](adr/README.md) | Architecture decision records, `ADR-NNN-title.md`, sequential, never deleted. |
| [`architecture/`](architecture/README.md) | Overview, diagrams, data model. |
| [`testing/`](testing/README.md) | Test strategy and plans. |
| [`operations/`](operations/README.md) | Runbooks, rollback plans, postmortems. |

## Build plan lifecycle

1. Write `build-plan/SPEC.md` for the work (the `/spec` workflow creates it), then `plan.md` and `todo.md`.
2. Build against them. Decisions that outlive the work become ADRs in `adr/`.
3. When the work ships, move the spec, plan and todo together into `build-plan/archive/YYYY-MM-<name>/`.
4. Start the next piece of work with a fresh `SPEC.md`.

`CONSTRAINTS.md`, `plan.md` and `todo.md` do not exist until a workflow creates them. See
[AGENTS.md](../../AGENTS.md) for the paths agents must use.
