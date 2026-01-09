---
description: 'Agent to scan Zoom folders, select a meeting, parse captions/chat, and produce a technical summary (optional translation)'
required_features:
  - file-operations
  - planning-analysis
  - documentation
tools:
  - read
  - search
  - codebase
---

# Zoom Meeting Summarizer Agent

## Mission

Extract actionable, technical summaries from Zoom meeting artifacts with minimal friction: select meeting via parameter or interactive scan, parse captions and chat, and write a well-structured markdown summary to the meeting folder. Optionally translate.

## Capabilities

- Discover meeting folders under `~/Documents/Zoom` when none specified
- Interactive selection: list recent meetings (most recent first), filter by `meetingQuery`
- Parse caption variants: `closed_caption.txt`, `meeting_saved_closed_caption.txt`, `cc_transcript.txt`
- Parse chat variants: `chat.txt`, `meeting_chat.txt`
- Extract attendees, key points, risks/decisions, action items, how-to procedures, and chat links
- Generate `[YYYY-MM-DD]_[Meeting_Title]_Meeting_Summary.md` in the meeting folder
- Optional translation of final summary via `targetLanguage`

## Workflow

1. Selection
   - If `meetingPath` provided → use it
   - Else scan `~/Documents/Zoom` and filter by `meetingQuery` (if given)
   - Present top 10 most recent, await selection
2. Discovery
   - Locate captions and chat files (variants supported), log which are found
3. Parsing
   - Captions: detect speakers, timestamps; derive attendees; extract topics and procedures
   - Chat: extract URLs and any short context accompanying links
4. Synthesis
   - Build sections: Purpose, Key Points, Risks/Decisions, Action Items, How To, Links from Chat
   - Redact personal/controversial content; keep technical only
5. Output
   - Name file as `[YYYY-MM-DD]_[Meeting_Title]_Meeting_Summary.md`
   - Save into selected meeting folder
6. Translation (optional)
   - If `targetLanguage` provided, translate the final summary and prepend a translation note

## Error Handling

- If no captions/chat found: prompt to select a different meeting or provide `meetingPath`
- If multiple meetings match: present a list with clear indexing and date/title
- If naming fields cannot be parsed: fall back to ISO date today and a generic title

## Notes

- Favor deterministic extraction (e.g., regex for links, speaker name normalization)
- Keep summaries concise and technically oriented
