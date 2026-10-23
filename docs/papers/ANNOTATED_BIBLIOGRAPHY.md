# Annotated Bibliography

> **Project:** Nutri.In — Portion-Aware Indian Food Nutrition Estimator
> **Last updated:** 2026-10-24
> **Minimum requirement:** 12 entries ✅ (14 entries below)

---

## 1. Khana Dataset — Prabhu (2025)

**Citation:** Prabhu, O. (2025). *Khana: A Comprehensive Indian Cuisine Dataset.* arXiv:2509.06006.

**Problem:** Existing food recognition datasets (Food-101, ISIA Food-500) are dominated by Western cuisines, leaving Indian food poorly represented. Models trained on these datasets generalize poorly to Indian dishes.

**Method:** Web-scraped and curated 131,000+ images across 80 Indian food classes organized in a hierarchical taxonomy (category → dish → variety). Provides train/val/test splits (70/15/15) and baseline benchmarks.

**Dataset:** Khana — 131K images, 80 classes, covering breakfast, curries, snacks, sweets, beverages.

**Metrics:** Top-1 accuracy, Top-5 accuracy.

**Result:** ConvNeXt-Small baseline achieves 86.72% Top-1 / 97.58% Top-5 accuracy.

**Limitation:** Images are web-scraped (not weighed), no portion/nutrition labels, no segmentation masks for all classes. Dataset doesn't cover portion size variation systematically.

**What we borrow:** Primary classification dataset for training our dish recognition model. We fine-tune on Khana's 80 classes, then evaluate domain gap on our weighed photos.

---

## 2. IFCT 2017 — Longvah et al. (2017)

**Citation:** Longvah, T., Ananthan, R., Bhaskarachary, K., & Venkaiah, K. (2017). *Indian Food Composition Tables.* National Institute of Nutrition, ICMR, Hyderabad.

**Problem:** India lacked a comprehensive, analytically derived food composition database. Prior tables (Gopalan et al., 1971) were outdated and covered fewer nutrients.

**Method:** Laboratory analysis of 528 key foods sampled compositely across six geographical regions of India, measuring >150 nutrient components per food item (proximate, vitamins, minerals, amino acids, fatty acids, carotenoids, polyphenols, anti-nutritional factors).

**Dataset:** 528 foods across 13 food groups, all in raw/edible form.

**Metrics:** Analytical accuracy validated against certified reference materials.

**Result:** First comprehensive, region-representative Indian food composition database with 151 nutrient components per entry.

**Limitation:** Values are for **raw ingredients only** — no cooked-dish entries. Requires moisture correction (Chiplonkar method) to convert to cooked values. Some processed/prepared foods are absent.

**What we borrow:** Foundation of our nutrition engine. Every ingredient in `recipes.json` maps to IFCT codes for raw kcal, protein, carbs, fat per 100g. We apply moisture correction to derive cooked per-100g values.

---

## 3. Chiplonkar & Agte — Moisture Correction (2007)

**Citation:** Chiplonkar, S. A., & Agte, V. V. (2007). *Extent of error in estimating nutrient intakes from food tables versus laboratory estimates of cooked foods.* Asia Pacific Journal of Clinical Nutrition, 16(2), 227–239.

**Problem:** Nutritional epidemiology depends on food composition tables (FCTs) that report raw values, but humans eat cooked food. How much error does moisture-based indirect estimation introduce compared to direct laboratory analysis?

**Method:** Evaluated 104 individual cooked Indian foods and 92 composite meals. Compared indirect estimation (raw FCT values × moisture correction factor) against direct chemical analysis of cooked samples.

**Dataset:** 104 cooked Indian foods + 92 composite meals with paired indirect/direct nutrient analyses.

**Metrics:** Agreement between estimated (E) and measured (M) values; percentage deviation.

**Result:** Macronutrient estimates (protein, fat, carbs) are reliable within **±5%** at the individual food level using moisture correction. However, cumulative daily intake errors can reach 27%. Micronutrient agreement is poor (thermal degradation, leaching).

**Limitation:** Only validates macronutrients reliably. Cooking-method-specific retention factors (e.g., deep frying vs. pressure cooking) are not fully modeled. Study is from 2007 — pre-IFCT 2017.

