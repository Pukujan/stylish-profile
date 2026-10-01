# Current Repository Checkpoint

<!-- continuity:current {"active_task":"SP-0006","active_task_file":"tasks/TASK-SP-0006-records-follow-through.md","protocol_version":"0.1.0-draft","schema":"project-continuity.current.v1"} -->

This is an as-of projection; live GitHub issues own progression. Link the owning leaf, parent ancestry and dependencies for active work.

## Program state

Phase: bootstrap.

## Completed

- continuity protocol initialized.
- SP-0001: the profile page shipped, with the illustrations, charts, and the written record.
- SP-0002: the projects table, a spoken note per project, four-frame animations, and a derived dark variant of every image.
- SP-0003: every voice note opens and plays, the dark variants cannot go stale without failing the gate, and the account has an avatar drawn as the same character as the page.
- SP-0004: the dark illustrations keep the character's own colours, and both pages introduce Pujan instead of auditing him.
- SP-0005: every content-system record matches the page it describes, and the length printed beside each voice note is checked against the clip.
  A review of the merged result found three usage strings, a divergent transcript, a stale project doc and a tracker that rewrites the charts without updating their hashes; SP-0006 carries those.

## Active

- SP-0006: make the records that still contradict the shipped page agree with it, and make the two that can drift fail a check instead of going stale quietly.

## Queued

- Re-run the tracker once the two probe repositories are gone, so the `sanitizer-probe` row leaves `profile/tracking.json`.
- Re-record `The Short Tour.mp3` and `What Is Still Being Built.mp3`, which still say three projects where the page lists four. Needs a paid Fish Audio run and the owner's approval.
- Upload the avatar to the GitHub account, which is a web-UI action the REST API does not expose.
- Delete the two throwaway probe repositories, which needs the `delete_repo` scope on the `gh` token.

## Blockers

None known.

## Next atomic action

Open the SP-0006 pull request against `main`, let `gates` run, and merge it;
then record the merge commit in the task file and close the task out.
