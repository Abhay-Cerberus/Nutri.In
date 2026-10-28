# 📊 Nutri.In — Progress Tracker

> **Last updated:** 2026-10-28
> **Current Phase:** Weeks 2–3 — Stage 1: Nutrition Backbone

---

## ✅ Week 0 — Pre-Project Checklist

### Automated Setup (Done by code)

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1 | GitHub repo created with folder structure | ✅ Done | Git initialized, full directory tree created |
| 2 | `.gitignore` configured | ✅ Done | Python, data, weights, IDE, frontend patterns |
| 3 | `README.md` with project overview + repo map | ✅ Done | Covers claims, structure, setup, team roles |
| 4 | `SCOPE.md` template (IN/OUT + dish list table) | ✅ Done | Dish list table to be filled in Week 1 |
| 5 | `FINDINGS.md` experiment log template | ✅ Done | Same-day update rule documented |
| 6 | `requirements.txt` with all dependencies | ✅ Done | PyTorch, timm, DVC, W&B, FastAPI, OpenAI, etc. |
| 7 | `recipes/recipes.json` schema + example entry | ✅ Done | One example (Rajma Curry) showing full structure |
| 8 | `recipes/ifct_lookup.csv` template | ✅ Done | Header row + extraction instructions |
| 9 | `src/nutrition/nutrition.py` skeleton | ✅ Done | grams → kcal/P/C/F with uncertainty range |
| 10 | `tests/test_nutrition.py` unit tests | ✅ Done | 7 tests covering linearity, ranges, edge cases |
| 11 | `benchmark/PROMPTS.md` LLM prompt templates | ✅ Done | 2 variants + constrained refiner prompt |
| 12 | Python `__init__.py` files for all packages | ✅ Done | src/, nutrition/, models/, segmentation/, etc. |
| 13 | `.gitkeep` files for empty directories | ✅ Done | Ensures Git tracks empty folders |
| 14 | DVC initialized (`dvc init`) | ✅ Done | DVC initialized, initial commit made |

### Manual Tasks (Team must do)

| # | Task | Status | Owner | Notes |
|---|------|--------|-------|-------|
| 15 | Weights & Biases account created | ❌ Not Done | All | Create shared W&B project for experiment tracking |
| 16 | Hardware decision finalized | ❌ Not Done | All | Colab Pro (~₹500/mo) vs Kaggle (30h free) vs Lab GPU |
| 17 | Budget items purchased | ❌ Not Done | Data Lead | Kitchen scale ₹300–500, consent forms ₹100, misc ₹200 |
| 18 | Shared Google Drive folder created | ❌ Not Done | Any | Folders: `papers/`, `meeting-notes/`, `dataset-docs/`, `figures/` |
| 19 | Team role assignments confirmed | ❌ Not Done | All | A=Data, B=Models, C=Systems |
| 20 | Guide checkpoint #1 — repo + scope email | ❌ Not Done | All | Show repo + scope confirmation to guide |
| 21 | Push repo to GitHub (remote) | ❌ Not Done | Any | Create GitHub repo and push initial commit |

---

## ✅ Week 1 — Stage 0: Literature & Scope Lock

| # | Task | Status | Owner | Notes |
|---|------|--------|-------|-------|
| 1 | Annotated bibliography (≥12 papers) | ✅ Done | All | 14 papers annotated in `docs/papers/ANNOTATED_BIBLIOGRAPHY.md` |
| 2 | Freeze dish list in `SCOPE.md` (30 dishes) | ✅ Done | Data Lead | 30 dishes selected: 8 curries, 4 rice/dal, 6 breads, 5 South Indian, 5 snacks, 2 kebabs |
| 3 | Download Khana labels + verify class overlap | ✅ Done | Models Lead | Labels (80 classes) + taxonomy saved to `data/raw/khana/`. All 30 dishes verified in Khana |
| 4 | Download IFCT 2017 → extract `ifct_lookup.csv` | ⏳ Partial | Systems Lead | IFCT PDF is present locally; 31 ingredient rows have been transcribed from Table 1 and linked to PDF pages. Remaining non-IFCT ingredients and proxies are marked in `recipes.json` |
| 5 | Related work draft (~1.5 pages) | ✅ Done | All | `docs/papers/RELATED_WORK_DRAFT_v0.md` — covers recognition, portion est., LLM benchmarks |
| 6 | `SCOPE.md` committed with frozen dish list | ✅ Done | Data Lead | Frozen 2026-10-24. Includes portion difficulty ratings + height-prior categories |

