# Motion Design Kit Setup

Get the motion plugin working in Claude Code in a couple of commands.

---

## Installation

### Option A: Install via Marketplace (Recommended)

**Step 1: Register the marketplace (one-time)**

```bash
/plugin marketplace add martin-iliew/motion-design-kit
```

**Step 2: Install the plugin**

```bash
/plugin install motion-design-kit@motion-design-kit
```

Done. All 5 skills are active.

Claude Code community distribution is currently a two-command flow. A true one-command install requires publication in Anthropic's official marketplace.

### Option B: Clone & Load Locally

```bash
git clone https://github.com/martin-iliew/motion-design-kit.git
cd motion-design-kit
claude --work .
```

Either method works — Option A is faster if you just want to use the skills. Option B is better if you're contributing new patterns.

---

## Using the Skills

### Write animations

```
/motion-dev animate a button with spring hover effect, using React + GSAP
```

### Audit existing code

```
/motion-audit src/components/Hero.jsx
```

### Quick fix (audit + auto-fix)

```
/motion-enhance src/pages/home.html
```

### Discover trends

```
/motion-discover
```

### Refresh library rankings

```
/motion-refresh
```

---

## What Each Skill Does

| Skill               | Use when                      | Command                  |
| ------------------- | ----------------------------- | ------------------------ |
| **motion-dev**      | Writing new animations        | `/motion-dev [request]`  |
| **motion-audit**    | Reviewing existing animations | `/motion-audit [file]`   |
| **motion-enhance**  | Modernizing old animations    | `/motion-enhance [file]` |
| **motion-discover** | Researching 2026 trends       | `/motion-discover`       |
| **motion-refresh**  | Refreshing pattern rankings   | `/motion-refresh`        |

---

## Key Files

- **Motion Tokens** (`.claude/motion-tokens.md`) — Standard durations, easing, stagger values
- **Motion Spec** (`.claude/motion-spec.md`) — Language-neutral animation format
- **Pattern Library** (`.claude/motion-library/`) — 75 production-ready animation patterns

---

## Questions?

- **"How do I animate X?"** → Ask `/motion-dev` with your stack
- **"Is my animation performant?"** → Run `/motion-audit [file]`
- **"Does this follow our standards?"** → Run `/motion-enhance [file]`

---

**Last updated:** March 2026
