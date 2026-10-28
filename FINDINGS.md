# FINDINGS.md — Experiment Log

> **Rule:** Update this file the same day as any result. 10 minutes of discipline saves a week of writing.
> This file *is* your results section's raw material.

---

## Log Format

Each entry follows: `date | stage | what we ran | numbers | surprise? | paper implication`

---

## Entries

The cooked-food accuracy comparison is pending until the team adds sourced reference values.

### 2026-10-28 | Stage 1 | IFCT lookup source audit

**What we ran:** Matched the ingredient codes used in the draft recipes against Table 1 in the provided IFCT 2017 PDF and transcribed the supported raw-food values into `recipes/ifct_lookup.csv`.

**Numbers:** 31 IFCT rows transcribed with PDF page references. The engine smoke run computed all 30 draft recipes. Their quantities and yields are unmeasured. No cooked-food reference values are loaded, so the accuracy comparison has not been run.

**Surprise?** Yes — several earlier code/name pairs were wrong (for example, H001 is almond, H010 is brown gingelly seed, and M001 is raw whole egg in the IFCT table). These mappings were corrected. Foods without a direct lookup remain explicitly marked as estimates or proxies.

**Paper implication:** Treat the engine outputs as provisional software checks only. Recipe collection and an independently sourced cooked-food comparison are still required before reporting accuracy.

<!-- TEMPLATE for copy-paste:

### YYYY-MM-DD | Stage X | <Brief description>

**What we ran:** ...

**Numbers:**
| Metric | Value |
|--------|-------|
| ... | ... |

**Surprise?** Yes/No — explanation

**Paper implication:** Which section/table this feeds into

---
-->
