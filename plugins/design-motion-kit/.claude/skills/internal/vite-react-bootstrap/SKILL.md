---
name: vite-react-bootstrap
description: >
  Internal bootstrap skill for greenfield work. It creates the base Vite React and Tailwind v4
  foundation before design-system, design, or motion implementation begins.
---

# vite-react-bootstrap

This is an internal skill. It is not a public command surface.

## Trigger

Use only when:

- the target repo does not already contain an app shell
- the user asked for greenfield project creation

## Workflow

1. Detect package manager and existing frontend tooling.
2. If the app does not exist yet, create the Vite React foundation.
3. Wire Tailwind v4 CSS-first theme loading so `brief/theme.css` can be imported later.
4. Use this vendored reference for project structure ideas:
   - `.claude/skills/vendor/anthropic/web-artifacts-builder/SKILL.md`

## Rules

- stop if project creation requires network access the environment does not allow
- keep bootstrap focused on the minimal production-ready shell
- do not hardcode theme values; the design-system skill runs next
