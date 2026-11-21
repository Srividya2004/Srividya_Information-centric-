"""
report.py
---------
Assembles the final structured output shown to an analyst, combining:
- the raw asset identities (from EnterpriseInventory)
- the predicted class + probabilities
- SHAP/LIME top contributing factors
- a pathway-style emerging-risk / business-consequence tag, derived from
  which raw signals were strong for THIS combination (mirrors the logic
  already used to build 07_Emerging_Risks / 08_Business_Consequences,
  applied live instead of at batch-generation time)
"""

EMERGING_RISK_BY_DOMINANT_FEATURE = {
    "information_complementarity_score": "Data Breach via Information Complementarity",
    "information_reconstruction_potential": "Data Breach via Information Reconstruction",
    "privilege_escalation_potential": "Privilege Escalation via Shared Access Path",
    "vulnerability_interaction_score": "Data Exfiltration via Vulnerability Interaction",
    "exploit_chain_potential": "Data Exfiltration via Exploit Chain",
    "emergent_capability_score": "Emergent Attack Capability Not Present in Any Single Asset",
    "relationship_strength": "Unauthorized Access via Dependency Chain",
    "control_gap_count": "Exploitation Enabled by Control Gaps",
}
CONSEQUENCE_BY_RISK = {
    "Data Breach via Information Complementarity": ["Data Exposure", "Regulatory Penalty"],
    "Data Breach via Information Reconstruction": ["Data Exposure", "Regulatory Penalty"],
    "Privilege Escalation via Shared Access Path": ["Operational Disruption", "Data Exposure"],
    "Data Exfiltration via Vulnerability Interaction": ["Data Exposure", "Financial Loss"],
    "Data Exfiltration via Exploit Chain": ["Data Exposure", "Financial Loss", "IP Loss"],
    "Emergent Attack Capability Not Present in Any Single Asset": ["Data Exposure", "Reputational Damage"],
    "Unauthorized Access via Dependency Chain": ["Operational Disruption", "Data Exposure"],
    "Exploitation Enabled by Control Gaps": ["Financial Loss", "Reputational Damage"],
}


def build_report(asset_ids, inv, predicted_label, probabilities, raw_features, shap_result, lime_result, is_new_combo):
    asset_details = [inv.asset_summary(a) for a in asset_ids]

    report = {
        "combination": " + ".join(asset_ids),
        "is_new_combination_not_in_training_set": is_new_combo,
        "assets": asset_details,
        "predicted_combined_criticality": predicted_label,
        "confidence": {cls: round(float(p), 3) for cls, p in probabilities.items()},
        "key_features": {k: raw_features[k] for k in
                          ["information_complementarity_score", "relationship_strength", "shared_user_count",
                           "privileged_access_present", "privilege_escalation_potential",
                           "vulnerability_interaction_score", "known_exploited_present",
                           "control_gap_count", "emergent_capability_score"]},
        "shap_top_factors": shap_result,
        "lime_explanation": lime_result,
    }

    if predicted_label != "Low":
        top_feature = shap_result[0]["feature"] if shap_result else None
        emerging_risk = EMERGING_RISK_BY_DOMINANT_FEATURE.get(top_feature, "Compound Contextual Risk")
        report["emerging_risk"] = emerging_risk
        report["business_consequence"] = "; ".join(CONSEQUENCE_BY_RISK.get(emerging_risk, ["Data Exposure"]))
    else:
        report["emerging_risk"] = "None -- manageable combination"
        report["business_consequence"] = "None"

    return report


def print_report(report):
    print("=" * 70)
    print(f"COMBINATION: {report['combination']}")
    print(f"New combination (not in 14,000 training set): {report['is_new_combination_not_in_training_set']}")
    print("-" * 70)
    for a in report["assets"]:
        print(f"  {a['asset_id']}: {a['asset_subtype']} ({a['department']}) "
              f"| existing_criticality={a['existing_criticality']}")
    print("-" * 70)
    print(f"PREDICTED COMBINED CRITICALITY: {report['predicted_combined_criticality']}")
    print(f"CONFIDENCE: {report['confidence']}")
    print("-" * 70)
    print("KEY FEATURE VALUES:")
    for k, v in report["key_features"].items():
        print(f"  {k}: {v}")
    print("-" * 70)
    print("SHAP TOP CONTRIBUTING FACTORS:")
    for f in report["shap_top_factors"]:
        print(f"  {f['feature']} = {f['raw_value']}  (SHAP contribution: {f['shap_value']:+.4f})")
    print("-" * 70)
    print("LIME LOCAL EXPLANATION:")
    for r in report["lime_explanation"]:
        print(f"  {r['rule']}  (weight: {r['weight']:+.4f})")
    print("-" * 70)
    print(f"EMERGING RISK: {report['emerging_risk']}")
    print(f"BUSINESS CONSEQUENCE: {report['business_consequence']}")
    print("=" * 70)
