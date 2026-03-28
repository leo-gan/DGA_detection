import pandas as pd
import numpy as np
import os
from sklearn.metrics import average_precision_score
from src.features import prepare_ensemble_features
from src.models import train_catboost, save_model
from src.evaluate import print_results

def cast_to_array(s):
    if isinstance(s, list):
        return np.array(s)
    if isinstance(s, np.ndarray):
        return s
    return np.array([int(el) for el in s[1:-1].split(", ")])

def main():
    # Hardcoded Configuration
    input_data = 'data/training_data/data.csv'
    ensemble_features_dir = 'data/training_data/ensemble_features'
    max_len = 26
    nrows = None
    
    # Load dataset and extract/prepare features
    print(f"Loading data from {input_data} (nrows={nrows})...")
    df = pd.read_csv(input_data, nrows=nrows)
    
    print("Preparing features...")
    df_res = prepare_ensemble_features(
        df, out_dir=ensemble_features_dir, max_len=max_len, nrows=nrows, save=False
    )
    
    # Cast strings to numpy arrays
    df_res['features'] = df_res['features'].apply(cast_to_array)
    
    # Check dataset size and split
    size = df_res.shape[0]
    train_size, dev_size, test_size = int(size * 0.8), int(size * 0.9), size
    print(f"train: {train_size:,}, dev: {dev_size - train_size:,}, test: {test_size - dev_size:,}")
    
    X_train = np.array(list(df_res.loc[0:train_size, 'features']))
    y_train = df_res.loc[0:train_size, 'y']
    
    X_dev = np.array(list(df_res.loc[train_size:dev_size, 'features']))
    y_dev = df_res.loc[train_size:dev_size, 'y']
    
    X_test = np.array(list(df_res.loc[dev_size:, 'features']))
    y_test = df_res.loc[dev_size:, 'y']

    # Train model
    print("Start training...")
    model = train_catboost(X_train, y_train, X_dev, y_dev, loss_function='MultiClass')
    
    # Evaluate
    print("Evaluating model...")
    y_pred_proba = model.predict_proba(X_test)
    y_scores = [p[1] for p in y_pred_proba]
    print_results(y_test, y_scores, y_pred=None)

    aps = average_precision_score(y_test, y_scores)
    out_file_name = f"models/catboost_ensemble_{aps:.3f}_{max_len}.model"
    
    # Save model
    save_model(model, out_file_name)


if __name__ == '__main__':
    main()
