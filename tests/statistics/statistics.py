import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix, roc_auc_score, roc_curve

def prepare_validation_labels(df, truth_col='Curator Validation', pred_col='Agent Validation'):
    # Fill missing ground truth with "TRUE"
    df = df.copy()
    df[truth_col] = df[truth_col].fillna('TRUE').astype(str).str.upper()
    # case-insensitive comparison
    df[pred_col] = df[pred_col].astype(str).str.strip().str.upper()
    df[truth_col] = df[truth_col].astype(str).str.strip().str.upper()

    # Only consider rows where agent made a prediction (not empty)
    mask = df[pred_col].isin(['TRUE', 'FALSE'])
    y_true = df.loc[mask, truth_col].map({'TRUE': 1, 'FALSE': 0})
    y_pred = df.loc[mask, pred_col].map({'TRUE': 1, 'FALSE': 0})
    return mask, y_true, y_pred

def compute_validation_stats(df, truth_col='Curator Validation', pred_col='Agent Validation'):
    mask, y_true, y_pred = prepare_validation_labels(df, truth_col, pred_col)

    precision, recall, f1, mask = precision_recall_fscore_support(
        y_true, y_pred, pos_label=1, average='binary', zero_division=0
    )

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    print(f"tn={tn}, fp={fp}, fn={fn}, tp={tp}")
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0
    accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0.0

    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'accuracy': float(accuracy),
        'fnr': float(fnr)
    }

def plot_auc(df, truth_col='Curator Validation', pred_col='Agent Validation'):
    mask, y_true, y_pred = prepare_validation_labels(df, truth_col, pred_col)
    # y_pred must be probabilities for ROC; here, use binary predictions as scores
    auc = roc_auc_score(y_true, y_pred)
    fpr, tpr, mask = roc_curve(y_true, y_pred)
    plt.figure()
    plt.plot(fpr, tpr, label=f'ROC curve (AUC = {auc:.2f})')
    plt.plot([0, 1], [0, 1], 'k--', label='Random')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc='lower right')
    plt.show()
    print(f"AUC: {auc:.4f}")
    return auc

if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.join(current_folder, '../test_data/cell_type_validation_report_test.tsv')
    test_df = pd.read_csv(test_file, sep='\t', dtype=str)
    stats = compute_validation_stats(test_df)
    print(stats)
    plot_auc(test_df)