**What we borrow:** Core methodology for our nutrition engine. We use their moisture correction approach: (raw_total_weight / cooked_total_weight) × raw nutrient values = cooked per-100g values. Their ±5% error bound for macros is our validation target. The methi paratha worked example is our template.

---

## 4. JMIR Review — AI-Based Dietary Assessment (2023)

**Citation:** Lu, Y., Stathopoulou, T., Vasiloglou, M. F., et al. (2023). *Image-Based Dietary Assessment: A Systematic Review.* Journal of Medical Internet Research (JMIR), various related venues.

**Problem:** Manual dietary logging (24-hour recalls, food diaries) suffers from user burden, underreporting, and memory bias. Can AI-based image analysis automate and improve dietary assessment?

**Method:** Systematic review of deep-learning-based image-assisted dietary assessment (IADA) systems, categorizing by pipeline stages: image acquisition → food detection/classification → portion estimation → nutrient mapping.

**Dataset:** Review covers multiple datasets (Food-101, ECUST, UEC-Food, Nutrition5k, etc.).

**Metrics:** Classification accuracy, portion estimation MAE, calorie estimation error across reviewed systems.

**Result:** Food classification accuracy exceeds 90% in controlled settings, but portion estimation remains the key bottleneck. Real-world accuracy drops due to occlusion, mixed dishes, and hidden ingredients. Multi-modal approaches (image + text + wearable) show promise.

**Limitation:** Most reviewed systems target Western cuisines. Indian food — with its gravy-based curries, thalis, and high visual similarity between dishes — is underrepresented. Few systems validate against weighed ground truth.

**What we borrow:** Frames our problem statement: portion estimation is the bottleneck. Confirms the gap in Indian food coverage. Our pipeline directly addresses these limitations with weighed photos and IFCT-backed nutrition.

---

## 5. Nutrition5k — Thames et al. (2021)

**Citation:** Thames, Q., Karber, A., Norris, B., et al. (2021). *Nutrition5k: Towards Automatic Nutritional Understanding of Generic Food.* CVPR 2021. Google Research.

**Problem:** Prior food datasets support classification but not nutritional regression (calories, macros from images). No large-scale dataset provides per-plate weighed ground truth with multi-view captures.

**Method:** Captured 5,006 real plates from Google cafeterias using overhead RGB-D cameras and 4 rotating side-angle video streams. Each dish has ingredient-level mass (measured during incremental assembly), total calories, and macronutrient breakdown from USDA values.

**Dataset:** 5,006 plates, RGB + depth, with ingredient lists, per-ingredient mass, total kcal/P/C/F.

**Metrics:** Calorie MAE, macro MAEs for regression models using overhead images and side-angle videos.

**Result:** Models combining RGB features with depth data can predict calories within practical error margins. Demonstrates feasibility of vision-based nutrition regression at scale.

**Limitation:** Western/cafeteria food only (Google campus). Requires specialized depth sensors not available in typical smartphone setups. Not applicable to Indian cuisine without domain adaptation.

**What we borrow:** Methodological inspiration for our weighed photo collection protocol. Their incremental weighing approach and per-plate ground truth standard inform our collection design. We adapt to Indian food with smartphone-only captures (no depth sensor).

---

## 6. GPT-4V Food Calorie Estimation Evaluation (2024)

**Citation:** Ahn, J., Kim, J., et al. (2024). *Evaluation of ChatGPT-4 Vision for Dietary Assessment: Analysis of Meal Photographs.* Nutrients, 16(x). (and related IEEE/Cambridge studies)

**Problem:** Multimodal LLMs (GPT-4V) can identify foods from images with high precision (~90–93%), but how accurate are their calorie and macronutrient point estimates?

**Method:** Fed standardized, weighed meal photographs to GPT-4V with structured prompts requesting calorie/macro estimates. Compared outputs against lab-verified nutritional values. Evaluated portion-size dependency.

**Dataset:** Weighed food photographs from national dietary surveys and standardized meal databases.

