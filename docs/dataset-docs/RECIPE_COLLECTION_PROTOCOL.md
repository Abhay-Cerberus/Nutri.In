# Recipe Collection Protocol

> **Document for Paper §3.1 — Dataset & Recipes**
> **Last updated:** 2026-10-28

## Current Data Status

The 30 entries in `recipes/recipes.json` are provisional software inputs. Their
ingredient quantities, cooked yields, and serving weights have not been
weighed, sourced to specific recipes, or checked with the campus kitchen, so
each is marked low confidence. The engine uses IFCT 2017 Table 1 rows where an
exact food code is available. Unsupported ingredients and proxy mappings are
explicitly marked. Do not use current dish estimates as validated nutrition
results.

---

## 1. Purpose

This protocol defines how recipe data is collected, structured, and validated for the Nutri.In nutrition engine. Each of the 30 frozen dishes requires a sourced, confidence-tagged recipe entry mapping raw ingredient grams to IFCT 2017 nutrient codes.

## 2. Source Priority (in order)

| Priority | Source | Confidence | Notes |
|----------|--------|------------|-------|
| 1 (best) | Campus canteen/mess kitchen | **High** | Direct measurement: ask cook for per-plate quantities; photograph measuring cups/ladles; measure standard ladle volume in grams |
| 2 | Weighed home cooking | **High** | Team member cooks and weighs each raw ingredient + final cooked weight |
| 3 | Published cooked-food studies with recipe and yield data | **High only when directly reported** | A paper describing moisture correction does not by itself source a recipe or cooked yield |
| 4 | Standard recipe books (Tarla Dalal, Sanjeev Kapoor) | **Medium** | Well-known standardized recipes, but may differ from canteen |
| 5 | Recipe websites (Hebbars Kitchen, VahChef) | **Medium** | Cross-reference 2–3 sources; use median values |
| 6 | MyFitnessPal / Nutritionix | **Low** | User-submitted, unverified; use only as sanity check |

## 3. Per-Recipe Data Requirements

Every recipe entry in `recipes.json` **MUST** include:

```
Required fields:
├── dish_id                    # snake_case identifier matching SCOPE.md
├── dish_name                  # Human-readable name
├── serving_units              # Common serving containers + grams
│   ├── katori (small bowl)    # ~150g
│   ├── plate/serving          # ~250-300g
│   └── [unit-specific]        # e.g., "piece" for samosa, "each" for idli
├── ingredients[]              # Array of ingredients
│   ├── name                   # Ingredient name
│   ├── raw_g                  # Raw weight in grams for one draft serving
│   ├── ifct_code              # Exact IFCT 2017 code, when available
│   ├── nutrition_per100g      # Required only for non-IFCT provisional overrides
│   ├── nutrition_source       # Source/status for a provisional override
│   └── source_note            # Proxy or data-quality caveat
├── raw_total_g                # Sum of all raw ingredient grams
├── cooked_total_g             # Measured cooked weight of the recipe
├── moisture_correction_factor # cooked_total / raw_total (or vice versa, documented)
├── source                     # Where this recipe came from
├── confidence                 # "high" / "medium" / "low"
└── notes                      # Any caveats, variants, assumptions
```

## 4. Measurement Protocol (for canteen/kitchen collection)

### Equipment
- Kitchen scale (±1g accuracy, capacity ≥2kg)
- Standard plates/bowls used in canteen (photograph them with ₹5 coin for reference)
- Measuring cups/spoons (backup)
- Camera (phone) for documentation

### Steps
1. **Introduce yourself** to the cook; explain academic purpose
2. **Request one standard serving** of the dish
3. **Photograph** the serving on the standard plate with ₹5 coin
4. **Weigh** the full plate → subtract plate weight = cooked_total_g
5. **Ask the cook** for raw ingredient quantities for that serving
6. If cook uses volume measures (cups, ladles):
   - Measure one ladle/cup of each ingredient on the scale
   - Record: "1 ladle of oil = 15g" etc.
7. **Record source** as "campus_mess_kitchen"
8. **Repeat for 3 servings** if possible (small/medium/large) to capture portion spread

### For Raw-Weighing Subset (~50 dishes)
For the Stage 2 weighed photo dataset, also:
1. Weigh each raw ingredient separately before cooking
2. Record total raw weight
3. Weigh final cooked output
4. Compute moisture_correction_factor = cooked_total_g / raw_total_g

## 5. Spice Mix Handling

The current `Spice mix` rows are unverified placeholders for software
integration. For publishable estimates, record each spice and its raw weight,
then use an exact IFCT entry when available. If a combined mix must be retained,
mark it provisional and document its composition and source.

```json
{
  "name": "Spice mix (cumin, turmeric, coriander, chilli)",
  "raw_g": 5,
  "ifct_code": "SPICE_MIX",
  "kcal_per100g": 300,
  "protein_per100g": 10.0,
  "carbs_per100g": 40.0,
  "fat_per100g": 10.0
}
```

Do not assume the mix has negligible nutrient contribution or inherits the
accuracy reported in another study. This project has not measured the mix or
validated its nutrient profile.

## 6. Conflict Resolution

When multiple sources disagree on ingredient quantities:

| Situation | Resolution |
|-----------|-----------|
| Canteen recipe vs. website recipe | **Canteen wins** — it's our target population |
| Two websites disagree | Use **median** of top 3 sources; note all in `notes` |
| Oil/ghee quantity uncertain | Default to **15ml (13.5g) per serving** for curries; document assumption |
| Regional variant differs significantly | Keep **one default variant**; note others in `notes` for discussion section |

## 7. Quality Checklist (per recipe)

- [ ] dish_id matches SCOPE.md frozen list
- [ ] Each ingredient has either an exact IFCT code or a sourced, clearly marked override
- [ ] raw_total_g = sum of all ingredient raw_g
- [ ] cooked_total_g is measured (not assumed)
- [ ] moisture_correction_factor computed correctly
- [ ] source field is filled
- [ ] confidence tag assigned
- [ ] Serving units defined with gram weights
