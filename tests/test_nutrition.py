"""Tests for IFCT loading and the deterministic nutrition calculation."""

import os
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from src.nutrition.nutrition import (
    compute_all_per100g,
    compute_cooked_per100g,
    compute_nutrition,
    compute_raw_totals,
    load_ifct,
    load_recipes,
)
from src.nutrition.sanity_check import load_reference_values


class NutritionEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipes = load_recipes()
        cls.ifct = load_ifct()

    def test_loads_all_frozen_dishes(self):
        expected = {
            "aloo_gobi", "aloo_mutter", "palak_paneer", "paneer_masala",
            "chana_masala", "bhindi_masala", "anda_curry", "fish_curry",
            "rajma_chawal", "biryani", "dal_khichdi", "navratan_korma",
            "chapati", "aloo_paratha", "chole_bhature", "puri_bhaji",
            "garlic_naan", "amritsari_kulcha", "masala_dosa", "idli",
            "medu_vada", "uttapam", "poha", "samosa", "vada_pav",
            "pav_bhaji", "dhokla", "onion_pakoda", "seekh_kebab",
            "hara_bhara_kabab",
        }
        self.assertEqual(set(self.recipes), expected)

    def test_ifct_lookup_reads_header_after_comments(self):
        self.assertEqual(len(self.ifct), 31)
        self.assertAlmostEqual(self.ifct["A015"]["kcal"], 356.4)
        self.assertAlmostEqual(self.ifct["L003"]["protein"], 18.86)
        self.assertAlmostEqual(self.ifct["L003"]["fat"], 14.78)
        self.assertEqual(self.ifct["A015"]["pdf_page"], "41")

    def test_every_recipe_ingredient_has_explicit_data_source(self):
        for dish_id, dish in self.recipes.items():
            for ingredient in dish["ingredients"]:
                if ingredient.get("ifct_code"):
                    self.assertIn(ingredient["ifct_code"], self.ifct, dish_id)
                else:
                    self.assertIn("nutrition_per100g", ingredient, dish_id)
                    self.assertTrue(ingredient.get("nutrition_source"), dish_id)
                    self.assertTrue(ingredient.get("source_note"), dish_id)

    def test_recipe_weights_and_yield_factors_are_consistent(self):
        for dish_id, dish in self.recipes.items():
            raw_total = sum(ingredient["raw_g"] for ingredient in dish["ingredients"])
            self.assertAlmostEqual(dish["raw_total_g"], raw_total, msg=dish_id)
            expected_mcf = dish["cooked_total_g"] / raw_total
            self.assertAlmostEqual(dish["moisture_correction_factor"], expected_mcf, delta=0.011, msg=dish_id)

    def test_raw_totals_resolve_values_from_ifct_lookup(self):
        dish = {
            "dish_id": "one_hundred_grams_rice",
            "ingredients": [{"name": "Rice", "raw_g": 100, "ifct_code": "A015"}],
        }
        totals = compute_raw_totals(dish, self.ifct)
        self.assertAlmostEqual(totals["kcal"], 356.4)
        self.assertAlmostEqual(totals["protein_g"], 7.94)
        self.assertAlmostEqual(totals["carbs_g"], 78.24)
        self.assertAlmostEqual(totals["fat_g"], 0.52)

    def test_moisture_adjustment_formula(self):
        dish = {
            "dish_id": "test_recipe",
            "cooked_total_g": 200,
            "ingredients": [{"name": "Rice", "raw_g": 100, "ifct_code": "A015"}],
        }
        values = compute_cooked_per100g(dish, self.ifct)
        self.assertAlmostEqual(values["kcal_per100g"], 178.2)
        self.assertAlmostEqual(values["protein_per100g"], 4.0)
        self.assertAlmostEqual(values["carbs_per100g"], 39.1)
        self.assertAlmostEqual(values["fat_per100g"], 0.3)

    def test_provisional_recipe_results_are_labeled(self):
        result = compute_nutrition("chapati", 35, self.recipes, ifct=self.ifct)
        self.assertGreater(result["kcal"], 0)
        self.assertEqual(result["confidence"], "low")
        self.assertIn("Oil", result["provisional_ingredients"])
        self.assertIn("not quantified", result["uncertainty_basis"])

    def test_computation_is_linear_and_zero_portion_is_zero(self):
        one = compute_nutrition("idli", 40, self.recipes, ifct=self.ifct)
        two = compute_nutrition("idli", 80, self.recipes, ifct=self.ifct)
        zero = compute_nutrition("idli", 0, self.recipes, ifct=self.ifct)
        self.assertAlmostEqual(two["kcal"], 2 * one["kcal"], places=1)
        self.assertEqual(zero["kcal"], 0.0)
        self.assertEqual(zero["protein_g"], 0.0)

    def test_unknown_dish_and_invalid_portion_raise(self):
        with self.assertRaises(ValueError):
            compute_nutrition("unknown", 100, self.recipes, ifct=self.ifct)
        with self.assertRaises(ValueError):
            compute_nutrition("idli", -1, self.recipes, ifct=self.ifct)
        with self.assertRaises(ValueError):
            compute_nutrition("idli", 100, self.recipes, uncertainty_pct=101, ifct=self.ifct)

    def test_invalid_cooked_yield_raises(self):
        dish = {"dish_id": "bad_yield", "cooked_total_g": 0,
                "ingredients": [{"name": "Rice", "raw_g": 100, "ifct_code": "A015"}]}
        with self.assertRaises(ValueError):
            compute_cooked_per100g(dish, self.ifct)

    def test_compute_all_returns_every_dish(self):
        self.assertEqual(len(compute_all_per100g(self.recipes, self.ifct)), len(self.recipes))

    def test_no_unsourced_sanity_references_are_preloaded(self):
        self.assertEqual(load_reference_values(), {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
