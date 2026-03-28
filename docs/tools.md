# Tools

The DGA anomaly detection project utilizes a distinct set of tools across its data processing, feature extraction, modeling, and evaluation layers.

## Data Processing and Management
- **Pandas / NumPy**: Core libraries for vector manipulations, DataFrame aggregations, and data formatting.
- **tldextract**: Used during dataset preparation to reliably separate the structural parts of URLs (e.g., separating the TLD from the root domain).

## Feature Engineering (NLP)
- **transformers (`DistilBertTokenizer`)**: Instead of relying heavily on explicit language models, we exploit the tokenizer's sub-word algorithm. By looking at how domains break down functionally, we extract token size histograms as a proxy for morphological "naturalness."

## Modeling and Scoring
- **CatBoost (`CatBoostClassifier`)**: Serving as the primary algorithm. It natively handles various feature interactions robustly, requires minimal hyperparameter tuning to get strong baselines, and produces fast inference artifacts.
- **scikit-learn (`sklearn.metrics`)**: Used strictly for model scoring (Average Precision, ROC-AUC, and generating classification reports).

## Environment and Dependency Management
- **Poetry**: Used to strictly manage dependencies (`pyproject.toml` and `poetry.lock`), ensuring reproducible builds across development, testing, and production environments. Overrides and direct configurations (like black and isort configs) are embedded inside `pyproject.toml`.
