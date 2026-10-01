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

### 2026-10-01 08:29:20 UTC — omp@windows-workstation

<!-- continuity:checkpoint {"agent":"omp@windows-workstation","blocked":[],"changed":["profile/README.md, docs/index.html, .content-system/asset-manifest.json, .content-system/voice-notes.json, .content-system/filename-legends/voice-notes.json, scripts/track_activity.py, scripts/generate_voice_notes.py, .github/workflows/gates.yml"],"completed":["the projects section opens on a table with a spoken note per project, every image is a four-frame animation, and every image has a derived dark variant"],"decisions":["an image inside a picture never swaps colour on GitHub, because the theme rule matches the anchor around a bare image; illustrations use two bare images with the theme fragment and charts use one picture with prefers-color-scheme sources, and no figure mixes the two"],"evidence":["gates passed on PR #6 and it merged as 9f1dbbc; the live profile page renders exactly 9 images in each of light and dark (18 before the fix); the live tour page serves 9 audio players that all load with real durations and no errors"],"next_action":"publish the doc and record updates that describe the shipped shape, then clean up the probe repositories","protocol_version":"0.1.0-draft","schema":"project-continuity.checkpoint.v1","task_id":"SP-0002","timestamp":"2026-10-01T08:29:20Z"} -->
<!-- continuity:checkpoint-operation {"payload_sha256":"b2c259ad5081e8671e4044e14dffffe6eaf90ee24278ad121b349432672ebe60","request_id":"2258b1b280c34c90bed8542752a98eee","schema":"project-continuity.checkpoint-operation.v1","task_id":"SP-0002"} -->

Completed:
- the projects section opens on a table with a spoken note per project, every image is a four-frame animation, and every image has a derived dark variant

Evidence:
- gates passed on PR #6 and it merged as 9f1dbbc; the live profile page renders exactly 9 images in each of light and dark (18 before the fix); the live tour page serves 9 audio players that all load with real durations and no errors

Decisions:
- an image inside a picture never swaps colour on GitHub, because the theme rule matches the anchor around a bare image; illustrations use two bare images with the theme fragment and charts use one picture with prefers-color-scheme sources, and no figure mixes the two

Changed:
- profile/README.md, docs/index.html, .content-system/asset-manifest.json, .content-system/voice-notes.json, .content-system/filename-legends/voice-notes.json, scripts/track_activity.py, scripts/generate_voice_notes.py, .github/workflows/gates.yml

Blocked/uncertain:
- none

Next:
- publish the doc and record updates that describe the shipped shape, then clean up the probe repositories

## Handoff

Read PROJECT → CURRENT → this task → minimum relevant spec. Checkpoint before stopping.
