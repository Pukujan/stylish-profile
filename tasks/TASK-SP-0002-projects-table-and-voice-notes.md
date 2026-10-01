# TASK-SP-0002 — Projects Table And Voice Notes

<!-- continuity:task {"acceptance": ["the projects section of profile/README.md opens on a table whose first column links each project to its repository and whose last column links that project's spoken note", "the long description of each project sits behind a dropdown, so the section no longer opens on a wall of prose", "the tour page plays all nine voice notes with a real player, and each project's note sits beside that project", "scripts/generate_voice_notes.py --check confirms every committed clip matches its recorded byte count, its manifest SHA-256 and its transcript, and the required gates job runs that check", "every illustration, the hero, the four charts and the two habit animations render exactly one image per figure in each of the four theme states, with no wrong-mode leakage", "the tour page leads with the dark palette and switches on prefers-color-scheme"], "depends_on": ["SP-0001"], "goal": "Open the profile page's projects section on a table with a spoken note per project, animate every image, and derive a dark variant of each", "id": "SP-0002", "issue_url": "https://github.com/Pukujan/stylish-profile/issues/5", "next_action": "push the task branch, let the gates job report, and confirm auto-merge lands the squash without an approval", "owner": "Pukujan", "priority": "P1", "protocol_version": "0.1.0-draft", "schema": "project-continuity.task.v1", "status": "active", "why": "The current-projects section is a wall of prose that buries the thing a reader came for, and the page only offered a light palette and still images"} -->

- Status: active
- Owner: Pukujan
- Priority: P1
- Depends on: SP-0001

## Goal

Open the profile page's projects section on a table with a spoken note per project, animate every image, and derive a dark variant of each

## Why

The current-projects section is a wall of prose that buries the thing a reader came for, and the page only offered a light palette and still images

## Allowed files

- define bounded paths before implementation.

## Human outcome

Describe what becomes easier, safer, clearer, or possible when this task is complete.

## Scope and boundaries

- In scope:
- Out of scope:
- Dependencies/uncertainty:

## Acceptance criteria

- [ ] the projects section of profile/README.md opens on a table whose first column links each project to its repository and whose last column links that project's spoken note
- [ ] the long description of each project sits behind a dropdown, so the section no longer opens on a wall of prose
- [ ] the tour page plays all nine voice notes with a real player, and each project's note sits beside that project
- [ ] scripts/generate_voice_notes.py --check confirms every committed clip matches its recorded byte count, its manifest SHA-256 and its transcript, and the required gates job runs that check
- [ ] every illustration, the hero, the four charts and the two habit animations render exactly one image per figure in each of the four theme states, with no wrong-mode leakage
- [ ] the tour page leads with the dark palette and switches on prefers-color-scheme

## Evidence and sources

Link repository state at a revision and cite external factual claims directly. Record commands and results for claims that need verification.

## Reproduction details (only when needed)

Starting revision, material inputs/configuration, runtime, exact command or prompt, observed result, and limitations.

## Related records

- Required leaf owning issue, parent ancestry and dependencies (or explicitly none):
- Primary writer / branch / source issue revision / as-of status:
- Related PR/CI evidence and push receipt (request ID / SHA):

## Checkpoint log

No checkpoints yet.

## Handoff

Read PROJECT → CURRENT → this task → minimum relevant spec. Checkpoint before stopping.
