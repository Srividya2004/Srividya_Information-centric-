"""
explain.py
----------
SHAP and LIME on a SINGLE new inference row -- exactly the same explainers
used in the research notebook, just wrapped to run once per query instead
of once per batch of 200 sampled test rows.
"""
import numpy as np
import shap


def shap_explain(row_aligned, bundle, top_n=6):
    model = bundle["model"]
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(row_aligned)

    predicted_class_idx = model.predict(row_aligned)[0]
    if hasattr(predicted_class_idx, "__len__"):
        predicted_class_idx = predicted_class_idx[0]
    predicted_class_idx = int(predicted_class_idx)

    if np.array(shap_values).ndim == 3:
        vals_for_class = shap_values[0, :, predicted_class_idx]
    else:
        vals_for_class = shap_values[0]

    contrib = sorted(zip(row_aligned.columns, vals_for_class), key=lambda x: abs(x[1]), reverse=True)[:top_n]
    return [{"feature": f, "shap_value": round(float(v), 4), "raw_value": row_aligned.iloc[0][f]} for f, v in contrib]


def lime_explain(row_aligned, bundle, background_df, top_n=6):
    import lime.lime_tabular
    model = bundle["model"]
    le = bundle["label_encoder"]

    lime_explainer = lime.lime_tabular.LimeTabularExplainer(
        background_df.values, feature_names=background_df.columns.tolist(),
        class_names=le.classes_, mode="classification"
    )
    exp = lime_explainer.explain_instance(row_aligned.iloc[0].values, model.predict_proba, num_features=top_n)
    return [{"rule": rule, "weight": round(weight, 4)} for rule, weight in exp.as_list()]
