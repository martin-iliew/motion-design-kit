---
description: Audit and automatically modernize HTML, React, Vue, Svelte, or related frontend files. Single files are fixed inline; multiple files are processed together when the feature spans markup, styles, or helpers. Optional leading mode syntax: mode: fast|balanced|premium. Default: balanced.
argument-hint: "mode: premium path/to/file.html" or "path/to/file.html path/to/component.tsx path/to/styles.css"
allowed-tools: Read, Edit, WebSearch, WebFetch, Agent, Bash
---

Use the `Skill` tool to invoke the `motion-upgrade` skill, passing "$ARGUMENTS" as the file(s) to upgrade. If no leading `mode:` prefix is present, the skill defaults to `balanced`.