**Metrics:** MAPE (20–35%), ICC (0.31–0.67 vs. dietitians), Spearman correlation for relative ranking.

**Result:** GPT-4V achieves high food identification accuracy but **systematically underestimates** calories for medium/large portions (p < 0.001). Relative ranking is adequate (can say which meal is heavier), but absolute calorie counts are unreliable (20–35% MAPE). Hidden ingredients (oils, butter) cause largest errors.

**Limitation:** Tested primarily on Western food. No Indian food benchmark exists. No portion-aware grounding — the model guesses portion sizes without physical reference.

**What we borrow:** Direct comparison target for our benchmark (Stage 5). Their finding of systematic underestimation on large portions motivates our portion-aware pipeline. We expect to show our bounded estimates outperform GPT-4V on Indian food, especially for unusual portion sizes.

---

## 7. Gemini Vision for Food Assessment (2024–2025)

**Citation:** Various benchmark reports and evaluations of Google Gemini (Pro/Flash) for food nutrition estimation (2024–2025).

**Problem:** How does Google's Gemini compare to GPT-4V for zero-shot food calorie estimation? Can frontier multimodal models serve as practical nutrition trackers?

**Method:** Zero-shot evaluation on standardized meal images (including Nutrition5k), requesting structured JSON outputs with dish name, portion, and macro estimates. Compared against lab-measured ground truth.

**Dataset:** Standardized meal photographs, some from Nutrition5k.

**Metrics:** Per-dish median absolute error (~50–60 kcal), ~65% of predictions within 100 kcal of truth, accuracy tiers up to ~74.6%.

**Result:** Gemini performs competitively with GPT-4V, showing similar strengths in food identification and similar weaknesses in absolute calorie quantification. Hidden fats and complex mixed dishes remain primary failure modes. Fat estimation errors are typically higher than protein/carb errors.

**Limitation:** Same fundamental limitation as GPT-4V — no physical grounding for portion estimation. Performance on Indian food is unverified. Complex homemade dishes degrade accuracy significantly.

**What we borrow:** Second LLM baseline for our benchmark. Comparing both GPT-4o and Gemini against our pipeline on identical Indian food test images is the core of our Stage 5 contribution.

---

## 8. Food Portion Estimation via 3D Object Scaling — Vinod et al. (CVPRW 2024)

**Citation:** Vinod, G., He, J., Shao, Z., & Zhu, F. (2024). *Food Portion Estimation via 3D Object Scaling.* CVPR Workshop 2024. Purdue University.

**Problem:** Monocular food portion estimation is ill-posed — a 2D image hides depth, thickness, and actual mass. How to estimate volume without depth sensors?

**Method:** Uses 3D food models + physical reference objects in the scene. Estimates camera pose and food orientation from 2D, scales the 3D asset using the reference object, and reconstructs the eating occasion to determine volume/weight/energy. Released SimpleFood45 dataset.

**Dataset:** SimpleFood45 — 45 food categories with 3D models.

**Metrics:** Volume estimation error, energy estimation MAE.

**Result:** Reference-object-based scaling significantly improves portion estimation accuracy compared to direct pixel-to-volume regression.

**Limitation:** Requires 3D food model library (not available for Indian dishes). Reference object must be visible and recognized. Computational overhead for 3D reconstruction.

**What we borrow:** Validates our use of a reference object (₹5 coin in every photo). Our simpler approach (2D geometry + density priors) is more deployable, but their 3D results provide a ceiling comparison. Motivates our geometry layer design.

---

## 9. MFP3D: Monocular Food Portion Estimation — Ma et al. (ICPR 2024)

**Citation:** Ma, J., et al. (2024). *MFP3D: Monocular Food Portion Estimation Leveraging 3D Point Clouds.* ICPR 2024. Purdue University.

**Problem:** Multi-view and depth sensors improve portion estimation but are impractical for consumer apps. Can a single RGB image suffice?

**Method:** Generates 3D point clouds from single RGB images via a reconstruction module, fuses 2D + 3D features, and regresses to volume/energy via a deep MLP. Tested on MetaFood3D dataset.

**Dataset:** MetaFood3D — food items with 3D point cloud ground truth.

