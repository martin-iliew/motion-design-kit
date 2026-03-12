# motion-design-kit

A public **Claude Code plugin marketplace and plugin** for writing, auditing, discovering, refreshing, and enhancing modern web animations. It ships 5 motion skills backed by a 75-pattern motion library with specs and code snippets.

**Status:** Public GitHub marketplace for Claude Code

---

## Skills

### `motion-dev`

**Expert animation code writer.** Writes clean, accessible, performant animation code for any stack (GSAP, CSS, Tailwind, React, Vue).

**Capabilities:**

- Write/generate animation code for any framework
- Convert animations between stacks ("give me the React version")
- Review and fix animation code
- Advise on GPU-safe properties and performance
- Make UI feel "more alive", "bouncy", "fluid", or "tactile"

**Trigger:** Mention animation intent, use `/motion-dev`, or share animation code

---

### `motion-audit`

**Animation quality auditor.** Analyzes HTML/JS/CSS files for animation issues across five quality dimensions.

**What it checks:**

- Dependencies (correct library imports, versions)
- Modernity (2026 patterns, current best practices)
- Performance (GPU safety, reflow/repaint, efficiency)
- Conflicts (animation clashes, timing issues)
- Consistency (follows motion tokens, patterns)

**Use when:**

- You need to audit animation code for quality and best practices
- Code feels dated or has performance issues
- Want a detailed severity report (CRITICAL/WARNING/INFO)

**Trigger:** Use `/motion-audit [file]` or ask to review animation code

---

### `motion-discover`

**Animation trend researcher.** Discovers and catalogs modern 2026 web motion patterns.

**What it does:**

- Research 12+ current animation trends
- Generate pattern files with specs and code snippets
- Auto-update the motion library

**Use when:**

- Want to modernize a site's animations
- Need new animation pattern ideas
- Want to document what 2026 animation trends look like

**Trigger:** Use `/motion-discover`

---

### `motion-refresh`

**Motion library reranker.** Re-evaluates the existing motion library against current 2026 trends and regenerates the lookup index used by the other skills.

**What it does:**

- Research current animation trends
- Update trend fields in the motion library catalog
- Regenerate the `scores.yaml` inverted index

**Use when:**

- Want fresh ranking data before a major update
- Need to rerank patterns against current 2026 trends
- Want to detect gaps in the library without creating new patterns yet

**Trigger:** Use `/motion-refresh`

---

### `motion-enhance`

**One-step audit + auto-fix.** Evaluates animation code against motion library patterns and auto-fixes issues.

**What it does:**

- Audit against the 75-pattern motion library
- Report which patterns apply to your code
- Auto-fix all CRITICAL and WARNING issues

**Use when:**

- Want to modernize animations in one step
- Need both audit and fixes applied automatically

**Trigger:** Use `/motion-enhance [file]`

---

## Quick Start

Use any of these commands to invoke the skills:

### `/motion-dev [request]`

Write or fix animation code. Examples:

- `animate a button with spring physics`
- `convert this GSAP code to React hooks`
- `make this scroll animation more performant`

### `/motion-discover`

Research and generate 2026 animation trends. Outputs new patterns to `.claude/motion-library/`.

### `/motion-refresh`

Research current animation trends and rerank the motion library by relevance and popularity. Updates `.claude/motion-library/catalog.yaml`, refreshes `.claude/motion-library/trends-overview.md`, and regenerates the `.claude/motion-library/scores.yaml` lookup index. Run monthly or quarterly to keep pattern relevance current.

### `/motion-audit [file]`

Full animation quality audit. Reports CRITICAL/WARNING/INFO issues.

```bash
/motion-audit my-site.html
```

### `/motion-enhance [file]`

Audit + auto-fix in one step. Fixes all CRITICAL and WARNING issues.

```bash
/motion-enhance my-site.html
```

---

## Motion Library

**75 production-ready animation patterns** organized across scroll-driven storytelling, typography, micro-interactions, galleries, navigation, modals, loaders, cursors, ambient effects, and transitions.

**Location:** `.claude/motion-library/`

**Each pattern includes:**

- `index.md` — Documentation, use cases, do's/don'ts, best practices
- `spec.yaml` — Language-neutral animation specification
- `snippet.css` or `snippet.js` — Copy-paste ready code

Browse the [full catalog](./.claude/motion-library/catalog.yaml).

---

## Reference

### Motion Tokens (`.claude/motion-tokens.md`)

Standardized animation values — duration, easing, and stagger scales. Use these when writing animations to maintain consistency.

**Quick reference:**

- **Duration:** `micro` (150ms), `fast` (300ms), `base` (600ms), `slow` (1s), `epic` (1.5s)
- **Easing:** `entrance`, `impact`, `transition`, `exit`, `spring`, `elastic`, `scrub`, `brand`
- **Stagger:** `tight` (0.04–0.06s), `medium` (0.08–0.10s), `loose` (0.12–0.15s)
- **GPU-Safe Properties:** `x`, `y`, `scale`, `rotation`, `opacity` (only these animate without reflow)

