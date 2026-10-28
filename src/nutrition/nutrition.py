"""Nutrition calculation using per-ingredient nutrients and recipe yield.

For each ingredient, the engine uses its IFCT 2017 code when available. A
clearly marked provisional override may be used for foods that are not in the
project's IFCT lookup. Raw nutrient totals are divided by the recipe's cooked
yield to estimate nutrients per 100 g cooked.

This implements the moisture-adjustment calculation discussed by Chiplonkar
and Agte (2007); the estimates here are not validated against lab analyses.
"""

import json
import csv
import math
import os
from typing import Dict, Optional, List, Mapping, Any

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
RECIPE_FILE = os.path.join(PROJECT_ROOT, "recipes", "recipes.json")
IFCT_FILE = os.path.join(PROJECT_ROOT, "recipes", "ifct_lookup.csv")


def load_recipes(filepath: str = RECIPE_FILE) -> Dict:
    """Load the recipe table from JSON, indexed by dish_id."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    dishes = data.get("dishes")
    if not isinstance(dishes, list):
        raise ValueError("recipes.json must contain a 'dishes' list")

    indexed = {}
    for dish in dishes:
        dish_id = dish.get("dish_id")
        if not dish_id:
            raise ValueError("Every recipe must have a non-empty dish_id")
        if dish_id in indexed:
            raise ValueError(f"Duplicate dish_id in recipes.json: {dish_id}")
        indexed[dish_id] = dish
    return indexed


def load_ifct(filepath: str = IFCT_FILE) -> Dict:
    """Load IFCT lookup rows from CSV, ignoring leading comment lines."""
    ifct = {}
    with open(filepath, "r", encoding="utf-8") as f:
        rows = (line for line in f if line.strip() and not line.lstrip().startswith("#"))
        reader = csv.DictReader(rows)
        required = {
            "ifct_code", "food_name", "energy_kcal_per100g",
            "protein_g_per100g", "carbs_g_per100g", "fat_g_per100g",
        }
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(
                f"IFCT CSV is missing required columns: {sorted(required - set(reader.fieldnames or []))}"
            )
        for row in reader:
            code = row["ifct_code"].strip()
            if not code:
                continue
            if code in ifct:
                raise ValueError(f"Duplicate IFCT code in CSV: {code}")
            ifct[code] = {
                "food_name": row["food_name"],
                "kcal": float(row["energy_kcal_per100g"]),
                "protein": float(row["protein_g_per100g"]),
                "carbs": float(row["carbs_g_per100g"]),
                "fat": float(row["fat_g_per100g"]),
                "source": row.get("source", "IFCT 2017"),
                "pdf_page": row.get("pdf_page", ""),
            }
    return ifct


def _non_negative_number(value: Any, field: str) -> float:
    """Return a finite, non-negative number or raise a useful error."""
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be a number") from exc
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{field} must be finite and non-negative")
    return number


def _ingredient_nutrients(ingredient: Mapping[str, Any], ifct: Mapping[str, Any]) -> Dict[str, Any]:
    """Resolve nutrient values from IFCT or an explicit provisional override."""
    code = ingredient.get("ifct_code")
    if code:
        if code not in ifct:
            name = ingredient.get("name", "unnamed ingredient")
            raise ValueError(f"{name} references unknown IFCT code {code!r}")
        values = ifct[code]
        source = f"{values.get('source', 'IFCT 2017')} ({code})"
        if values.get("pdf_page"):
            source += f", PDF page {values['pdf_page']}"
    else:
        values = ingredient.get("nutrition_per100g")
        source = ingredient.get("nutrition_source")
        if not isinstance(values, dict) or not source:
            name = ingredient.get("name", "unnamed ingredient")
            raise ValueError(
                f"{name} needs a valid ifct_code or an explicit nutrition_per100g override and source"
            )

    nutrients = {
        "kcal": _non_negative_number(values.get("kcal"), f"{ingredient.get('name', 'ingredient')} kcal"),
        "protein": _non_negative_number(values.get("protein"), f"{ingredient.get('name', 'ingredient')} protein"),
        "carbs": _non_negative_number(values.get("carbs"), f"{ingredient.get('name', 'ingredient')} carbs"),
        "fat": _non_negative_number(values.get("fat"), f"{ingredient.get('name', 'ingredient')} fat"),
        "source": source,
        "source_note": ingredient.get("source_note", ""),
    }
    return nutrients


def compute_raw_totals(dish: Dict, ifct: Optional[Dict] = None) -> Dict:
    """
    Compute total raw nutrient contributions for a recipe.

    For each ingredient:
      nutrient_contribution = (raw_g / 100) * nutrient_per100g

    Returns dict with total kcal, protein, carbs, fat from raw ingredients.
    """
    if ifct is None:
        ifct = load_ifct()

    ingredients = dish.get("ingredients")
    if not isinstance(ingredients, list) or not ingredients:
        raise ValueError(f"Recipe {dish.get('dish_id', '<unknown>')} has no ingredients")

    total_kcal = 0.0
    total_protein = 0.0
    total_carbs = 0.0
    total_fat = 0.0

    sources = set()
    provisional_ingredients = []

    for ing in ingredients:
        raw_g = _non_negative_number(ing.get("raw_g"), f"{ing.get('name', 'ingredient')} raw_g")
        values = _ingredient_nutrients(ing, ifct)
        total_kcal += (values["kcal"] / 100.0) * raw_g
        total_protein += (values["protein"] / 100.0) * raw_g
        total_carbs += (values["carbs"] / 100.0) * raw_g
        total_fat += (values["fat"] / 100.0) * raw_g
        sources.add(values["source"])
        if not ing.get("ifct_code") or ing.get("source_note"):
            provisional_ingredients.append(ing.get("name", "unnamed ingredient"))

    return {
        "kcal": total_kcal,
        "protein_g": total_protein,
        "carbs_g": total_carbs,
        "fat_g": total_fat,
        "input_sources": sorted(sources),
        "provisional_ingredients": sorted(set(provisional_ingredients)),
    }


def compute_cooked_per100g(dish: Dict, ifct: Optional[Dict] = None) -> Dict:
    """
    Compute per-100g cooked nutrients using recipe yield adjustment.

    cooked_per100g = raw_total_nutrients * (100 / cooked_total_g)

    This is the moisture correction: if cooking adds water (e.g., rice),
    nutrients per 100g decrease; if cooking removes water (e.g., frying),
    nutrients per 100g increase.
    """
    raw_totals = compute_raw_totals(dish, ifct)
    cooked_total = _non_negative_number(dish.get("cooked_total_g"), "cooked_total_g")
    if cooked_total == 0:
        raise ValueError(f"Recipe {dish.get('dish_id', '<unknown>')} must have cooked_total_g > 0")
    scale = 100.0 / cooked_total

    return {
        "kcal_per100g": round(raw_totals["kcal"] * scale, 1),
        "protein_per100g": round(raw_totals["protein_g"] * scale, 1),
        "carbs_per100g": round(raw_totals["carbs_g"] * scale, 1),
        "fat_per100g": round(raw_totals["fat_g"] * scale, 1),
        "input_sources": raw_totals["input_sources"],
        "provisional_ingredients": raw_totals["provisional_ingredients"],
    }


def compute_nutrition(
    dish_id: str,
    cooked_grams: float,
    recipes: Optional[Dict] = None,
    uncertainty_pct: float = 25.0,
    ifct: Optional[Dict] = None,
) -> Dict:
    """
    Compute nutrition from dish identification and portion weight.

    Args:
        dish_id: Identifier matching recipes.json
        cooked_grams: Estimated cooked weight in grams
        recipes: Pre-loaded recipe dict (optional, loads from file if None)
        uncertainty_pct: Portion-mass uncertainty percentage (default 25%). This
            does not include uncertainty in recipe composition or cooking yield.
        ifct: Pre-loaded IFCT lookup table (optional).

    Returns:
        Dict with keys: kcal, protein_g, carbs_g, fat_g, kcal_range, grams_range,
        plus per-100g cooked values and metadata.
    """
    cooked_grams = _non_negative_number(cooked_grams, "cooked_grams")
    uncertainty_pct = _non_negative_number(uncertainty_pct, "uncertainty_pct")
    if uncertainty_pct > 100:
        raise ValueError("uncertainty_pct must be between 0 and 100")

    if recipes is None:
        recipes = load_recipes()

    if dish_id not in recipes:
        raise ValueError(f"Unknown dish_id: {dish_id}. Available: {list(recipes.keys())}")

    dish = recipes[dish_id]
    per100g = compute_cooked_per100g(dish, ifct)

    # Scale to actual portion
    portion_scale = cooked_grams / 100.0
    kcal = per100g["kcal_per100g"] * portion_scale
    protein = per100g["protein_per100g"] * portion_scale
    carbs = per100g["carbs_per100g"] * portion_scale
    fat = per100g["fat_per100g"] * portion_scale

    # Uncertainty range (±uncertainty_pct)
    factor = uncertainty_pct / 100.0
    kcal_low = kcal * (1 - factor)
    kcal_high = kcal * (1 + factor)
    grams_low = cooked_grams * (1 - factor)
    grams_high = cooked_grams * (1 + factor)

    return {
        "dish_id": dish_id,
        "dish_name": dish["dish_name"],
        "cooked_grams": cooked_grams,
        "kcal": round(kcal, 1),
        "protein_g": round(protein, 1),
        "carbs_g": round(carbs, 1),
        "fat_g": round(fat, 1),
        "kcal_per100g_cooked": per100g["kcal_per100g"],
        "protein_per100g_cooked": per100g["protein_per100g"],
        "carbs_per100g_cooked": per100g["carbs_per100g"],
        "fat_per100g_cooked": per100g["fat_per100g"],
        "kcal_range": (round(kcal_low, 1), round(kcal_high, 1)),
        "grams_range": (round(grams_low, 1), round(grams_high, 1)),
        "confidence": dish.get("confidence", "unknown"),
        "source": dish.get("source", "unknown"),
        "input_sources": per100g["input_sources"],
        "provisional_ingredients": per100g["provisional_ingredients"],
        "uncertainty_basis": (
            "Portion mass only; recipe composition and cooked yield uncertainty are not quantified."
        ),
    }


def compute_all_per100g(
    recipes: Optional[Dict] = None,
    ifct: Optional[Dict] = None,
) -> List[Dict]:
    """
    Compute per-100g cooked values for ALL dishes.
    Returns a list of dicts suitable for the sanity-check table.
    """
    if recipes is None:
        recipes = load_recipes()

    results = []
    for dish_id, dish in recipes.items():
        per100g = compute_cooked_per100g(dish, ifct)
        results.append({
            "dish_id": dish_id,
            "dish_name": dish["dish_name"],
            "kcal_per100g": per100g["kcal_per100g"],
            "protein_per100g": per100g["protein_per100g"],
            "carbs_per100g": per100g["carbs_per100g"],
            "fat_per100g": per100g["fat_per100g"],
            "raw_total_g": dish["raw_total_g"],
            "cooked_total_g": dish["cooked_total_g"],
            "mcf": dish["moisture_correction_factor"],
            "confidence": dish["confidence"],
            "source": dish["source"],
            "input_sources": per100g["input_sources"],
            "provisional_ingredients": per100g["provisional_ingredients"],
        })

    return results


if __name__ == "__main__":
    print("=" * 80)
    print("NUTRI.IN - Nutrition Engine - All 30 Dishes")
    print("=" * 80)

    recipes = load_recipes()
    print(f"\nLoaded {len(recipes)} recipes.\n")

    # Print per-100g cooked values for all dishes
    print(f"{'Dish':<25} {'kcal/100g':>10} {'P/100g':>8} {'C/100g':>8} {'F/100g':>8} {'Conf':>8}")
    print("-" * 75)

    all_results = compute_all_per100g(recipes)
    for r in all_results:
        print(f"{r['dish_name']:<25} {r['kcal_per100g']:>10.1f} {r['protein_per100g']:>8.1f} "
              f"{r['carbs_per100g']:>8.1f} {r['fat_per100g']:>8.1f} {r['confidence']:>8}")

    # Example: compute nutrition for a specific dish
    print("\n" + "=" * 80)
    print("Example: Palak Paneer, 200g cooked")
    print("=" * 80)
    result = compute_nutrition("palak_paneer", 200.0, recipes)
    for k, v in result.items():
        print(f"  {k}: {v}")
