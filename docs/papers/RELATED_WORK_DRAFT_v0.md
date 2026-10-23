# Related Work — Draft v0

> **Status:** Draft v0 — living document, grows as we read.
> **Target:** ~1.5 pages in final paper format.
> **Last updated:** 2026-10-24

---

## 2. Related Work

Our work intersects three research areas: (i) food image recognition, (ii) portion and calorie estimation, and (iii) the emerging use of multimodal large language models (LLMs) for dietary assessment. We review each in turn, highlighting the gap our work addresses: the absence of a weighed, portion-aware benchmark for Indian food.

### 2.1 Food Image Recognition

Deep learning has transformed food recognition from a niche pattern recognition task into a near-solved problem for well-represented cuisines. Datasets such as Food-101 (Bossard et al., 2014), ISIA Food-500 (Min et al., 2020), and UEC-Food-256 (Kawano & Yanai, 2015) have driven classification accuracy above 90% using modern CNN and Vision Transformer architectures. However, these datasets are overwhelmingly Western-centric, with limited or no coverage of the regional diversity in Indian cuisine — a food tradition spanning hundreds of visually similar dishes that differ primarily in spice composition and preparation method rather than visual appearance.

The Khana dataset (Prabhu, 2025) directly addresses this gap, providing 131,000+ web-curated images across 80 Indian food classes organized in a hierarchical taxonomy. A ConvNeXt-Small (Liu et al., 2022) baseline achieves 86.72% top-1 accuracy on Khana's test split, establishing a competitive benchmark for Indian food classification. However, Khana provides no portion-size annotations, no weighed ground truth, and no nutrition labels — limiting its utility to the recognition stage of a dietary assessment pipeline.

We adopt ConvNeXt-Small as our primary classifier architecture, following Khana's baseline, and supplement it with MobileNetV3 (Howard et al., 2019) for an efficiency comparison relevant to mobile deployment. Critically, we evaluate both models not only on Khana's test split but also on our own weighed photo set, measuring the **domain gap** between web-scraped training images and real institutional dining conditions — a finding relevant to any deployment of food recognition in the wild.

### 2.2 Portion and Calorie Estimation

While food recognition has matured, portion estimation remains the primary bottleneck in automated dietary assessment (Lu et al., 2023; JMIR systematic review). The core challenge is that a single 2D photograph fundamentally lacks depth, density, and mass information.

**Reference-based approaches** use known objects (plates, coins, cards) to calibrate pixel-to-centimeter scaling, then estimate volume via geometric assumptions. Vinod et al. (CVPRW 2024) demonstrate that 3D food models scaled using physical reference objects significantly improve portion accuracy, and Ma et al. (ICPR 2024) show that monocular 3D point cloud reconstruction can approximate multi-view depth sensing. Shao et al. (ICME 2023) propose end-to-end voxel reconstruction from single RGB images, tested on Nutrition5k. However, all three systems rely on Western food datasets (SimpleFood45, MetaFood3D, Nutrition5k) and 3D food model libraries that do not exist for Indian cuisine.

**Data-driven approaches** treat portion estimation as a regression problem. The Nutrition5k dataset (Thames et al., 2021) — 5,006 Google cafeteria plates with RGB-D captures and per-ingredient weighed ground truth — enabled the first large-scale vision-to-nutrition regression baselines. Their key insight is that combining visual features with depth data yields practically useful calorie estimates. Our work adapts this insight to a smartphone-only context: we replace depth sensors with dish-specific geometric priors (height categories: flat, mounded, pooled, liquid) and density tables (INFOODS values), fusing them with a learned regression model to estimate portion grams from single images.

**Nutrition computation** from estimated portions requires reliable food composition data. The Indian Food Composition Tables (IFCT 2017; Longvah et al., 2017) provide analytically derived nutrient values for 528 raw foods across 151 components. Critically, IFCT values are for raw ingredients — converting to cooked values requires moisture correction. Chiplonkar and Agte (2007) validated this approach on 104 cooked Indian foods, demonstrating that macronutrient estimates (protein, fat, carbohydrates) are reliable within ±5% at the individual food level when raw composition table values are adjusted by the ratio of raw-to-cooked weight. We adopt their method as the foundation of our nutrition engine, extending it with canteen-sourced recipes and IFCT-backed ingredient lookup.

The Indian Nutrient Databank (INDB; Anuvaad Solutions) provides computed nutritional profiles for 1,014+ Indian recipes using IFCT 2017 as its foundation, serving as a cross-validation resource for our own computed values.

### 2.3 Multimodal LLMs for Dietary Assessment

The recent release of multimodal LLMs with vision capabilities — notably GPT-4V/GPT-4o (OpenAI, 2023–2024) and Gemini Pro/Flash (Google, 2024) — has introduced a new paradigm for food understanding. These models can identify food items from photographs with high precision (~90–93%) and provide natural-language nutritional assessments without domain-specific training.

However, emerging evaluations reveal fundamental limitations for quantitative nutrition estimation. Studies evaluating GPT-4V on weighed meal photographs (Ahn et al., 2024; various Nutrients/IEEE publications) report that while food identification is strong, **calorie estimation exhibits 20–35% mean absolute percentage error (MAPE)**, with systematic underestimation of medium-to-large portions (p < 0.001). Gemini-class models show similar performance characteristics, with median absolute errors around 50–60 kcal per dish and approximately 65% of predictions falling within 100 kcal of ground truth. Both models struggle most with hidden calorie-dense ingredients (cooking oils, butter, ghee) — a particularly acute problem for Indian cuisine, where dishes frequently contain substantial oil/ghee not visible in photographs.

Critically, no published study has benchmarked multimodal LLMs specifically on Indian food with weighed ground truth. Existing evaluations use Western meal photographs from national dietary surveys. Our work fills this gap with the **first systematic benchmark** of GPT-4o and Gemini on Indian food calorie estimation, using 100 weighed test images with IFCT-backed ground truth. We further introduce a **constrained refiner** experiment: comparing unconstrained LLM adjustments to user feedback ("this is a small portion") against our bounded adjustment system, which restricts LLM-generated corrections to a ±30% envelope anchored to our portion-aware estimates.

### 2.4 Our Contribution in Context

Our work is distinguished by three properties absent from prior literature:

1. **A portion-aware pipeline designed for Indian food**, combining dish-specific serving priors, geometric estimation, and learned regression — all grounded in IFCT 2017 nutrient values with Chiplonkar-validated moisture correction.
2. **The first benchmark of multimodal LLMs on Indian food calorie estimation**, using the same weighed test images, the same metrics, and a direct comparison to our pipeline.
3. **A released recipe table** documenting ~30 Indian dishes with sourced, confidence-tagged ingredient-level recipes and IFCT nutrient codes — a resource contribution following the precedent of Chiplonkar and Agte's published nutrient computations.

---

*This is a living document. Entries will be expanded as additional papers are reviewed during the project.*
