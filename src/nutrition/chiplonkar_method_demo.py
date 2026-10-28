"""
Method Demonstration - Three Provisional Worked Examples

Demonstrates the moisture-adjusted nutrient calculation discussed by:
  Chiplonkar & Agte (2007), Asia Pacific Journal of Clinical Nutrition,
  16(2):227-239. DOI: 10.6133/APJCN.2007.16.2.05

Method:
  1. List raw ingredients with IFCT 2017 nutrient values
  2. Compute total raw nutrient content
  3. Measure cooked weight
  4. Apply moisture correction: cooked_per100g = raw_total * (100 / cooked_weight)
  5. Validate against laboratory/reference values (not done by this script)

These recipes use provisional, unmeasured ingredient quantities and cooked
yields. This is a software/method illustration, not a replication of the
study's measured foods or a validation of Nutri.In estimates.
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)
from src.nutrition.nutrition import load_recipes, load_ifct, compute_raw_totals, compute_cooked_per100g


def worked_example(dish_id: str, recipes: dict, ifct: dict):
    """Print a detailed, provisional illustration for one dish."""
    dish = recipes[dish_id]
    
    print(f"\n{'='*70}")
    print(f"WORKED EXAMPLE: {dish['dish_name']}")
    print(f"{'='*70}")
    print(f"Source: {dish['source']} | Confidence: {dish['confidence']}")
    print("Status: provisional ingredient amounts and cooked yield; not weighed")
    print(f"Notes: {dish.get('notes', 'None')}")
    
    # Step 1: Raw ingredients
    print("\nStep 1 - Raw ingredients (IFCT values or marked provisional overrides per 100 g)")
    print(f"{'Ingredient':<28} {'Source':<14} {'Raw(g)':>8} {'kcal':>8} {'P(g)':>8} {'C(g)':>8} {'F(g)':>8}")
    print("-" * 92)
    
    for ing in dish["ingredients"]:
        raw_g = ing["raw_g"]
        values = ifct[ing["ifct_code"]] if ing.get("ifct_code") else ing["nutrition_per100g"]
        kcal_contrib = (values["kcal"] / 100) * raw_g
        p_contrib = (values["protein"] / 100) * raw_g
        c_contrib = (values["carbs"] / 100) * raw_g
        f_contrib = (values["fat"] / 100) * raw_g
        if ing.get("ifct_code"):
            source_label = "IFCT proxy" if ing.get("source_note") else f"IFCT {ing['ifct_code']}"
        else:
            source_label = "PROVISIONAL"
        
        print(f"  {ing['name']:<26} {source_label:<14} {raw_g:>8.0f} {kcal_contrib:>8.1f} "
              f"{p_contrib:>8.1f} {c_contrib:>8.1f} {f_contrib:>8.1f}")
    
    # Step 2: Raw totals
    raw_totals = compute_raw_totals(dish, ifct)
    print("-" * 80)
    print(f"  {'TOTAL (raw)':<28} {dish['raw_total_g']:>8.0f} {raw_totals['kcal']:>8.1f} "
          f"{raw_totals['protein_g']:>8.1f} {raw_totals['carbs_g']:>8.1f} "
          f"{raw_totals['fat_g']:>8.1f}")
    
    # Step 3: Cooked weight
    print(f"\nStep 2 - Cooking")
    print(f"  Raw total weight:    {dish['raw_total_g']}g")
    print(f"  Cooked total weight: {dish['cooked_total_g']}g")
    mcf = dish['cooked_total_g'] / dish['raw_total_g']
    print(f"  Weight change ratio: {mcf:.2f}x ({'gained water' if mcf > 1 else 'lost water'})")
    
    # Step 4: Moisture correction
    per100g = compute_cooked_per100g(dish, ifct)
    print(f"\nStep 3 - Moisture adjustment calculation (method illustration)")
    print(f"  Formula: cooked_per100g = raw_nutrient_total * (100 / cooked_weight)")
    print(f"  Scale factor: 100 / {dish['cooked_total_g']} = {100/dish['cooked_total_g']:.4f}")
    print(f"\n  Results per 100g COOKED:")
    print(f"    Energy:  {per100g['kcal_per100g']:>8.1f} kcal")
    print(f"    Protein: {per100g['protein_per100g']:>8.1f} g")
    print(f"    Carbs:   {per100g['carbs_per100g']:>8.1f} g")
    print(f"    Fat:     {per100g['fat_per100g']:>8.1f} g")
    
    # Step 5: Serving estimate
    serving_units = dish.get("serving_units", {})
    if serving_units:
        print(f"\nStep 4 - Per-serving estimates")
        for unit_name, unit_grams in serving_units.items():
            s = unit_grams / 100.0
            print(f"  1 {unit_name} ({unit_grams}g):")
            print(f"    {per100g['kcal_per100g'] * s:.0f} kcal | "
                  f"{per100g['protein_per100g'] * s:.1f}g protein | "
                  f"{per100g['carbs_per100g'] * s:.1f}g carbs | "
                  f"{per100g['fat_per100g'] * s:.1f}g fat")
    
    return per100g


if __name__ == "__main__":
    recipes = load_recipes()
    ifct = load_ifct()
    
    print("CHIPLONKAR METHOD DEMONSTRATION")
    print("Following: Chiplonkar & Agte (2007), APJCN 16(2):227-239")
    print("Applying moisture correction to raw ingredient values -> cooked per-100g")
    print("Illustration only: quantities and cooked yields are provisional; no validation is performed.")
    
    # Three worked examples as specified in the plan:
    # 1. Flatbread example -> aloo_paratha
    # 2. A curry → palak_paneer
    # 3. A rice dish → dal_khichdi
    
    examples = ["aloo_paratha", "palak_paneer", "dal_khichdi"]
    
    results = {}
    for dish_id in examples:
        per100g = worked_example(dish_id, recipes, ifct)
        results[dish_id] = per100g
    
    # Summary comparison
    print(f"\n\n{'='*70}")
    print("SUMMARY TABLE - Three Worked Examples")
    print(f"{'='*70}")
    print(f"{'Dish':<25} {'Type':<15} {'kcal/100g':>10} {'P':>6} {'C':>6} {'F':>6} {'MCF':>6}")
    print("-" * 75)
    
    dish_types = {
        "aloo_paratha": "Flatbread",
        "palak_paneer": "Curry",
        "dal_khichdi": "Rice+Dal",
    }
    
    for dish_id in examples:
        dish = recipes[dish_id]
        r = results[dish_id]
        mcf = dish['cooked_total_g'] / dish['raw_total_g']
        print(f"{dish['dish_name']:<25} {dish_types[dish_id]:<15} "
              f"{r['kcal_per100g']:>10.1f} {r['protein_per100g']:>6.1f} "
              f"{r['carbs_per100g']:>6.1f} {r['fat_per100g']:>6.1f} {mcf:>6.2f}")
    
    print(f"\nMCF = Moisture Correction Factor (cooked_weight / raw_weight)")
    print(f"MCF > 1: food absorbed water (rice, dal)")
    print(f"MCF < 1: food lost water (frying, roasting)")
    print("\nThis table documents the calculation only; it is not a validation result.")
