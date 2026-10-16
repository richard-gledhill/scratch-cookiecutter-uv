# Development docs

Everything about *building* this project lives here. This folder is excluded from the MkDocs site
(`exclude_docs` in `mkdocs.yml`), so nothing in it is published. Anything users should read belongs in
the MkDocs part of `docs/`, one level up.

| Path | What goes there |
|---|---|
| [`CONSTRAINTS.md`](CONSTRAINTS.md) | The measured, tool-enforced quality bar. Project-wide and long-lived. Read before writing code; never weaken it to make a change pass. Protected: the guard hook blocks agent edits, so the owner changes it. |
| [`conventions.md`](conventions.md) | The judgement-based style guide. Read before writing code. Protected: the guard hook blocks agent edits, so the owner changes it. |
| [`requirements/`](requirements/README.md) | PRDs, product briefs and user stories. Human-owned and long-lived; the guard hook blocks agent edits to existing docs. |
| [`plan/`](plan/README.md) | The current piece of work: `SPEC.md`, `plan.md` and `todo.md`, plus an `archive/` of finished work. |
| [`rfcs/`](rfcs/README.md) | A pointer only: RFCs are GitHub issues labelled `rfc` on the project board. |
| [`adr/`](adr/README.md) | Architecture decision records, `ADR-NNN-title.md`, sequential, never deleted. |
| [`architecture/`](architecture/README.md) | Overview, diagrams, data model. |
| [`testing/`](testing/README.md) | Test strategy and plans. |
| [`operations/`](operations/README.md) | Runbooks, rollback plans, postmortems. |

## From requirement to shipped work

1. **Requirement**: a person writes `requirements/<feature>-prd.md` with `Status: Draft`, and marks it `Accepted`
   when it is ready to build.
2. **RFC**: a design question that needs discussion is raised as an `rfc` issue.
3. **ADR**: a decided RFC, or any decision that outlives the work, is recorded in `adr/` and linked both ways with
   its issue.
4. **Plan**: write `plan/SPEC.md` (the `/spec` workflow creates it), linking its requirement, then `plan.md` and
   `todo.md`. Build against them.
5. **Archive**: when the work ships, move the spec, plan and todo together into `plan/archive/YYYY-MM-<feature>/` and
   set the requirement's status to `Done`. Start the next piece of work with a fresh `SPEC.md`.

`plan.md` and `todo.md` do not exist until a workflow creates them. See [AGENTS.md](../../AGENTS.md) for the paths
agents must use.
