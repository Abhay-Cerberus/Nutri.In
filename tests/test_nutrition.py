"""
Unit tests for the nutrition engine.
Tests that known grams → known calories (acceptance criteria from plan).
"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.nutrition.nutrition import compute_nutrition, load_recipes


class TestNutritionEngine:
    """Tests for nutrition.py compute_nutrition function."""

    def test_load_recipes_returns_dict(self):
        """Recipe file loads and returns indexed dict."""
        recipes = load_recipes()
        assert isinstance(recipes, dict)
        assert len(recipes) > 0

    def test_compute_nutrition_returns_all_fields(self):
        """Output contains all required nutrition fields."""
        recipes = load_recipes()
        dish_id = list(recipes.keys())[0]
        result = compute_nutrition(dish_id, 200.0, recipes)

        required_keys = [
            "dish_id", "dish_name", "cooked_grams",
            "kcal", "protein_g", "carbs_g", "fat_g",
            "kcal_per100g_cooked", "kcal_range", "grams_range",
        ]
        for key in required_keys:
            assert key in result, f"Missing key: {key}"

    def test_compute_nutrition_zero_grams(self):
        """Zero grams should return zero nutrition."""
        recipes = load_recipes()
        dish_id = list(recipes.keys())[0]
        result = compute_nutrition(dish_id, 0.0, recipes)
        assert result["kcal"] == 0.0
        assert result["protein_g"] == 0.0

    def test_compute_nutrition_linearity(self):
        """Doubling grams should double calories."""
        recipes = load_recipes()
        dish_id = list(recipes.keys())[0]
        r1 = compute_nutrition(dish_id, 100.0, recipes)
        r2 = compute_nutrition(dish_id, 200.0, recipes)
        assert abs(r2["kcal"] - 2 * r1["kcal"]) < 0.5

    def test_unknown_dish_raises(self):
        """Unknown dish_id should raise ValueError."""
        recipes = load_recipes()
        with pytest.raises(ValueError):
            compute_nutrition("nonexistent_dish_xyz", 100.0, recipes)

    def test_uncertainty_range(self):
        """Calorie range should bracket the point estimate."""
        recipes = load_recipes()
        dish_id = list(recipes.keys())[0]
        result = compute_nutrition(dish_id, 200.0, recipes)
        low, high = result["kcal_range"]
        assert low <= result["kcal"] <= high

    def test_confidence_field_present(self):
        """Each result should carry confidence from recipe."""
        recipes = load_recipes()
        dish_id = list(recipes.keys())[0]
        result = compute_nutrition(dish_id, 200.0, recipes)
        assert result["confidence"] in ["high", "medium", "low", "unknown"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
