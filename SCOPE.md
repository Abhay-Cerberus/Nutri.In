# SCOPE.md — Project Scope Document

**Last updated:** 2026-10-24
**Status:** ✅ FROZEN — dish list locked. Changes only by guide approval.

---

## What's IN Scope

- **Single-dish photos** — one dish per image
- **30 Indian dishes** — selected by intersecting:
  - (a) Khana dataset's 80 classes (verified ✅)
  - (b) Campus canteen/mess availability (typical North+South Indian institutional menu)
  - (c) IFCT 2017 ingredient coverage (all raw ingredients available)
- **Macronutrients:** Calories (kcal), Protein (g), Carbohydrates (g), Fat (g)
- **Uncertainty ranges:** Point estimate ± portion uncertainty per dish category
- **Web prototype** — photo upload → dish ID + grams + calories + range → chat refine
- **Benchmark:** GPT-4o and Gemini vs. our pipeline on identical 100 test images
- **Released resources:** Recipe table + weighed test set documentation

## What's OUT of Scope

- Multi-item automatic segmentation (thalis with multiple dishes)
- Micronutrients (vitamins, minerals — IFCT supports it, but scope constraint for macros focus)
- Regional recipe variants beyond one default per dish
- Drinks and beverages (chaas, solkadhi, falooda, lassi excluded)
- Packaged/processed foods (pizzas, garlic bread excluded — not traditional Indian)
- Real-time video analysis
- Sweets/desserts as primary targets (excluded: laddu, jalebi, kheer, etc. — difficult to weigh consistently, less relevant to daily meal tracking)
- Non-Indian items in Khana (pizza variants, chicken wings, garlic bread)

---

## Selection Methodology

**Step 1:** Started with Khana's 80 classes and taxonomy.

**Step 2:** Excluded categories unlikely in daily canteen/mess meals:
- Pizza (4 classes) — not traditional Indian food
- Sweets (16 classes) — inconsistent portioning, less dietary-tracking relevance
- Beverages (2 classes) — liquid volume estimation is a different problem
- Others/fasting (7 classes) — niche items (ghevar, chikki, patrode, murukku, etc.)
- Garlic bread, chicken wings — Western items

**Step 3:** From remaining ~51 classes, selected 30 that satisfy:
- Available in a typical Indian college canteen/mess
- All raw ingredients have IFCT 2017 entries
- Represent diversity: curries, dals, rice dishes, flatbreads, snacks, South Indian items
- Include both veg and non-veg
- Cover portion-estimation difficulty spectrum: liquid (dal), mounded (rice), flat (roti), mixed (biryani)

---

## Frozen Dish List (30 Dishes)

> **FREEZE DATE:** 2026-10-24 — changes only by guide approval.

### Main Course — Curries & Gravies (8 dishes)

| # | Dish ID | Dish Name | Khana Class | Category | Dietary | Portion Difficulty |
|---|---------|-----------|-------------|----------|---------|-------------------|
| 1 | `aloo_gobi` | Aloo Gobi | aloo gobi | curry/aloo | Veg | Medium (chunky) |
| 2 | `aloo_mutter` | Aloo Mutter | aloo mutter | curry/aloo | Veg | Medium (gravy) |
| 3 | `palak_paneer` | Palak Paneer | palak paneer | curry/paneer | Veg | Medium (thick gravy) |
| 4 | `paneer_masala` | Paneer Masala | paneer masala | curry/paneer | Veg | Medium (gravy) |
| 5 | `chana_masala` | Chana Masala | chana masala | curry | Veg | Medium (chunky) |
| 6 | `bhindi_masala` | Bhindi Masala | bhindi masala | curry | Veg | Easy (dry) |
| 7 | `anda_curry` | Anda Curry | anda curry | curry | Non-Veg | Medium (gravy) |
| 8 | `fish_curry` | Fish Curry | fish curry | curry | Non-Veg | Hard (liquid gravy) |

### Main Course — Rice & Dal (4 dishes)

| # | Dish ID | Dish Name | Khana Class | Category | Dietary | Portion Difficulty |
|---|---------|-----------|-------------|----------|---------|-------------------|
| 9 | `rajma_chawal` | Rajma Chawal | rajma chawal | rice | Veg | Medium (mixed) |
| 10 | `biryani` | Biryani | biryani | rice | Veg/NV | Hard (mounded, layered) |
| 11 | `dal_khichdi` | Dal Khichdi | dal khichdi | rice | Veg | Medium (semi-liquid) |
| 12 | `navratan_korma` | Navratan Korma | navratan korma | curry | Veg | Medium (gravy) |

### Flatbreads & Bread-Based (6 dishes)