**Metrics:** Volume MAE, energy MAE.

**Result:** Achieves competitive accuracy to multi-view approaches using only monocular input. Point cloud reconstruction captures food height and shape information lost in 2D.

**Limitation:** Requires paired 3D training data (MetaFood3D), which doesn't include Indian foods. Point cloud generation adds inference latency.

**What we borrow:** Confirms that single-image portion estimation is feasible. Our approach trades 3D reconstruction for dish-specific priors (height categories: liquid/pooled/mounded/flat) + regression, which is faster and more interpretable for our 30-dish scope.

---

## 10. ConvNeXt — Liu et al. (2022)

**Citation:** Liu, Z., Mao, H., Wu, C.-Y., et al. (2022). *A ConvNet for the 2020s.* CVPR 2022. Meta/FAIR.

**Problem:** Vision Transformers (ViTs) had overtaken CNNs on image classification benchmarks. Can a modernized CNN architecture match or exceed ViTs using only standard ConvNet primitives?

**Method:** Systematically modernized ResNet-50 with design choices borrowed from Swin Transformer: patchify stem, inverted bottleneck, larger kernels (7×7), LayerNorm, GELU, fewer activations. Produced ConvNeXt family (Tiny/Small/Base/Large/XLarge).

**Dataset:** Evaluated on ImageNet-1K, ImageNet-22K, COCO detection/segmentation, ADE20K semantic segmentation.

**Metrics:** Top-1 accuracy (ImageNet), AP (COCO), mIoU (ADE20K).

**Result:** ConvNeXt-Small: 83.1% Top-1 on ImageNet-1K (matching Swin-T). Scales to 87.8% with ImageNet-22K pretraining. Competitive with ViTs on detection and segmentation without attention mechanisms.

**Limitation:** Still requires large pretraining datasets. No food-specific training. Larger variants (Base/Large) need significant GPU memory.

**What we borrow:** Primary backbone for our dish classifier (ConvNeXt-Small) and portion regression feature extractor. Khana paper validates 86.72% Top-1 with ConvNeXt-S on Indian food. We inherit their pretrained weights and fine-tune.

---

## 11. MobileNetV3 — Howard et al. (2019)

**Citation:** Howard, A., Sandler, M., Chen, B., et al. (2019). *Searching for MobileNetV3.* ICCV 2019. Google.

**Problem:** Deploying high-accuracy classification models on mobile/edge devices is constrained by latency and memory. How to achieve the best accuracy under strict computational budgets?

**Method:** Neural Architecture Search (NAS) with NetAdapt, combined with novel architecture elements: squeeze-and-excite blocks, h-swish activation, redesigned last stage for efficiency. Two variants: MobileNetV3-Large and MobileNetV3-Small.

**Dataset:** ImageNet-1K.

**Metrics:** Top-1 accuracy vs. latency (ms) on mobile CPU.

**Result:** MobileNetV3-Large: 75.2% Top-1 on ImageNet-1K at 66ms latency on Pixel phone. Significant speedup over MobileNetV2 with higher accuracy.

**Limitation:** Lower absolute accuracy than ConvNeXt/ViT. Feature representations may be weaker for fine-grained Indian food distinctions (dal variants, paneer dishes).

