---
description: Audit one or more files for animation issues, then automatically fix all CRITICAL and WARNING items. Single files are fixed inline (fast path — no sub-agent). Multiple files are processed in true parallel with one agent per file to prevent race conditions.
argument-hint: path/to/file.html [path/to/another.js ...]
allowed-tools: Read, Edit, WebSearch, WebFetch, Agent, Bash
---

Use the `Skill` tool to invoke the `motion-enhance` skill, passing "$ARGUMENTS" as the file(s) to enhance.