---

## 📋 Weeks 2–3 — Stage 1: Nutrition Backbone

| # | Task | Status | Owner | Notes |
|---|------|--------|-------|-------|
| 1 | Recipe collection protocol documented | ✅ Done | Data Lead | Protocol written; actual canteen weighing and recipe sourcing remain team tasks |
| 2 | Build `recipes.json` (≥25 dishes, sourced) | ⚠️ Partial | Data Lead | 30 draft entries exist; all quantities/yields are unmeasured and marked low confidence. Source/variant verification remains |
| 3 | Extract IFCT values → `ifct_lookup.csv` | ⚠️ Partial | Systems Lead | 31 matched Table 1 entries transcribed from the local PDF with physical page references. Besan/rice flour use marked proxies; several ingredients have provisional non-IFCT overrides |
| 4 | Implement `nutrition.py` fully | ✅ Done | Systems Lead | Uses the IFCT lookup, resolves marked overrides, applies cooked-yield scaling, checks invalid inputs, and labels provisional ingredients. Recipe accuracy is not validated |
| 5 | Sanity-check experiment | ⚠️ Partial | Systems Lead | Runner and source-required reference template are ready; no comparison was run because verified cooked-food references have not been added |
| 6 | Replicate Chiplonkar's method (3 dishes) | ⚠️ Partial | Data Lead | `src/nutrition/chiplonkar_method_demo.py` demonstrates moisture adjustment only; provisional recipe values mean this is not a study replication or validation |
| 7 | Unit tests pass with real data | ⚠️ Partial | Systems Lead | 12 standard-library tests pass for lookup loading, calculation, and input checks. Project recipe inputs remain provisional; no measured recipe data has been tested |

---

## 📋 Weeks 3–5 — Stage 2: Weighed Photo Dataset

| # | Task | Status | Owner | Notes |
|---|------|--------|-------|-------|
| 1 | Collection protocol document written | ❌ Not Started | Data Lead | Equipment, naming convention, metadata fields |
| 2 | Collect ≥400 weighed photos | ❌ Not Started | All | ~15 per dish × 30 dishes, varied portions/lighting/angles |
| 3 | Master annotation CSV complete | ❌ Not Started | Data Lead | Zero missing `true_grams` |
| 4 | Data split: Train 250 / Val 100 / Test 100 | ❌ Not Started | Models Lead | Stratified by dish + portion size |
| 5 | Test set checksum committed | ❌ Not Started | Models Lead | `test_set_manifest.sha256` — sacred test set |
| 6 | QA: blur detection + duplicate check | ❌ Not Started | Models Lead | Laplacian variance + perceptual hash |

---

## 📋 Weeks 5–7 — Stage 3: Dish Recognition

| # | Task | Status | Owner | Notes |
|---|------|--------|-------|-------|
| 1 | ResNet-50 baseline on Khana | ❌ Not Started | Models Lead | Proves pipeline works; floor number |
| 2 | ConvNeXt-Small training | ❌ Not Started | Models Lead | Target ≥80% top-1 on Khana test |
| 3 | MobileNetV3 training | ❌ Not Started | Models Lead | Efficiency comparison |
| 4 | Domain-gap experiment | ❌ Not Started | Models Lead | Khana test vs weighed val set |
| 5 | Confusion matrix + per-class accuracy | ❌ Not Started | Models Lead | Flag classes <70% |
| 6 | Inference latency benchmark | ❌ Not Started | Models Lead | CPU + GPU timing table |
| 7 | Model selection decision documented | ❌ Not Started | Models Lead | Speed vs accuracy tradeoff |
| 8 | Top-3 + confidence threshold implemented | ❌ Not Started | Models Lead | <0.7 → user picks |

---

## 📋 Weeks 7–10 — Stage 4: Portion Estimation (Core Contribution)

