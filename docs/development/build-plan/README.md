# Build plan

The current piece of work: what is being built, how, and what is left. One piece of work at a time.

| File | What it is |
|---|---|
| `SPEC.md` | The spec for the current piece of work. Created by the `/spec` workflow. |
| `plan.md` | The implementation plan for `SPEC.md`. Created by agents. |
| `todo.md` | The task list for the plan. Created by agents. Use an issue tracker instead, or gitignore it, if you don't want task state committed. |
| [`archive/`](archive/README.md) | Finished work, one folder each. |

`CONSTRAINTS.md` is not here: it is project-wide and long-lived, so it sits one level up in
`docs/development/`.

## Lifecycle

1. Write `SPEC.md` (the `/spec` workflow creates it), then `plan.md` and `todo.md`.
2. Build against them. Decisions that outlive the work become ADRs in [`../adr/`](../adr/README.md).
3. When the work ships, move `SPEC.md`, `plan.md` and `todo.md` together into
   `archive/YYYY-MM-<short-name>/` (for example `archive/2026-10-auth-flow/`).
4. Start the next piece of work with a fresh `SPEC.md`.
