import numpy as np
import os
from catboost import CatBoostClassifier

def ensemble_predict(prob1, prob2, weight1=0.5, weight2=0.5):
    """
    Ensemble predictions from two models based on their class probabilities.
    Weighted average of predicted probabilities.
    """
    return (np.array(prob1) * weight1 + np.array(prob2) * weight2)


def train_catboost(X_train, y_train, X_dev=None, y_dev=None, loss_function='MultiClass', **kwargs):
    """
    Train a CatBoost model.
    """
    model = CatBoostClassifier(loss_function=loss_function, **kwargs)
    eval_set = (X_dev, y_dev) if X_dev is not None and y_dev is not None else None
    
    model.fit(
        X_train, y_train, 
        eval_set=eval_set, 
        verbose=False,
        plot=False
    )
    return model


def save_model(model, out_file_path: str):
    """
    Save the model to the given path.
    """
    os.makedirs(os.path.dirname(out_file_path), exist_ok=True)
    model.save_model(out_file_path)
    print(f'Saved model to {out_file_path}')
