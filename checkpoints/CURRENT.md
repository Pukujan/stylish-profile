# Current Repository Checkpoint

<!-- continuity:current {"active_task":"SP-0004","active_task_file":"tasks/TASK-SP-0004-dark-illustrations-and-page-voice.md","protocol_version":"0.1.0-draft","schema":"project-continuity.current.v1"} -->

This is an as-of projection; live GitHub issues own progression. Link the owning leaf, parent ancestry and dependencies for active work.

## Program state

Phase: bootstrap.

## Completed

- continuity protocol initialized.
- SP-0001: the profile page shipped, with the illustrations, charts, and the written record.
- SP-0002: the projects table, a spoken note per project, four-frame animations, and a derived dark variant of every image.
- SP-0003: every voice note opens and plays, the dark variants cannot go stale without failing the gate, and the account has an avatar drawn as the same character as the page.

## Active

- SP-0004: make the dark illustrations look like the drawings they came from, and rewrite the profile page so a visitor is welcomed instead of handed an audit trail.

## Queued

- Upload the avatar to the GitHub account, which is a web-UI action the REST API does not expose.
- Delete the two throwaway probe repositories, which needs the `delete_repo` scope on the `gh` token.

## Blockers

None known.

## Next atomic action

Open the pull request for SP-0004, let the required `gates` check run, merge it
automatically, then mirror the profile page into `Pukujan/Pukujan` and append a
receipt to issue #1.
