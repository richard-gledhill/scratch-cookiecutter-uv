# Development docs

Everything about *building* this project lives here. This folder is excluded from the MkDocs site
(`exclude_docs` in `mkdocs.yml`), so nothing in it is published. Anything users should read belongs in
the MkDocs part of `docs/`, one level up.

| Path | What goes there |
|---|---|
| `SPEC.md` | The current feature or project spec. Created by the agent workflows; holds one feature at a time. |
| `CONSTRAINTS.md` | The quality bar. Read before writing code; never weaken it to make a change pass. |
| [`requirements/`](requirements/README.md) | Archived specs, one per shipped feature. |
| [`rfcs/`](rfcs/README.md) | Design proposals, before a decision is made. |
| [`adr/`](adr/README.md) | Architecture decision records, `ADR-NNN-title.md`, sequential, never deleted. |
| [`architecture/`](architecture/README.md) | Overview, diagrams, data model. |
| [`testing/`](testing/README.md) | Test strategy and plans. |
| [`operations/`](operations/README.md) | Runbooks, rollback plans, postmortems. |
| [`tasks/`](tasks/README.md) | `plan.md` and `todo.md`, created by agents. |

## SPEC.md lifecycle

1. Write `docs/development/SPEC.md` for the feature (the `/spec` workflow creates it).
2. Plan and build against it. Decisions that outlive the feature become ADRs in `adr/`.
3. When the feature ships, move the spec to `requirements/<feature>.md`.
4. Start the next feature with a fresh `SPEC.md`.

`SPEC.md` and `CONSTRAINTS.md` do not exist until a workflow creates them. See [AGENTS.md](../../AGENTS.md)
for the paths agents must use.
