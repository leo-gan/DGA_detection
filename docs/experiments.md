# DGA Detection Experiments

## Background and Motivation
Domain Generation Algorithms (DGA) are a technique used by various malware families to generate a large number of domain names. These serve as rendezvous points with Command and Control (C&C) servers. Because these algorithms create unpredictable and large quantities of domains, static blacklisting is ineffective. Machine learning models must be trained to recognize the "anomalous" patterns of generated domains versus benign human-readable domains.

## Evolution of Models

The experimental process focused on engineering lightweight and highly robust features from raw domain strings. The progression of experiments captures these main phases:

### Phase 1: Byte-based Features
Initially, we relied on character/byte-level features. 
- **Methodology**: Domain strings are padded to a max length or truncated (favoring the middle of the string, which typically contains the most entropy). Characters are then mapped to their ordinal byte values.
- **Model**: `catboost.0.964.26_bytes.model` (trained on 1400 iterations). 
- **Observations**: Byte models captured the unusual character distributions of DGA domains but required deep trees and many iterations.

### Phase 2: Token-based Features
To capture structural characteristics of words (e.g., readability, pronounceability), we explored NLP tokenizers.
- **Methodology**: Rather than passing raw tokens, we used `DistilBertTokenizer` to tokenize the string. We counted occurrences of token lengths (from length 1 up to 14). 
- **Theory**: DGA domains break into many small, unnatural tokens or single characters under BPE (Byte-Pair Encoding), whereas benign domains split into fewer, longer readable chunks.

### Phase 3: Ensemble Features (Current State of the Art)
We merged both bytes-based and token length-based representations.
- **Methodology**: Concatenating token length histograms with raw padded bytes. 
- **Model**: `catboost.0.977.26_ensemble.model`
- **Result**: The ensemble approach yielded a significantly higher score and allowed the model to converge well at fewer iterations (1000 iterations), resulting in improved performance and a smaller model size.

## Thoughts and Rationale

- **Why CatBoost?**: Gradient Boosting handles non-linear relationships well, particularly combining raw categorical-like ordinal numbers and BPE histogram bins.
- **Why reduce iterations?**: Smaller iteration counts resulted in smaller, faster-to-load models without sacrificing generalized performance, which is heavily desired in real-time DNS traffic scanning.
- **Why truncate from the middle?**: TLDs (like `.com`) and subdomains (like `www.`) are predictable. The entropy of a DGA domain is typically focused in the middle of long strings.