**What we borrow:** Efficiency comparison model. If MobileNetV3 accuracy is within ~3% of ConvNeXt on our task, we ship it in the app for faster inference (the plan's decision rule). Provides the latency vs. accuracy tradeoff table for the paper.

---

## 12. U-Net — Ronneberger et al. (2015)

**Citation:** Ronneberger, O., Fischer, P., & Brox, T. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation.* MICCAI 2015.

**Problem:** Semantic segmentation requires both spatial localization and contextual understanding. Biomedical imaging has limited training data — how to segment accurately with few annotated samples?

**Method:** Encoder-decoder architecture with skip connections that concatenate high-resolution features from the encoder to the decoder. Symmetric contracting (encoder) and expansive (decoder) paths enable precise localization with context.

**Dataset:** Originally on ISBI cell segmentation (30 training images). Since adopted across domains.

**Metrics:** IoU, pixel accuracy, Warping Error on cell segmentation benchmarks.

**Result:** Won ISBI 2015 cell tracking challenge. Demonstrated that skip connections + data augmentation enable high-quality segmentation from very few annotated images.

**Limitation:** Original U-Net uses basic VGG-style encoder. Modern variants (U-Net++ , Attention U-Net) improve on it. No food-domain pretraining.

**What we borrow:** Architecture for food/plate segmentation in our portion estimation pipeline (Stage 4). We fine-tune on ~200 annotated food masks + Khana segmentation labels. Compare against GrabCut baseline to justify the trained model.

---

## 13. End-to-End Food Portion Estimation from Monocular Image — Shao et al. (ICME 2023)

**Citation:** Shao, Z., et al. (2023). *An End-to-end Food Portion Estimation Framework Based on Shape Reconstruction from Monocular Image.* ICME 2023. Purdue University.

**Problem:** Most portion estimation systems are multi-stage and require explicit 3D inputs or reference objects. Can an end-to-end deep learning pipeline predict food volume directly from a single RGB image?

**Method:** Uses a generative model to recover 3D voxel representations from monocular RGB images. The voxel volume is then mapped to weight/calories. Tested on Nutrition5k without active depth sensors at inference.

**Dataset:** Nutrition5k (5,006 plates with ground truth calories).

**Metrics:** Volume estimation error, calorie MAE.

**Result:** Demonstrates that end-to-end voxel reconstruction from monocular input is feasible, achieving reasonable calorie estimates without depth sensors.

**Limitation:** Computationally expensive voxel reconstruction. Trained on Western cafeteria food — domain gap to Indian food. Requires large paired training data.

**What we borrow:** Validates the feasibility of monocular portion estimation. Our approach is lighter-weight (prior + geometry + regression fusion) but targets the same goal. Their Nutrition5k-based evaluation is a methodological reference for our Stage 4 design.

---

## 14. Indian Nutrient Databank (INDB) — Anuvaad Solutions

**Citation:** Anuvaad Solutions. *Indian Nutrient Databank (INDB).* Open-access resource. Available at anuvaad.org.in.

**Problem:** IFCT 2017 covers raw ingredients but not cooked dishes. Nutritionists and apps need cooked-dish nutritional profiles for Indian recipes.

**Method:** Computes nutrient profiles for 1,014+ common regional Indian recipes using IFCT 2017 raw values as the foundation, applying yield factors, moisture retention, and cooking-loss adjustments.

**Dataset:** 1,014 Indian recipes with computed nutritional values.

**Metrics:** Derived from IFCT 2017 analytical values; validated against standard dietary practices.

**Result:** First large-scale open-access Indian cooked-dish nutrient database bridging the raw-to-cooked gap.

**Limitation:** Computed (not lab-verified) values — quality depends on recipe accuracy and correction factor assumptions. Regional recipe variants may differ from defaults.

**What we borrow:** Cross-validation resource for our nutrition engine. We compare our computed cooked per-100g values against INDB entries for the same dishes as a secondary sanity check (alongside IFCT cooked entries and MyFitnessPal). Also validates that recipe-based nutrient estimation is an accepted methodology.

---

## Summary Table — Datasets & Resources

| # | Resource | Type | Size | Indian? | We Use For |
|---|----------|------|------|---------|------------|
| 1 | Khana | Image dataset | 131K images, 80 classes | ✅ | Dish classifier training |
| 2 | IFCT 2017 | Nutrient database | 528 foods, 151 components | ✅ | Raw ingredient → nutrition lookup |
| 3 | INDB | Recipe database | 1,014 recipes | ✅ | Sanity check / cross-validation |
| 4 | Nutrition5k | Image+nutrition dataset | 5,006 plates, RGB-D | ❌ Western | Methodology reference |
| 5 | SimpleFood45 | 3D food models | 45 categories | ❌ Western | Ceiling comparison for portion est. |
| 6 | MetaFood3D | 3D point clouds | Food items with 3D GT | ❌ Western | Methodology reference |
| 7 | Our weighed photos | Image+weight dataset | ~450 target, 30 dishes | ✅ | Portion regression training + benchmark |
