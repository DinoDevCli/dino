# DINO WEBSITE BLUEPRINT

**Version:** 1.0  
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

### Voice

- Precise — say exactly what it is
- Direct — no filler
- Technical — use real terms
- Confident — no hype words (no “revolutionary”, “disruptive”)
- Short — every sentence earns its place

---

## 2. Page structure

1. **Hero** — Local-First / Audit Engine · Live Demo + Early Access CTAs  
2. **Problem ↔ Solution** — asymmetric 2+1+2 with vertical rule  
3. **Engine flow** — Seal → Export → Index → Dashboard (dimmed)  
4. **USPs** — two-column spec list (not cards)  
5. **Live Demo** — black terminal transcript / player  
6. **Quickstart** — black code block, no copy button  
7. **Early Access** — copy left, mailto CTA right  
8. **Footer** — name left, meta right  

---

## 3. Rules checklist

- [ ] No icon clusters in tiles
- [ ] No rounded corners
- [ ] No shadows
- [ ] No generic marketing fluff
- [ ] Max contrast: black / gray / white / one blue
- [ ] Asymmetry over centered sales layouts
- [ ] Mono for technical identifiers
- [ ] Primary CTA is email (developers write mail)

---

## 4. File map

| File | Role |
|------|------|
| `app/globals.css` | CSS variables (palette) |
| `tailwind.config.js` | Token mapping + fonts |
| `app/layout.tsx` | Inter + JetBrains Mono |
| `app/page.tsx` | Blueprint sections |
| `lib/content.ts` | Copy source |
| `docs/internal/WEBSITE_BLUEPRINT.md` | This document |
