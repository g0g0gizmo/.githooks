---
description: Standards for summarizing Zoom meetings from captions and chat with selection and translation
applyTo: '**'
---

## Core Engineering Principles

- DRY: Use a consistent summary template across meetings
- Code Quality Goals: Clear, readable, technically accurate content
- Problem Decomposition: Separate purpose, key points, risks, actions, procedures

## Scope

Applies when working with Zoom artifacts such as `closed_caption.txt` and `chat.txt`, or when generating `[YYYY-MM-DD]_[Meeting_Title]_Meeting_Summary.md` files.

## Selection & Discovery

- Prefer explicit `meetingPath` parameter when available
- If absent, scan `~/Documents/Zoom` and list most recent meetings for selection
- Support file variants: captions (`closed_caption.txt`, `meeting_saved_closed_caption.txt`, `cc_transcript.txt`) and chat (`chat.txt`, `meeting_chat.txt`)

## Summary Requirements

- Output file name: `[YYYY-MM-DD]_[Meeting_Title]_Meeting_Summary.md`
- Sections (in order):
  - Title, Date/Time, Context
  - Attendees
  - Purpose/Reason for Meeting
  - Agenda or Key Points
  - Risks and Decisions
  - Action Items (owner, due-if-stated)
  - How To(<Subject>)
  - Links from Chat

## Content Rules

- Attendees: derive from speakers; de-duplicate; accept override param when provided
- Exclude personal/controversial chatter; keep technical/work-appropriate content only
- Extract and include all chat URLs (deduplicated), add short context when available
- For procedures, convert imperatives/sequences into ordered steps under `How To(<Subject>)`

## Translation

- If `targetLanguage` is provided, translate the final summary while preserving headings, code, and links
- Add a short note: "Translated from English to <LANG>"

## Error Handling

- Missing chat: proceed without the Links section
- Missing captions: summarize from chat context only (note reduced fidelity)
- Neither found: re-prompt for a different meeting or explicit `meetingPath`
