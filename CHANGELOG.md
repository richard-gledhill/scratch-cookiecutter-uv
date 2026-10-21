# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and to [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

## Unreleased changes

### Feature
- ship a py.typed marker so type checkers use the package's annotations [`5ab8bce`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/5ab8bce)

### Bug Fixes
- make tox work with coverage and its own per-env venvs [`7ca9d0b`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/7ca9d0b)

### Documentation
- allow RFCs in a tracker or as local files [`96d30a3`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/96d30a3)
- :robot: changelog file generated [`2cb14ed`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/2cb14ed)
- :robot: changelog file generated [`a996284`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/a996284)
- :robot: changelog file generated [`3d34069`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/3d34069)
- add coverage reporting details to constraints.md [`75110f3`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/75110f3)
- :robot: changelog file generated [`5b1490a`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/5b1490a)
- align agent project rules with the board model and built-in workflows [`6917da2`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/6917da2)
- :robot: changelog file generated [`d34d0ac`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/d34d0ac)
- fix constraints.md link text and list markers in conventions.md [`4fef337`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/4fef337)
- lowercase constraints.md, add md naming rule, describe repo purpose [`9c30bf6`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/9c30bf6)
- rename build-plan to plan, add requirements, point RFCs at the tracker [`c57c15b`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/c57c15b)
- :robot: changelog file generated [`35fe82a`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/35fe82a)
- describe how agents work with the linked GitHub Project [`1b55244`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/1b55244)
- :robot: changelog file generated [`2b5d053`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/2b5d053)
- track work as labelled issues in project 6 and drop template-fork wording [`38625ab`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/38625ab)
- :robot: changelog file generated [`9d4b9cf`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/9d4b9cf)
- :robot: changelog file generated [`b2d22a1`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/b2d22a1)

### Build
- use uv build in make build and limit the sdist to the sources [`e38524f`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/e38524f)

### Chore
- pin the development interpreter to Python 3.11 [`f13c4c2`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/f13c4c2)
- Bump the github-actions-dependencies group across 2 directories with 6 updates [`73d442d`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/73d442d)

### Other
- Merge pull request #32 from richard-gledhill/docs/flexible-rfcs [`ed82d32`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/ed82d32)
- Merge pull request #31 from richard-gledhill/docs/update-constraints [`6d62dc3`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/6d62dc3)
- Merge pull request #30 from richard-gledhill/build/uv-build [`70889c2`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/70889c2)
- Merge pull request #29 from richard-gledhill/chore/pin-python-version [`c12f327`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/c12f327)
- Merge pull request #28 from richard-gledhill/feature/py-typed [`0e71a4a`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/0e71a4a)
- Merge pull request #27 from richard-gledhill/fix/tox-pytest-cov [`1d8ead6`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/1d8ead6)
- Merge pull request #26 from richard-gledhill/docs/project-board-workflow [`ba5d84e`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/ba5d84e)
- Merge pull request #25 from richard-gledhill/docs/plan-requirements-rfcs [`dd039d4`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/dd039d4)
- Merge pull request #24 from richard-gledhill/docs/github-project-process [`1509691`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/1509691)
- Merge pull request #8 from richard-gledhill/docs/issue-tracking [`4035b1e`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/4035b1e)
- Merge pull request #5 from richard-gledhill/dependabot/github_actions/github-actions-dependencies-c1392ceaf0 [`296247e`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/296247e)

## v0.0.1 (2026-10-14)

### Feature
- block agent edits to conventions.md and CONSTRAINTS.md [`d775d5b`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/d775d5b)

### Bug Fixes
- remove fetch-depth 0 from changelog checkout [`554c82c`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/554c82c)

### Continuous Integration
- fetch full history for changelog and fix dependabot comment [`5f3d9fd`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/5f3d9fd)
- add branch naming check, changelog generation and dependabot [`8dbf98e`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/8dbf98e)

### Documentation
- move conventions to docs/development/conventions.md [`0f34796`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/0f34796)
- add MkDocs pages for README, changelog, contributing and license [`01ea2e6`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/01ea2e6)
- expand README with features, development and structure [`4ca3ed4`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/4ca3ed4)
- consolidate tasks and specs under docs/development/build-plan [`3b1f966`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/3b1f966)
- add docs/development layout, agent rules and guard hook [`8bfab5b`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/8bfab5b)

### Test
- make protected-file hook test respect filesystem case sensitivity [`b361f51`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/b361f51)

### Chore
- raise minimum Python to 3.11 [`52d5f45`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/52d5f45)

### Other
- Merge pull request #7 from richard-gledhill/fix/changelog-checkout [`852264d`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/852264d)
- Merge pull request #6 from richard-gledhill/docs/conventions-file [`b42a0d7`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/b42a0d7)
- Merge pull request #4 from richard-gledhill/docs/mkdocs-site-pages [`cbd31a3`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/cbd31a3)
- Merge pull request #3 from richard-gledhill/docs/development-layout [`d2b03c0`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/d2b03c0)
- Merge pull request #2 from richard-gledhill/ci/conventional-commits-changelog [`44d1a4e`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/44d1a4e)
- Merge pull request #1 from richard-gledhill/chore/min-python-3.11 [`b88e2bc`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/b88e2bc)
- Fix formatting issues [`778dc0f`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/778dc0f)
- init commit [`2059d4b`](https://github.com/richard-gledhill/scratch-cookiecutter-uv/commit/2059d4b)
