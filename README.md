# DGA Anomaly Detection

This project provides machine learning and NLP pipelines for detecting Domain Generation Algorithms (DGA) anomalies in DNS traffic. Malicious actors use DGAs to periodically generate rendezvous domain names, making botnets resilient to takedowns. This system categorizes domains as benign or malignant based on their structure.

## Overview

- **Modular Features:** Engineers token-based (ngram lengths) and raw byte-based features from domain strings.
- **Ensemble Model:** Uses a robust state-of-the-art `CatBoostClassifier` ensemble model.
- **Automated Pipeline:** Full end-to-end functionality (loading, processing, model training, evaluation) provided in standard scripts.

## The Best Model

The current best-performing model is `catboost.0.977.26_ensemble.model` (trained on 1000 iterations). 
It leverages two sets of engineered features:
1. **Ngram Lengths:** Tokenizer extracts up to 14 token lengths.
2. **Raw Bytes:** 26 features representing the exact ASCII bytes (padded or cropped symmetrically).

## Usage

You can launch the training and evaluation workflow by executing the main python script from the root directory:

```bash
python src/train.py
```

*Note: The original Jupyter notebook containing earlier research is accessible in `experiments/DGA_detection.ipynb`.*

## Documentation

For an in-depth explanation of the logic behind this project, please refer to the markdown files in the `docs/` folder:
- [Experiments](docs/experiments.md): Background context and evolution of the models.
- [Tools](docs/tools.md): The specific tech stack and libraries used.
- [Workflows](docs/workflows.md): The core architecture and execution logic.
- [Evaluations](docs/evaluations.md): Key metrics and rationale behind modeling strategies.
