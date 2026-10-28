"""Optional sanity check against externally sourced cooked-food references.

The reference file is intentionally empty until someone records an actual
source and access URL for each comparison. No guessed reference values are
used in this experiment.
"""

import csv
import math
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)
from src.nutrition.nutrition import load_ifct, load_recipes, compute_all_per100g

REFERENCE_FILE = os.path.join(PROJECT_ROOT, "recipes", "reference_values.csv")


def load_reference_values(filepath=REFERENCE_FILE):
    """Read sourced cooked-food references from the team-maintained CSV."""
    if not os.path.exists(filepath):
        return {}

    with open(filepath, "r", encoding="utf-8", newline="") as stream:
        lines = (line for line in stream if line.strip() and not line.lstrip().startswith("#"))
        reader = csv.DictReader(lines)
        required = {"dish_id", "kcal_per100g", "source", "reference_url"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"Reference CSV must contain columns: {sorted(required)}")

        references = {}
        for row in reader:
            dish_id = (row.get("dish_id") or "").strip()
            kcal_text = (row.get("kcal_per100g") or "").strip()
            if not dish_id and not kcal_text:
                continue
            if not dish_id or not kcal_text:
                raise ValueError("Each reference row needs both dish_id and kcal_per100g")
            if not (row.get("source") or "").strip() or not (row.get("reference_url") or "").strip():
                raise ValueError(f"Reference for {dish_id} needs source and reference_url")
            if dish_id in references:
                raise ValueError(f"Duplicate reference row for {dish_id}")
            kcal = float(kcal_text)
            if not math.isfinite(kcal) or kcal <= 0:
                raise ValueError(f"Reference kcal_per100g for {dish_id} must be positive and finite")
            references[dish_id] = {
                "kcal_per100g": kcal,
                "source": row["source"].strip(),
                "reference_url": row["reference_url"].strip(),
                "notes": (row.get("notes") or "").strip(),
            }
    return references


def run_sanity_check(references=None, threshold_pct=25.0):
    """Compare estimates to sourced values, when the reference CSV has rows."""
    recipes = load_recipes()
    ifct = load_ifct()
    results = compute_all_per100g(recipes, ifct)
    if references is None:
        references = load_reference_values()

    print("SANITY CHECK - computed vs. sourced cooked-food references (kcal/100 g)")
    print("Recipe quantities and yields are provisional; results are not validated.")
    print(f"\n{'Dish':<25} {'Ours':>9} {'Ref':>9} {'Diff':>9} {'Status':<28}")
    print("-" * 84)

    flagged = []
    compared = 0
    for result in results:
        reference = references.get(result["dish_id"])
        if reference is None:
            print(f"{result['dish_name']:<25} {result['kcal_per100g']:>9.1f} {'-':>9} {'-':>9} {'reference pending':<28}")
            continue

        ref_kcal = reference["kcal_per100g"]
        diff_pct = (result["kcal_per100g"] - ref_kcal) / ref_kcal * 100.0
        compared += 1
        status = "investigate" if abs(diff_pct) > threshold_pct else "within threshold"
        print(f"{result['dish_name']:<25} {result['kcal_per100g']:>9.1f} {ref_kcal:>9.1f} {diff_pct:>+8.1f}% {status:<28}")
        if abs(diff_pct) > threshold_pct:
            flagged.append({
                "dish_id": result["dish_id"],
                "dish": result["dish_name"],
                "ours": result["kcal_per100g"],
                "reference": ref_kcal,
                "difference_pct": diff_pct,
                "source": reference["source"],
                "reference_url": reference["reference_url"],
            })

    pending = len(results) - compared
    print("-" * 84)
    print(f"Compared: {compared}; reference pending: {pending}; flagged above {threshold_pct:g}%: {len(flagged)}")
    if not compared:
        print("No validation comparison was run. Add sourced rows to recipes/reference_values.csv first.")
    return flagged


if __name__ == "__main__":
    run_sanity_check()
