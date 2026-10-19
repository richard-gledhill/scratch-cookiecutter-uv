# Request for Change

An RFC is a design question or proposed change that is discussed before it is built. RFCs live in exactly one
place: a tracker, or this folder. Never both, so there is a single source of truth.

## Which mode this project uses

**Tracker** (current). RFCs are GitHub issues in this repository labelled `rfc`, on the
[project board](https://github.com/users/richard-gledhill/projects/6). No RFC files are kept in this folder; refer to
the issue instead.

To switch modes, update this section and the `RFCs` line in [AGENTS.md](../../AGENTS.md) together.

## Tracker mode

Use this when the project has a GitHub Project, GitHub Issues or another tracker.

- Raise each RFC as an issue labelled `rfc`. Discussion happens on the issue.
- Don't create or copy RFC files into this folder.
- Once decided, record the outcome as an ADR in [`../adr/`](../adr/README.md) and link the ADR and the issue to
  each other. Close the issue.

## Local mode

Use this when the project has no tracker.

- One file per RFC, named `RFC-NNN-title.md` (for example `RFC-001-plugin-loading.md`). Numbers are sequential:
  continue the existing sequence. RFCs are never deleted; a rejected or withdrawn RFC keeps its file and status.
- Start each file with a status line, then the sections below:

  ```markdown
  # RFC-NNN: Title

  Status: Draft | Discussion | Accepted | Rejected | Withdrawn

  ## Problem
  ## Proposal
  ## Alternatives
  ## Open questions
  ## Decision
  ```

- Once decided, set the status, record the outcome as an ADR in [`../adr/`](../adr/README.md), and link the ADR
  and the RFC file to each other.
