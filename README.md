This project train models for the DGA anomaly detection.


# The best models
## Update: 2022-09-26
It is the `catboost.0.977.26_ensemble.model`. It is trained on 1000 iterations, 
so it is smaller than the previous best.

See the DGA_detection.ipynb : "Ensemble: token-based and bytes-based" section.

The model features: 
- ngram length numbers, extracted by a tokenizer: 14 lengths
- bytes as features: 26 bytes. Note: for the long domains it takes bytes from
  the middle of the string.

## 2022-09-23
So far, it is `catboost.0.964.26_bytes.model` it trained on 1400 iterations.
The `catboost.0.962.32_bytes.model` is nearby. It trained on 1000 iterations.
The reason we use the first one, is it smaller.
