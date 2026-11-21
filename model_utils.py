"""
model_utils.py
---------------
Trains the model ONCE from the existing 14,000-row dataset (reusing the
existing 70/15/15 split already stored in ERG.xlsx), then saves:
  1. the trained model
  2. the EXACT list/order of one-hot-encoded feature columns used at training

This second artifact is critical and easy to get wrong: a new combination's
raw features must be one-hot encoded and then REINDEXED to match the
training column order exactly (filling any missing dummy column with 0),
otherwise the model will silently misinterpret the input.
"""
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
from catboost import CatBoostClassifier


def train_and_save(xlsx_path, model_out_path="trained_model.pkl"):
    features_df = pd.read_excel(xlsx_path, sheet_name="05_Combination_Features")
    labels_df = pd.read_excel(xlsx_path, sheet_name="06_Combined_Criticality_Labels")
    splits_df = pd.read_excel(xlsx_path, sheet_name="11_Model_TrainTest_Split")

    df = features_df.merge(labels_df, on="combination_id").merge(splits_df, on="combination_id")

    ID_COLS = ["combination_id"]
    TARGET_COL = "combined_criticality"
    SPLIT_COL = "split"

    bool_cols = df.select_dtypes(include="bool").columns.tolist()
    df[bool_cols] = df[bool_cols].astype(int)
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    cat_cols = [c for c in cat_cols if c not in ID_COLS + [TARGET_COL, SPLIT_COL]]

    df_enc = pd.get_dummies(df, columns=cat_cols, drop_first=False)
    feature_cols = [c for c in df_enc.columns if c not in ID_COLS + [TARGET_COL, SPLIT_COL]]

    train_df = df_enc[df_enc.split == "train"]
    test_df = df_enc[df_enc.split == "test"]

    le = LabelEncoder()
    y_train = le.fit_transform(train_df[TARGET_COL])
    y_test = le.transform(test_df[TARGET_COL])

    model = CatBoostClassifier(iterations=400, depth=6, learning_rate=0.08, random_state=42, verbose=False)
    model.fit(train_df[feature_cols], y_train)

    test_acc = model.score(test_df[feature_cols], y_test)
    print(f"[train_and_save] Test accuracy on held-out set: {test_acc:.4f}")

    bundle = {
        "model": model,
        "feature_cols": feature_cols,   # exact training column order -- required for correct inference
        "cat_cols": cat_cols,           # which raw columns were one-hot encoded
        "bool_cols": bool_cols,
        "label_encoder": le,
        "test_accuracy": test_acc,
    }
    joblib.dump(bundle, model_out_path)
    print(f"[train_and_save] Saved model bundle to {model_out_path}")
    return bundle


def load_model(model_path="trained_model.pkl"):
    """Load the trained model + schema WITHOUT retraining."""
    return joblib.load(model_path)


def prepare_inference_row(raw_features: dict, bundle: dict):
    """
    Takes a raw feature dict (from feature_extraction.compute_features) for
    ONE new combination, applies the SAME encoding used at training, and
    reindexes to the SAME column order/set -- filling any missing dummy
    column with 0. This is the step most implementations get wrong.
    """
    row_df = pd.DataFrame([raw_features])

    bool_cols_present = [c for c in bundle["bool_cols"] if c in row_df.columns]
    row_df[bool_cols_present] = row_df[bool_cols_present].astype(int)

    cat_cols_present = [c for c in bundle["cat_cols"] if c in row_df.columns]
    row_enc = pd.get_dummies(row_df, columns=cat_cols_present, drop_first=False)

    # CRITICAL STEP: align to the exact training columns, filling gaps with 0
    row_aligned = row_enc.reindex(columns=bundle["feature_cols"], fill_value=0)
    return row_aligned


if __name__ == "__main__":
    train_and_save("ERG.xlsx", "trained_model.pkl")