### Motion Spec (`.claude/motion-spec.md`)

Language-neutral YAML format for describing animations. Use this when:

- Documenting custom animations
- Translating between stacks
- Creating new motion library patterns

---

## Installation & Setup

These skills work with **Claude Code**. This repository now includes both a strict plugin manifest at `.claude-plugin/plugin.json` and a GitHub marketplace manifest at `.claude-plugin/marketplace.json`.

### Community Install

Claude Code community marketplaces currently use a two-command flow:

Step 1 (one-time): Register the marketplace

```bash
/plugin marketplace add martin-iliew/motion-design-kit
```

Step 2: Install the plugin

```bash
/plugin install motion-design-kit@motion-design-kit
```

All 5 skills and their slash commands become available after install. Claude Code will pull updates from the same GitHub source when the plugin is updated.

If you want a true one-command install from the official Anthropic marketplace, the remaining step is submitting this plugin for official marketplace inclusion. The repository is now structured for that path.

**Alternative — Clone & load locally:**

```bash
git clone https://github.com/martin-iliew/motion-design-kit.git
cd motion-design-kit
claude --work .
```

Use this if you're contributing new patterns or want full local control.

**How to use:**

- **Explicit:** Type `/motion-dev [request]`, `/motion-audit [file]`, `/motion-discover`, `/motion-refresh`, or `/motion-enhance [file]`
- **Auto-trigger:** Skills activate automatically when context mentions animation + framework

---

## Example: Animate a Card Hover

**Request:**

```
I want a card to lift on hover with a spring effect. Using vanilla JS + GSAP.
```

**Claude (via `motion-dev`):**
Detects vanilla JS + GSAP, loads motion tokens, enforces GPU-safe properties, wraps in `gsap.matchMedia()`, includes reduced-motion guard.

Output:

```javascript
// token: micro / spring
gsap.to(card, {
  y: -12,
  duration: 0.15, // token: micro
  ease: "back.out(1.7)", // token: spring
  overwrite: "auto",
});
```

---

## Workflows

### Write a new animation

1. Describe what you want to animate + which stack (React, Vue, CSS, vanilla)
2. Use `/motion-dev` (triggers auto-magically or explicitly)
3. Get production-ready code with token comments and reduced-motion guards

### Audit existing animations

1. Run `/motion-audit my-file.html`
2. Review severity report (CRITICAL/WARNING/INFO)
3. Optionally apply auto-fixes

### Modernize a site's motion

1. Run `/motion-enhance my-site.html`
2. Review which 2026 patterns apply
3. Auto-fixes apply; manual tweaks available via `/motion-dev`

### Discover new animation trends

1. Run `/motion-discover`
2. 12+ patterns generate in `.claude/motion-library/`
3. Copy snippets into your project

### Refresh pattern rankings

1. Run `/motion-refresh`
2. Review notable score and status changes
3. Use the regenerated `scores.yaml` index in downstream skills

---

## Directory Structure

```
.
├── README.md                    # This file
└── .claude/
    ├── commands/                # Slash command definitions
    │   ├── motion-dev.md
    │   ├── motion-audit.md
    │   ├── motion-discover.md
    │   ├── motion-enhance.md
    │   └── motion-refresh.md
    ├── skills/                  # Production skills
    │   ├── motion-dev/
    │   │   ├── SKILL.md
    │   │   └── references/      # Motion spec, tokens, guides
    │   ├── motion-audit/
    │   │   ├── SKILL.md
    │   │   └── references/
    │   ├── motion-discover/
    │   │   ├── SKILL.md
    │   │   └── references/
    │   ├── motion-enhance/
    │       ├── SKILL.md
    │       └── references/
    │   └── motion-refresh/
    │       └── SKILL.md
    ├── motion-library/          # 25 production animation patterns
    │   ├── catalog.yaml
    │   ├── scroll-trigger-reveal/
    │   ├── spring-physics-interactions/
    │   └── [22 more patterns]
    ├── scripts/                 # Utility scripts
    │   └── query_cost.py
    ├── motion-tokens.md         # Standardized animation values
    ├── motion-spec.md           # Language-neutral spec format
    └── settings.json            # Claude Code configuration
```

---

---

## Team Reference

**For animation questions:**

1. **Writing new animations?** → Use `/motion-dev` (supports all stacks)
2. **Code feels dated?** → Use `/motion-enhance` (audit + auto-fix)
3. **Need a full review?** → Use `/motion-audit` (detailed severity report)
4. **Want new patterns?** → Use `/motion-discover` (research 2026 trends)
5. **Need fresh ranking data?** → Use `/motion-refresh` (rerank the library and regenerate the index)

**Updating the library:**
When patterns are added or improved, commit to `main`:

```bash
git add .claude/motion-library/
git commit -m "motion-library: add new pattern [name]"
git push
```

Then marketplace users can pull or reinstall to get the latest patterns.

---

**Status:** Public GitHub marketplace
**Skills:** 5 | **Commands:** 5 | **Patterns:** 75 | **Last updated:** March 2026
