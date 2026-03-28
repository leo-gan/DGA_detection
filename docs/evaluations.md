# Evaluations

Model evaluation is tightly integrated into the final stage of `src/train.py` and relies entirely on isolated test data (a 10% holdout split) that the model has neither trained on nor been evaluated against for validation checkpoints. The project strictly controls these splits to guarantee high generalization confidence against zero-day DGA behaviors.

## Core Evaluation Metrics

The fundamental metrics calculated in `src/evaluate.py` are aimed at providing deep visibility over class imbalance effects (e.g., having many more benign domains in real DNS traffic than malicious DGA domains).

1. **Average Precision Score (APS) / PR-AUC**
   - Because of class imbalance, standard accuracy is misleading. 
   - APS summarizes the Precision-Recall curve as a single score, effectively measuring the weighted mean of precisions achieved at each threshold.
   - This score directly dictates model file naming (`catboost_ensemble_{aps}_{max_len}.model`), acting as the principal target to maximize.

2. **ROC AUC Score**
   - Area Under the Receiver Operating Characteristic Curve. 
   - A score closer to 1.0 dictates that the model handles separating the distributions of positive (DGA) and negative (Benign) classes efficiently.

3. **Classification Report**
   - We utilize `sklearn`'s comprehensive report to monitor precision, recall, and f1-score per individual class. 
   - Precision for class 1 (DGA) dictates real-world false-positive rates (how many clean sites are blocked).
   - Recall for class 1 dictates false-negative rates (how much malware bypasses detection).

## Experimental Observations on Performance

- The older `bytes-only` CatBoost model maxed out near ~0.964 APS.
- Increasing interactions natively improved structural pattern recognition, allowing the `ensemble` CatBoost model to clear ~0.977 APS.
- Adding the token-length distributions severely drops the required iteration count. This tells us the model was primarily spending trees trying to 're-invent' sub-word analysis on byte level data. Giving it the tokenizer explicitly lifted that burden.

## Continuous Evaluation Strategy

1. For new feature experiments, ensure you evaluate on the existing test partitions.
2. If changing the underlying tokenizer or `max_len`, re-evaluate the baseline byte-based model to ensure the control remains scientifically sound.
3. Track and commit the test-set metrics to repository artifacts directly in the script (`train.py`), logging the final string alongside the saved `.model` representation.
