# DGA Detection Workflows

The workflow inside this project handles the entire pipeline—from raw data amalgamation to feature caching, model training, and exporting. The codebase has recently been refactored from a standalone Jupyter notebook (`DGA_detection.ipynb`) into a modular Python scaffolding (`src/`) to support automated CI/CD and large horizontal scaling.

## Pipeline Architecture

The execution pipeline involves the following core modules:

1. **`src/data.py`**
   - **Ingestion**: Raw DNS records and generated domain names are read from source files via wildcard matches (e.g., globbing `example_domains.txt`).
   - **Deduplication**: Domain overlaps (particularly in benign versus malicious datasets) are resolved securely by dropping duplicates to prevent data leakage and label poisoning.
   - **Standardization**: Use `tldextract` to strip generic TLDs (`.com`, `.net`), isolating the actual domain root which houses the intrinsic character entropy.

2. **`src/features.py`**
   - **Byte Features**: Pads strings shorter than `max_len`, but trims longer strings systematically by taking bytes from the middle (which represent the pure domain entropy). Converts characters to standard binary representations (ordinals).
   - **Token Features**: Triggers the `DistilBertTokenizer`, turning strings into sub-word arrays, ignoring explicit vocab mapping, and mapping counts of *token lengths*.
   - **Ensemble Combination**: Provides a wrapper (`prepare_ensemble_features`) that performs row-wise map/apply on the pandas Dataframe passing domains through both byte and token pathways before concatenating the output vectors.

3. **`src/models.py`**
   - Standardizes the declaration, parameterization, and initialization of `CatBoostClassifier`.
   - Offers simple helper methods combining arrays (e.g., `.predict_proba`), returning binary decisions, and natively serializing the binary file via `.save_model`.

4. **`src/train.py`**
   - The primary orchestrator.
   - It manages configuration parameters (max string length, file paths).
   - Enforces an `80/10/10` (train/dev/test) split over the prepared dataset.
   - Passes the `dev` set to CatBoost during training for evaluation tracking and early stopping.
   - Saves final model representations to the `models/` directory, uniquely tagged with `aps` (Average Precision Score) and `max_len`.

## Workflow Guidelines

- **Caching**: The feature preparation step (`prepare_ensemble_features`) supports saving intermediate artifacts to CSV (if `save=True`). This avoids redundant BPE tokenization, saving hours during iterative machine learning architecture adjustments.
- **Reproducibility**: All randomization (like the `shuffle` call inside data prep) requires explicit seed propagation to guarantee identical results during local versus cloud training.
- **Modularity**: By sequestering data extraction from model fitting, experimental loops can evaluate completely disparate architectures without altering the upstream logic.
