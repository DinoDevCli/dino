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
- Documentary: real commands, golden JSON
- One page, anchor navigation
- Top of page: **Problem → How → Architecture → Demo** only
- **Demo** = `DemoWalkthrough` (no terminal replay)

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

- Architecture: `max-width: 1200px`
- Problem / How / Demo / Early Access: `max-width: 800px`
- Section padding: `py-24`
- `border-radius: 0`
- No glow, no autotype, no animation, no marketing pills

---

## 2. Page map

### Nav

**Dino · Demo · Early Access · GitHub**

### Section order

1. Identity — `$ dino version` + product name
2. Problem (`#problem`) — fraud_score pain (no architecture dump)
3. How (`#how`) — one mechanics paragraph
4. Product (`#product`) — definition + architecture diagram
5. DemoWalkthrough (`#demo`)
6. Early Access (`#early-access`)
7. Footer

Seal / Export / Index / Compare appear as the architecture diagram under Product — not as a separate Engine/USP section.

---

## 3. Demo rules

- Steps: command → explanation → golden artifact
- Excerpts from `tests/simulation/golden/demo_excerpts.json`
- Final callout: `changed: true` + `pipeline_version_diff`
- Fail-closed step (`EMPTY_SCAN_ROOTS`) kept for honesty

---

## 4. File map

| File | Role |
|------|------|
| `website/app/globals.css` | Tokens, code/json panels, static grid |
| `website/tailwind.config.js` | Token mapping |
| `website/app/page.tsx` | Section order |
| `website/lib/content.ts` | All copy + golden excerpts |
| `website/components/DemoWalkthrough.tsx` | Demo |
| `website/components/Tiles.tsx` | ArchitectureFlow |
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
