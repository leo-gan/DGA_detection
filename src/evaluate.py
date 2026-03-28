from sklearn.metrics import average_precision_score, classification_report, roc_auc_score

def print_results(y_true, y_scores, y_pred=None):
    if not y_pred:
        y_pred = [1 if sc > 0.5 else 0 for sc in y_scores]
        
    support = len(y_true)
    print(f"support: {support:}")
    print(f"average_precision_score: {average_precision_score(y_true, y_scores):.3}")
    
    roc_auc_score_val = roc_auc_score(y_true, y_scores)
    print(f"roc_auc_score: {roc_auc_score_val:.3}")
    
    print(f"classification_report: \n{classification_report(y_true, y_pred)}")
