"""
Nutri.In — Nutrition Engine
Computes calories, protein, carbs, fat from dish + grams input.
Uses IFCT 2017 values + custom recipe table with moisture correction.
"""

import json
import os
from typing import Dict, Tuple, Optional

# Path to recipe data
RECIPE_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "recipes", "recipes.json")


def load_recipes(filepath: str = RECIPE_FILE) -> Dict:
    """Load the recipe table from JSON."""
    with open(filepath, "r") as f:
        data = json.load(f)
    # Index by dish_id for fast lookup
    return {dish["dish_id"]: dish for dish in data["dishes"]}


def compute_nutrition(
    dish_id: str,
    cooked_grams: float,
    recipes: Optional[Dict] = None,
    uncertainty_pct: float = 25.0,
) -> Dict:
    """
    Compute nutrition from dish identification and portion weight.

    Args:
        dish_id: Identifier matching recipes.json
        cooked_grams: Estimated cooked weight in grams
        recipes: Pre-loaded recipe dict (optional, loads from file if None)
        uncertainty_pct: Portion uncertainty as percentage (default ±25%, refined in Stage 4)

    Returns:
        Dict with keys: kcal, protein_g, carbs_g, fat_g, kcal_range, grams_range
    """
    if recipes is None:
        recipes = load_recipes()

    if dish_id not in recipes:
        raise ValueError(f"Unknown dish_id: {dish_id}. Available: {list(recipes.keys())}")

    dish = recipes[dish_id]

    # Compute per-100g cooked values from raw ingredients + moisture correction
    cooked_total = dish["cooked_total_g"]

    total_kcal_raw = 0
    total_protein_raw = 0
    total_carbs_raw = 0
    total_fat_raw = 0

    for ing in dish["ingredients"]:
        raw_g = ing["raw_g"]
        total_kcal_raw += (ing["kcal_per100g"] / 100) * raw_g
        total_protein_raw += (ing["protein_per100g"] / 100) * raw_g
        total_carbs_raw += (ing["carbs_per100g"] / 100) * raw_g
        total_fat_raw += (ing["fat_per100g"] / 100) * raw_g

    # Per 100g cooked values (moisture-corrected)
    scale = 100.0 / cooked_total
    kcal_per100g = total_kcal_raw * scale
    protein_per100g = total_protein_raw * scale
    carbs_per100g = total_carbs_raw * scale
    fat_per100g = total_fat_raw * scale

    # Scale to actual portion
    portion_scale = cooked_grams / 100.0
    kcal = kcal_per100g * portion_scale
    protein = protein_per100g * portion_scale
    carbs = carbs_per100g * portion_scale
    fat = fat_per100g * portion_scale

    # Uncertainty range
    factor = uncertainty_pct / 100.0
    grams_low = cooked_grams * (1 - factor)
    grams_high = cooked_grams * (1 + factor)
    kcal_low = kcal * (1 - factor)
    kcal_high = kcal * (1 + factor)

    return {
        "dish_id": dish_id,
        "dish_name": dish["dish_name"],
        "cooked_grams": cooked_grams,
        "kcal": round(kcal, 1),
        "protein_g": round(protein, 1),
        "carbs_g": round(carbs, 1),
        "fat_g": round(fat, 1),
        "kcal_per100g_cooked": round(kcal_per100g, 1),
        "kcal_range": (round(kcal_low, 1), round(kcal_high, 1)),
        "grams_range": (round(grams_low, 1), round(grams_high, 1)),
        "confidence": dish.get("confidence", "unknown"),
        "source": dish.get("source", "unknown"),
    }


if __name__ == "__main__":
    # Quick test
    recipes = load_recipes()
    for dish_id in recipes:
        result = compute_nutrition(dish_id, 200.0, recipes)
        print(f"{result['dish_name']} (200g cooked):")
        print(f"  Calories: {result['kcal']} kcal (range: {result['kcal_range']})")
        print(f"  Protein:  {result['protein_g']}g")
        print(f"  Carbs:    {result['carbs_g']}g")
        print(f"  Fat:      {result['fat_g']}g")
        print()
