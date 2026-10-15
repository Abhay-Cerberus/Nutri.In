# LLM Benchmark Prompt Templates

> **Rule:** Pick ONE prompt variant for the main benchmark BEFORE seeing results (avoid p-hacking).
> The second variant is reported as a robustness check.

---

## Variant A — Structured JSON Output

```
You are a nutrition estimation assistant. Analyze this food image and provide your estimate in the following JSON format:

{
  "dish_name": "<identified dish>",
  "estimated_portion_grams": <number>,
  "calories_kcal": <number>,
  "protein_g": <number>,
  "carbohydrates_g": <number>,
  "fat_g": <number>,
  "confidence": "<low/medium/high>",
  "reasoning": "<brief explanation>"
}

Be specific about the Indian dish you identify. State your assumed portion size explicitly.
```

## Variant B — Free Text

```
Estimate the calories, protein, carbohydrates, and fat in this food image, stating your assumed portion size in grams. Identify the specific Indian dish and explain your reasoning.
```

---

## Pre-Registration

- **Selected variant for main benchmark:** [ ] A / [ ] B — *decide before running*
- **Date of decision:** ___
- **Rationale:** ___

## Constrained Refiner Prompts

```
The user has provided feedback about their meal: "{user_feedback}"

Current estimate:
- Dish: {dish_name}
- Portion: {estimated_grams}g
- Calories: {calories} kcal

Parse the user's intent and suggest an adjustment. Respond in JSON:
{
  "adjustment_type": "portion_increase|portion_decrease|preparation_change|no_change",
  "adjustment_factor": <float between 0.7 and 1.3>,
  "reasoning": "<explanation>"
}
```
