# Nutri.In — Portion-Aware Indian Food Nutrition Estimator

> *"How Wrong Are Multimodal LLMs on Indian Food? A Portion-Aware Pipeline and First Benchmark"*

## Overview

A portion-aware pipeline (recognition → portion estimation → IFCT-recipe engine) for Indian food calorie/macro estimation, with the **first benchmark** of GPT-4V-class and Gemini-class models on Indian food calorie estimation using a publicly documented weighed test set.

## Core Claims

1. A portion-aware pipeline for Indian food calorie/macro estimation
2. First benchmark of multimodal LLMs on Indian food calorie estimation
3. Evidence that portion-aware estimation beats unconstrained LLM guessing
4. A documented recipe table + nutrition lookup for ~30 Indian dishes as a released resource

## Repository Structure

```
Nutri.In/
├── data/
│   ├── raw/                  # Raw datasets (DVC-tracked)
│   │   ├── khana/            # Khana dataset images
│   │   ├── ifct/             # IFCT 2017 nutrient tables
│   │   └── weighed_photos/   # Our weighed photo dataset
│   ├── processed/            # Cleaned & transformed data
│   └── splits/               # Train/val/test split manifests
├── src/
│   ├── nutrition/            # Nutrition engine (IFCT + recipes)
│   ├── models/               # Dish recognition models
│   ├── segmentation/         # Food/plate segmentation
│   ├── benchmark/            # LLM benchmark scripts
│   ├── app/                  # Web application
│   │   ├── backend/          # FastAPI backend
│   │   └── frontend/         # React frontend
│   └── utils/                # Shared utilities
├── recipes/                  # Recipe data (recipes.json, ifct_lookup.csv)
├── configs/                  # Training & experiment configs
├── notebooks/                # Exploration & analysis notebooks
├── benchmark/                # LLM prompts & benchmark config
├── weights/                  # Trained model checkpoints
├── tests/                    # Unit & integration tests
└── docs/
    ├── papers/               # Reference papers
    ├── meeting-notes/        # Guide meeting notes
    ├── dataset-docs/         # Dataset documentation
    └── figures/              # Paper figures
```

## Setup

```bash
# Clone the repo
git clone <repo-url>
cd Nutri.In

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize DVC (already done)
# dvc init
```

## Tech Stack

- **Classification:** ConvNeXt-Small, MobileNetV3 (PyTorch)
- **Segmentation:** U-Net / DeepLabV3
- **Nutrition Engine:** IFCT 2017 + custom recipe table
- **Benchmark:** GPT-4o, Gemini (via API)
- **Backend:** FastAPI
- **Frontend:** React
- **Experiment Tracking:** Weights & Biases
- **Data Versioning:** DVC

## Team

| Role | Responsibility |
|------|---------------|
| **Member A — Data Lead** | Datasets, recipes, weighed photos, annotations |
| **Member B — Models Lead** | Classifier, segmentation, regression, training runs |
| **Member C — Systems Lead** | Nutrition engine, LLM benchmark, app, metrics |

## License

TBD
