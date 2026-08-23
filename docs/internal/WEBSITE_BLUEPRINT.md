# DINO WEBSITE BLUEPRINT

**Version:** 1.1  
**Target:** Developers, Data Engineers, ML Engineers, Compliance teams  
**Tone:** Precise, direct, technical, calm, trust-building  
**Aesthetic:** Purist, industrial, dark, content-first

Central story:

> Dino is the motor for deterministic audits. Your pipeline runs. Dino seals it. Your dashboard shows the proofs. Nothing more.

---

## 1. Design system

### Colors

| Role | Name | Hex | Use |
|------|------|-----|-----|
| Background | Anthracite | `#0A0A0E` | Page |
| Surface | Dark gray | `#121216` | Panels |
| Border | Cool gray | `#1E1E26` | Dividers |
| Hover | Light gray | `#282830` | Interaction |
| Text | Near-white | `#E8E8ED` | Headlines |
| Muted | Gray | `#8A8A99` | Body, labels |
| Accent | Tech blue | `#3B82F6` | CTAs, links |
| Accent hover | Blue | `#2563EB` | CTA hover |
| Code bg | Black | `#000000` | Code blocks |

### Typography

- **Headlines:** Inter 700, `letter-spacing: -0.03em`
- **Body:** Inter 400, `line-height: 1.7`
- **Code:** JetBrains Mono 400, `0.875rem`
- Technical tokens (`proof.json`, `proof_hash`, schemas) always mono

### Layout rules

- `max-width: 1100px`, `px-6`
- Section padding `py-24`
- `border-radius: 0` everywhere
- No box-shadow, no glow, no decorative icons/emojis
- Left-aligned (docs feel, not sales)
- Soft transitions `0.2s ease`
- Subtle hero grid only (no radial glow)

### Voice

- Precise — say exactly what it is
- Direct — no filler
- Technical — use real terms
- Confident — no hype words
- Short — every sentence earns its place

---

## 2. Page map (single marketing page)

| Route | Role |
|-------|------|
| `/` | Full story — all sections via anchors |
| `/docs` | Doc index (repo links) |

### Anchors on `/`

| Anchor | Section |
|--------|---------|
| (hero) | Local-First / Audit Engine + CTAs |
| `#problem` | Problem ↔ Solution |
| `#engine` | Seal → Export → Index → Dashboard |
| `#capabilities` | USP spec list (no icons) |
| `#demo` | Embedded TerminalPlayer |
| `#quickstart` | Install code block |
| `#early-access` | Mailto conversion |

Nav: **Home · Demo · Early Access · Docs** → `/`, `/#demo`, `/#early-access`, `/docs`

### Components

`Nav` · `Button` · `Container` · `Section` · `EngineFlow` · `UspList` · `TerminalPlayer` · `Footer`

---

## 3. Rules checklist

- [x] No icon clusters in USP tiles
- [x] No rounded corners
- [x] No shadows / no glow
- [x] No generic marketing fluff
- [x] Max contrast: black / gray / white / one blue
- [x] Asymmetry over centered sales layouts
- [x] Mono for technical identifiers
- [x] Primary CTA is email
- [x] One long page (not multi-route marketing)

---

## 4. File map

| File | Role |
|------|------|
| `app/globals.css` | CSS variables + hero grid |
| `tailwind.config.js` | Token mapping + fonts |
| `app/layout.tsx` | Inter + JetBrains Mono |
| `app/page.tsx` | Single-page blueprint sections |
| `lib/content.ts` | Copy source |
| `docs/internal/WEBSITE_BLUEPRINT.md` | This document |
