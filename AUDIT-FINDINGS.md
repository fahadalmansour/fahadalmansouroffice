# fahadalmansouroffice — Visual/UX Audit

Last run: **2026-05-08** · Run ID: **2026-05-08-1500**
Captured: `~/.claude/reports/fahadalmansouroffice/screenshots/2026-05-08/` (3 shots: home × 3 viewports × en)
HEAD: `b648043`
Notion: https://www.notion.so/e38bdfd54e3343109402b1def5e8c693

> Single-page brand identity site (static HTML, deployed to VPS via rsync). No AR/RTL variant captured because the site is EN-only per registry.

**Tally:** 0 BLOCKER · 2 HIGH · 4 MEDIUM · 3 LOW · 1 OUT-OF-SCOPE = **10 findings**

---

## BLOCKER
*(none)*

---

## HIGH

### H1. Hero FA badge oversized on mobile, pushes headline below the fold
- Viewport / page / locale: 360 / home / en
- Source: `index.html`
- Fix: Cap the hero badge SVG to ~140-160 px on viewports <480 (e.g. `max-width: 45vw`) so the bilingual headline + CTAs sit within the first viewport.

### H2. About paragraph line length too long at 1280 (~110ch)
- Source: `index.html`
- Fix: Constrain the About paragraph wrapper to `max-width: 65ch` (or ~720 px) and center it; keep the badge column on the left.

---

## MEDIUM

### M1. Service-card icons compete with card titles (1280)
- Source: `index.html`
- Fix: Reduce navy icon tile from ~56 px to ~44 px, or switch to outlined icons on a tinted background, so the H3 title becomes the dominant element.

### M2. Top utility strip cramped on mobile (360)
- Source: `index.html`
- Fix: Below 480 px, hide the "ELECTRONIC SERVICES & E-COMMERCE" tagline in the utility bar (or move it under the FA badge); keep only the domain link.

### M3. Contact rows mix LTR labels + RTL values without consistent alignment (360)
- Source: `index.html`
- Fix: Force each row to `flex-direction: column; text-align: start` so the Arabic value sits predictably under its English label.

### M4. Message textarea too short to invite real inquiries
- Source: `index.html`
- Fix: `min-height: 140px` (or `rows=5`) on the contact-form textarea so the form looks like a business inquiry form, not a feedback widget.

---

## LOW

### L1. Primary + secondary CTA have identical visual weight (768)
- Source: `index.html`
- Fix: Make "Our Services" solid navy primary; convert "Contact Us" to ghost/outline (transparent fill, navy border + text).

### L2. Footer copyright + meta wraps awkwardly at 360
- Source: `index.html`
- Fix: Stack footer meta as 3 centered lines (EN tagline / AR tagline / © + CR) with `line-height: 1.5`; avoid inline separators on mobile.

### L3. Service cards stretch full-width on mobile — weakens "card" affordance (360)
- Source: `index.html`
- Fix: Add ~16 px horizontal padding around `.services` container on mobile; subtle 1 px border or shadow so each card reads as discrete.

---

## OUT-OF-SCOPE

### OOS1. Bilingual hero would benefit from a true RTL/LTR dual-column layout
- Source: `index.html`
- Why out of scope: Restructures the hero into paired EN/AR columns with mirrored direction attributes — that's a hero rewrite, not a component fix.

---

## Summary

This site is a single-page brand identity that's already calm and brand-forward at 1280 / 768. Findings cluster on **mobile reflow** (H1, M2, L2, L3) and **typographic restraint at desktop** (H2 line length, M1 icon weight). No commerce surface, no auth flow, no RTL parity to test — so the audit is naturally smaller than the Woo stores.

The two HIGH items are the highest leverage: capping the hero badge on 360 and constraining About line length at 1280. After those, the medium-tier items are 1-line CSS edits.
