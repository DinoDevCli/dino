# DINO WEBSITE BLUEPRINT

**Version:** 2.0 — Final documentary single-page  
**Target:** Developers, Data Engineers, ML Engineers, Compliance  
**Tone:** Documentary, technical, artifact-based — not marketing  
**Aesthetic:** Dark, industrial, content-first

Central story:

> Two fraud-score runs. Seal both. Diff them. That is the audit.

---

## Philosophy

- No AI template look
- No marketing tone / polished SaaS
- Documentary: real commands, golden JSON, real hashes when present
- One page, anchor navigation
- **Primary demo** = `DemoWalkthrough` (readable without Play)
- **Terminal replay** = optional, slow, never first impression

---

## 1. Design system

### Colors

| Role | Hex | Use |
|------|-----|-----|
| Background | `#0A0A0F` | Page |
| Code | `#000000` | Command panels |
| JSON box | `#111118` | Artifact excerpts |
| Border | `#1E1E26` | Dividers / frames |
| Text | `#FFFFFF` | Headlines |
| Secondary | `#A0A0B0` | Body, labels, CLI prompt |
| Accent | `#FF6B00` | Sparse emphasis only |

### Typography

- **Headlines:** Inter 700
- **Body:** Inter 400
- **Code / tokens:** JetBrains Mono

### Layout

- Engine / USP: `max-width: 1200px`
- Demo / Early Access: `max-width: 800px`
- Hero copy: `max-width: 900px`
- Section padding: `py-24`
- `border-radius: 0`
- No glow, no autotype, no animation, no marketing pills

---

## 2. Page map

| Route | Role |
|-------|------|
| `/` | Full documentary page |
| `/docs` | Optional doc index (repo links) — not in primary nav |

### Nav

**Dino · Demo · Early Access · GitHub**

Hash links use plain `<a href="{basePath}/#…">` (Next `Link` does not scroll same-page hashes).

### Section order

1. Hero — static `$ dino version`
2. Problem / Context
3. Engine Flow (Seal → Export → Index → Dashboard)
4. USPs (5 tiles)
5. DemoWalkthrough (`#demo`)
6. Terminal Replay (`#replay`) — optional, slow
7. Early Access (`#early-access`) — mailto only
8. Footer — Early Access · MIT · v0.3.1

---

## 3. Demo rules

- Steps: command → explanation → golden artifact
- Excerpts from `tests/simulation/golden/demo_excerpts.json`
- Final callout: `changed: true` + `pipeline_version_diff`
- Fail-closed step (`EMPTY_SCAN_ROOTS`) kept for honesty
- TerminalPlayer: `autoplay=false`, ~400ms/line, pause on `#`

---

## 4. File map

| File | Role |
|------|------|
| `website/app/globals.css` | Tokens, code/json panels, static grid |
| `website/tailwind.config.js` | Token mapping |
| `website/app/page.tsx` | Section order |
| `website/lib/content.ts` | All copy + golden excerpts |
| `website/components/DemoWalkthrough.tsx` | Primary demo |
| `website/components/TerminalPlayer.tsx` | Optional replay |
| `website/components/Nav.tsx` | Anchor + GitHub |
| `docs/internal/WEBSITE_BLUEPRINT.md` | This document |

---

## 5. Success criteria

A developer can:

1. Read the page like a technical document
2. Understand the demo without pressing Play
3. See real golden JSON / compare fields
4. Follow the fraud_score v1/v2 use case
5. Perceive Dino as an audit engine — not a landing-page product
