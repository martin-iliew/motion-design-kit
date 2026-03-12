# motion-design-kit

Claude Code plugin for modern web motion work. It gives your team 5 motion skills plus a 75-pattern library so they can point Claude at a real app file and let it write, audit, or modernize the animation code.

Best use case: you already have a file like `index.html`, `Hero.tsx`, `Hero.vue`, or `Hero.svelte` and you want Claude to handle the implementation instead of hand-writing the motion layer yourself.

**Status:** Public GitHub marketplace for Claude Code

---

## Fast Start

### 1. Install the plugin

From a terminal:

```bash
claude plugin marketplace add --scope user martin-iliew/motion-design-kit
claude plugin install --scope user motion-design-kit@motion-design-kit
```

Inside Claude Code, the slash-command equivalent is:

```bash
/plugin marketplace add martin-iliew/motion-design-kit
/plugin install motion-design-kit@motion-design-kit
```

Today, the community install path is 2 commands. Once installed, the plugin is available in any project where Claude Code can load user-scoped plugins.

### 2. Add the recommended project settings

Plugin install gives your team the skills and slash commands. It does **not** automatically change permission behavior inside every app repo.

In the project they want Claude to edit, create `.claude/settings.json` and use this:

```json
{
  "permissions": {
    "defaultMode": "acceptEdits",
    "allow": [
      "Bash(rg:*)",
      "Bash(ls:*)",
      "Bash(dir:*)",
      "Bash(Get-ChildItem:*)",
      "Bash(cat:*)",
      "Bash(type:*)",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git ls-files:*)",
      "Bash(git rev-parse:*)",
      "Bash(npm run build:*)",
      "Bash(npm run lint:*)",
      "Bash(npm run test:*)",
      "Bash(pnpm run build:*)",
      "Bash(pnpm run lint:*)",
      "Bash(pnpm run test:*)",
      "Bash(yarn build:*)",
      "Bash(yarn lint:*)",
      "Bash(yarn test:*)",
      "Bash(bun run build:*)",
      "Bash(bun run lint:*)",
      "Bash(bun run test:*)"
    ]
  }
}
```

This is the same profile stored in this repo at `.claude/settings.json`.

What it does:

- Claude can edit files without asking every time.
- Claude can inspect the repo and run common read/build/lint/test commands without constant permission prompts.
- Package installs, unusual shell commands, and pushes still ask unless the user allows them explicitly.

### 3. Open Claude Code at the app root

```bash
cd your-project
claude
```

Then reference real file paths from that project in your prompt or slash command.

---

## Daily Workflow

The fastest way to use this plugin is:

1. Open Claude Code in your app repo.
2. Give Claude a file path.
3. Say what motion outcome you want.
4. Let Claude inspect the file and make the changes.

You do **not** need to explain the implementation in detail.

Good request shape:

```text
[file path] + [what should happen] + [optional stack/library preference]
```

Examples:

- `src/index.html add a polished scroll-triggered reveal to the pricing cards`
- `src/components/Hero.tsx add a premium intro animation and keep the current layout`
- `src/components/Hero.vue make the testimonials feel more alive on scroll`
- `src/lib/Hero.svelte modernize the section transitions and keep them accessible`

What Claude will usually do on its own:

- detect whether the file is HTML, React, Vue, Svelte, or another frontend format
- inspect nearby imports and project structure
- choose the right motion implementation path for the existing stack
- update the component, markup, styles, and motion code where needed
- keep reduced-motion and performance considerations in place
- preserve the existing UI structure unless you ask for a redesign

---

## Different Ways To Use It

| Goal | Best command | What to give Claude |
| --- | --- | --- |
| Add new motion to an existing file | `/motion-dev` | file path + desired effect |
| Automatically modernize an existing file | `/motion-enhance` | one or more file paths |
| Get a report before changing anything | `/motion-audit` | one or more file paths |
| Research new pattern ideas | `/motion-discover` | no file needed |
| Re-rank the motion library | `/motion-refresh` | no file needed |

### 1. `motion-dev` for targeted implementation

Use this when you know what you want Claude to build.

```bash
/motion-dev src/index.html add a GSAP reveal for each .feature-card on scroll
```

```bash
/motion-dev src/components/Hero.tsx add an intro timeline for the heading, CTA, and hero image. Keep the component structure and use the current stack.
```

```bash
/motion-dev src/components/Hero.vue add staggered enter animations and keep it smooth on low-end devices
```

```bash
/motion-dev src/lib/Hero.svelte make the stat cards animate in when they enter the viewport
```