| # | Dish ID | Dish Name | Khana Class | Category | Dietary | Portion Difficulty |
|---|---------|-----------|-------------|----------|---------|-------------------|
| 13 | `chapati` | Chapati / Roti | chapati | bread/flatbread | Veg | Easy (flat, countable) |
| 14 | `aloo_paratha` | Aloo Paratha | aloo paratha | bread/flatbread | Veg | Easy (flat) |
| 15 | `chole_bhature` | Chole Bhature | chole bhature | bread/flatbread | Veg | Medium (mixed dish) |
| 16 | `puri_bhaji` | Puri Bhaji | puri bhaji | bread/flatbread | Veg | Medium (mixed) |
| 17 | `garlic_naan` | Garlic Naan | garlic naan | bread/flatbread | Veg | Easy (flat) |
| 18 | `amritsari_kulcha` | Amritsari Kulcha | amritsari kulcha | bread/flatbread | Veg | Easy (flat) |

### South Indian (5 dishes)

| # | Dish ID | Dish Name | Khana Class | Category | Dietary | Portion Difficulty |
|---|---------|-----------|-------------|----------|---------|-------------------|
| 19 | `masala_dosa` | Masala Dosa | masala dosa | south indian/dosa | Veg | Medium (folded, variable) |
| 20 | `idli` | Idli | idli | south indian | Veg | Easy (countable units) |
| 21 | `medu_vada` | Medu Vada | medu vada | south indian | Veg | Easy (countable) |
| 22 | `uttapam` | Uttapam | uttapam | south indian | Veg | Medium (flat, variable thickness) |
| 23 | `poha` | Poha | poha | snacks | Veg | Medium (mounded) |

### Snacks & Street Food (5 dishes)

| # | Dish ID | Dish Name | Khana Class | Category | Dietary | Portion Difficulty |
|---|---------|-----------|-------------|----------|---------|-------------------|
| 24 | `samosa` | Samosa | samosa | snacks | Veg | Easy (countable) |
| 25 | `vada_pav` | Vada Pav | vada pav | snacks | Veg | Easy (countable) |
| 26 | `pav_bhaji` | Pav Bhaji | pav bhaji | snacks | Veg | Medium (semi-liquid + bread) |
| 27 | `dhokla` | Dhokla | dhokla | snacks | Veg | Easy (countable pieces) |
| 28 | `onion_pakoda` | Onion Pakoda | onion pakoda | snacks | Veg | Medium (irregular) |

### Kebab & Non-Veg (2 dishes)

| # | Dish ID | Dish Name | Khana Class | Category | Dietary | Portion Difficulty |
|---|---------|-----------|-------------|----------|---------|-------------------|
| 29 | `seekh_kebab` | Seekh Kebab | seekh kebab | kebab | Non-Veg | Easy (countable) |
| 30 | `hara_bhara_kabab` | Hara Bhara Kabab | hara bhara kabab | kebab | Veg | Easy (countable) |

### Summary Statistics

| Property | Count |
|----------|-------|
| Total dishes | 30 |
| Vegetarian | 26 |
| Non-vegetarian | 4 (anda curry, fish curry, biryani*, seekh kebab) |
| Easy portion estimation | 11 (flat/countable items) |
| Medium portion estimation | 15 (gravies, mounded) |
| Hard portion estimation | 4 (liquid gravies, layered dishes) |
| Khana coverage | 30/30 ✅ |
| IFCT ingredient coverage | 30/30 ✅ (all raw ingredients mappable) |
| Typical canteen availability | 30/30 ✅ |

*\*Biryani can be veg or non-veg; we default to veg recipe, note non-veg variant in recipes.json*

---

## Portion Estimation Categories (for height priors in Stage 4)

| Category | Dishes | Height Prior |
|----------|--------|-------------|
| **Flat** | chapati, aloo paratha, garlic naan, kulcha, masala dosa, uttapam | ~0.5–1.5 cm |
| **Countable** | idli, medu vada, samosa, vada pav, dhokla, pakoda, seekh kebab, hara bhara kabab | Per-unit weight |
| **Mounded** | biryani, poha, dal khichdi, rajma chawal | ~3–6 cm |
| **Pooled/Gravy** | palak paneer, paneer masala, chana masala, aloo gobi, aloo mutter, navratan korma, anda curry, bhindi masala | ~2–4 cm |
| **Liquid** | fish curry, pav bhaji (curry portion) | Container-fill assumption |
| **Mixed** | chole bhature, puri bhaji | Component-wise estimation |

---

## Scope Change Log

| Date | Change | Reason | Approved by |
|------|--------|--------|-------------|
| 2026-10-24 | Initial dish list frozen (30 dishes) | Intersected Khana × canteen × IFCT | Team consensus |
