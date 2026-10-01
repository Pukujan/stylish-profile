# Current Repository Checkpoint

<!-- continuity:current {"active_task":"SP-0003","active_task_file":"tasks/TASK-SP-0003-voice-notes-play-and-avatar.md","protocol_version":"0.1.0-draft","schema":"project-continuity.current.v1"} -->

This is an as-of projection; live GitHub issues own progression. Link the owning leaf, parent ancestry and dependencies for active work.

## Program state

Phase: bootstrap.

## Completed

- continuity protocol initialized.
- SP-0001: the profile page shipped, with the illustrations, charts, and the written record.
- SP-0002: the projects table, a spoken note per project, four-frame animations, and a derived dark variant of every image.

## Active

- SP-0003: make every voice note open and play, keep the derived dark variants from going stale, and give the account an avatar drawn as the same character as the page.

## Queued

- Upload the avatar to the GitHub account, which is a web-UI action the REST API does not expose.
- Delete the two throwaway probe repositories, which needs the `delete_repo` scope on the `gh` token.

## Blockers

None known.

## Next atomic action

Publish SP-0003 through the required `gates` check, mirror the profile page into
`Pukujan/Pukujan`, and append the receipt to issue #1.