| # | Task | Status | Owner | Notes |
|---|------|--------|-------|-------|
| 1 | Prior-only baseline | ❌ Not Started | Systems Lead | Serving median per dish → calorie MAE |
| 2 | Geometry layer (GrabCut + ellipse fit) | ❌ Not Started | Systems Lead | Zero-training baseline |
| 3 | Annotate ~200 photos with masks | ❌ Not Started | All | Label Studio / CVAT, ~2 hrs |
| 4 | Fine-tune U-Net/DeepLabV3 segmentation | ❌ Not Started | Models Lead | On Khana + our masks |
| 5 | Portion regressor (ConvNeXt features → grams) | ❌ Not Started | Models Lead | Huber loss, 250 train photos |
| 6 | Fusion grid search | ❌ Not Started | Systems Lead | w1·prior + w2·geo + w3·reg, tune on val |
| 7 | Ablation table complete | ❌ Not Started | Systems Lead | prior / +geo / +reg / full fusion |
| 8 | Bland-Altman + scatter plots | ❌ Not Started | Systems Lead | Predicted vs actual |
| 9 | Failure case gallery (worst 10) | ❌ Not Started | All | Categorize why each failed |

---

## 📋 Weeks 10–12 — Stage 5: LLM Benchmark

| # | Task | Status | Owner | Notes |
|---|------|--------|-------|-------|
| 1 | Prompt variant pre-registered | ❌ Not Started | Systems Lead | Pick ONE before seeing results |
| 2 | `run_llms.py` batch runner | ❌ Not Started | Systems Lead | GPT-4o + Gemini, temp=0, retry logic |
| 3 | `metrics.py` unified metrics | ❌ Not Started | Systems Lead | MAE, MAPE, RMSE, %±20%, macro MAEs |
| 4 | Full benchmark run (all systems, 100 images) | ❌ Not Started | Systems Lead | Pipeline, prior-only, GPT-4o, Gemini |
| 5 | Constrained refiner experiment (30 images) | ❌ Not Started | Systems Lead | User corrections: bounded vs unbounded |
| 6 | Second prompt variant run (robustness) | ❌ Not Started | Systems Lead | Not cherry-picking |
| 7 | Benchmark master table + boxplots | ❌ Not Started | Systems Lead | % errors per system |
| 8 | Error-vs-portion analysis | ❌ Not Started | Systems Lead | Bin by portion size |
| 9 | Qualitative figure (6 images × all systems) | ❌ Not Started | All | Photo, truth, ours, GPT-4o, Gemini |

---

## 📋 Weeks 12–14 — Stage 6: App, Integration & Paper

| # | Task | Status | Owner | Notes |
|---|------|--------|-------|-------|
| 1 | FastAPI `/predict` endpoint | ❌ Not Started | Systems Lead | ≤5s target |
| 2 | Constrained refiner endpoint | ❌ Not Started | Systems Lead | LLM parse → bounded adjust |
| 3 | React frontend | ❌ Not Started | Systems Lead | Upload → results card → chat box |
| 4 | Deploy demo (HF Spaces / lab server) | ❌ Not Started | Systems Lead | Free tier |
| 5 | Paper: Methods §3 | ❌ Not Started | All | Write first |
| 6 | Paper: Results §4 | ❌ Not Started | All | Write second |
| 7 | Paper: Intro §1 | ❌ Not Started | All | Write after methods/results |
| 8 | Paper: Related Work §2 | ❌ Not Started | All | Expand from Stage 0 draft |
| 9 | Paper: Discussion §5 | ❌ Not Started | All | Honest limitations |
| 10 | Internal review + guide feedback | ❌ Not Started | All | Each member reads draft cold |
| 11 | Repo public with README + reproducibility | ❌ Not Started | All | `pip install && python run_benchmark.py` |

---

## 📈 Overall Progress

| Phase | Status | Completion |
|-------|--------|------------|
| Week 0 — Pre-Project Setup | 🔧 In Progress | ~65% (automated done, manual tasks remaining) |
| Week 1 — Literature & Scope | ✅ Mostly Done | ~90% (literature/scope done; IFCT subset extracted, remaining ingredient entries need confirmation) |
| Weeks 2–3 — Nutrition Backbone | ⚠️ In Progress | ~55% (engine and IFCT subset ready; recipe validation and sourced references remain) |
| Weeks 3–5 — Weighed Photos | ❌ Not Started | 0% |
| Weeks 5–7 — Dish Recognition | ❌ Not Started | 0% |
| Weeks 7–10 — Portion Estimation | ❌ Not Started | 0% |
| Weeks 10–12 — LLM Benchmark | ❌ Not Started | 0% |
| Weeks 12–14 — App & Paper | ❌ Not Started | 0% |
