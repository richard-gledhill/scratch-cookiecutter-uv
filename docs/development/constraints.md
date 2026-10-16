# Constraints

The measured, tool-enforced quality bar for this project. Read it before writing code. The judgement-based style
guide is [conventions.md](conventions.md); a rule a tool checks belongs here.

Only the owner changes this file: the guard hook blocks agent edits. Never weaken it to make a change pass.

## Gates

A change is done only when both pass on a clean tree:

- `make check`: `uv lock --locked`, `pre-commit run -a` (file hygiene, `ruff check`, `ruff format`), `mypy`, and
  `deptry src`.
- `make test`: `pytest --doctest-modules`.

## Type checking

mypy covers `src` (not tests), configured in `pyproject.toml`: `disallow_untyped_defs`, `disallow_any_unimported`,
`no_implicit_optional`, `check_untyped_defs`, `warn_return_any`, `warn_unused_ignores`.

Code must import and type-check on Linux (CI) and Windows. Write platform-only constants out, import platform modules
inside the function that uses them, and guard the body with `if sys.platform == "<platform>":` so mypy skips it
elsewhere.

## Lint and security

`ruff` config lives only in the root `pyproject.toml`. Line length 120. Rule families: `YTT`, `S` (bandit security),
`B`, `A`, `C4`, `T10`, `SIM`, `I`, `C90` (complexity), `E`, `W`, `F`, `PGH`, `UP`, `RUF`, `TRY`. The only ignores are
`E501` and `E731`, plus `S101` in `tests/`.

## Never silence a check

- Fix the code, not the check.
- No `# type: ignore`, `# noqa`, `SKIP=` or `--no-verify`, and no loosening the mypy, deptry, ruff or pre-commit
  config, unless the owner asks for it.
- Never skip, delete or weaken a test.
- Add or update tests for any behaviour you change.

## Coverage

TODO: no coverage threshold is enforced yet. Set one (for example `--cov --cov-fail-under=<N>` in `make test`) and
record it here.