### 2. `motion-enhance` for do-it-for-me modernization

Use this when the file already exists and you want Claude to audit it and apply improvements automatically.

```bash
/motion-enhance src/pages/home.html
```

```bash
/motion-enhance src/components/Hero.tsx src/components/Hero.module.css
```

```bash
/motion-enhance src/components/Hero.vue
```

```bash
/motion-enhance src/lib/Hero.svelte src/lib/hero.css
```

Best when the teammate wants: "just make this feel modern and fix obvious motion issues."

### 3. `motion-audit` for report-first review

Use this when you want findings first and code changes second.

```bash
/motion-audit src/pages/home.html
```

```bash
/motion-audit src/components/Hero.tsx src/components/Hero.module.css
```

This is useful for PR review, QA, or when you want to compare before/after changes.

### 4. Plain English also works

Your team does not have to use slash commands every time. They can speak naturally as long as they reference the file.

Examples:

```text
Update src/components/Hero.tsx with a more premium entrance animation. Keep the current design.
```

```text
Inspect src/index.html and make the scroll motion feel more current, but do not redesign the section.
```

```text
Look at src/lib/Hero.svelte and add motion that feels tactile, subtle, and mobile-safe.
```

For predictable behavior, the slash commands are still the better default.

---

## File-First Examples By Stack

### HTML

If everything is in one file, just reference that file:

```bash
/motion-dev src/index.html add a sticky storytelling section with smooth reveals
```

```bash
/motion-enhance landing-page.html
```

### React / Next / TSX

If styles are colocated in the component, give the component file only:

```bash
/motion-dev src/components/Hero.tsx add a launch-style hero intro with staggered text and image motion
```

If styles are separate, include both files:

```bash
/motion-enhance src/components/Hero.tsx src/components/Hero.module.css
```

### Vue

For single-file components, one file is usually enough:

```bash
/motion-dev src/components/PricingSection.vue add scroll reveal and CTA hover motion
```

### Svelte

For `.svelte` files, the same pattern works:

```bash
/motion-dev src/lib/sections/FeatureGrid.svelte add subtle enter motion for each card
```

If there is a separate stylesheet or helper file, include it too:

```bash
/motion-enhance src/lib/sections/FeatureGrid.svelte src/lib/sections/feature-grid.css
```

### Multi-file feature

When the animation depends on multiple files, list them together so Claude has the right context.

```bash
/motion-enhance src/components/Hero.tsx src/components/Hero.module.css src/lib/animations.ts
```

Use this when markup, styles, and animation helpers live in different places.

---

## What To Tell Claude

Give Claude the minimum it needs:

- the file path
- the desired effect
- any hard constraint that really matters

Useful constraints:

- `use GSAP`
- `CSS only`
- `keep the current layout`
- `mobile-safe`
- `respect reduced motion`
- `do not touch the copy`
- `only edit this file`

You usually do **not** need to tell Claude:

- which selectors to use
- how to wire imports
- whether to update styles and markup
- which motion tokens or easing choices to apply

That is the point of the plugin.

---

## Recommended Team Behavior

For teammates who just want results fast:

1. Use `/motion-enhance` when they already have a file and want Claude to improve it automatically.
2. Use `/motion-dev` when they know the specific effect they want.
3. Include every relevant file if the component spans markup, styles, and helpers.
4. Start with one section or component, not the whole app.
5. Review the diff after Claude finishes.

Good first commands:

```bash
/motion-enhance src/pages/home.html
```

```bash
/motion-dev src/components/Hero.tsx add a premium hero entrance animation
```

```bash
/motion-audit src/components/Hero.vue
```

---

## Secondary Skills

These are more useful for maintainers than day-to-day app work:

### `motion-discover`

Researches current motion patterns and generates new entries in `.claude/motion-library/`.

### `motion-refresh`

Re-ranks the motion library and regenerates the lookup index used by the other skills.

---

## What Ships In This Repo

- 5 motion skills
- 5 slash commands
- 75 motion patterns in `.claude/motion-library/`
- generator, refresh, and validation scripts in `.claude/scripts/`
- recommended project settings in `.claude/settings.json`

---

## Maintainer Notes

If the team updates the motion library itself:

```bash
git add .claude/motion-library/ .claude/scripts/ README.md SETUP.md

git commit -m "chore: update motion design kit"
git push
```

Validate before pushing:

```bash
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
python .claude/scripts/validate_motion_library.py --expected-count 75
```

---

**Skills:** 5  
**Commands:** 5  
**Patterns:** 75  
**Last updated:** March 2026
