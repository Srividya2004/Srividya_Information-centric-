"""
compliance_mapper.py
Candidate ISO/IEC 27001:2022 Annex A mapping for the GRC Pro project.

IMPORTANT: every mapping in this file is a CANDIDATE. A human reviewer must
confirm it. A High prediction does not prove ISO non-compliance.
"""
import pandas as pd

TITLE_NOTE = "Checked against a secondary source; confirm against the ISO text"

# ---------------------------------------------------------------- Part 1
_ISO_ROWS = [
    ("A.5.9",  "Inventory of information and other associated assets", "Organizational", "Asset inventory"),
    ("A.5.12", "Classification of information",   "Organizational", "Information classification and protection"),
    ("A.5.13", "Labelling of information",        "Organizational", "Information classification and protection"),
    ("A.5.14", "Information transfer",            "Organizational", "Information classification and protection"),
    ("A.5.15", "Access control",                  "Organizational", "Access and identity"),
    ("A.5.16", "Identity management",             "Organizational", "Access and identity"),
    ("A.5.17", "Authentication information",      "Organizational", "Access and identity"),
    ("A.5.18", "Access rights",                   "Organizational", "Access and identity"),
    ("A.8.2",  "Privileged access rights",        "Technological",  "Access and identity"),
    ("A.8.3",  "Information access restriction",  "Technological",  "Access and identity"),
    ("A.8.5",  "Secure authentication",           "Technological",  "Access and identity"),
    ("A.8.8",  "Management of technical vulnerabilities", "Technological", "Vulnerability management"),
    ("A.8.9",  "Configuration management",        "Technological",  "Vulnerability management"),
    ("A.8.12", "Data leakage prevention",         "Technological",  "Information classification and protection"),
    ("A.8.15", "Logging",                         "Technological",  "Logging and monitoring"),
    ("A.8.16", "Monitoring activities",           "Technological",  "Logging and monitoring"),
    ("A.8.24", "Use of cryptography",             "Technological",  "Cryptography"),
]


def get_iso_reference():
    """Return the ISO reference as a fresh DataFrame (Table 1)."""
    df = pd.DataFrame(_ISO_ROWS, columns=["iso_control_id", "iso_control_title",
                                          "iso_theme", "topic_group"])
    df["title_verified"] = TITLE_NOTE
    return df


# ---------------------------------------------------------------- Part 2
# name -> (candidate ISO ids separated by "; ", fit, plain-language rationale)
ERG_CONTROL_TO_ISO = {
    "Patch Management": ("A.8.8", "Direct",
        "Applying patches fixes known technical vulnerabilities, which is vulnerability management."),
    "EDR (Endpoint Detection & Response)": ("A.8.16", "Partial",
        "EDR watches endpoints for suspicious behaviour, which relates to monitoring. It also does more than monitoring, so the match is partial."),
    "MFA": ("A.8.5", "Direct",
        "Multi-factor authentication strengthens sign-in, which is secure authentication."),
    "Mobile Device Management (MDM)": ("", "None",
        "Managing mobile devices is not covered by any control in the shortlist."),
    "Endpoint Firewall": ("", "None",
        "Network filtering on a device is not covered by any control in the shortlist."),
    "Access Control": ("A.5.15; A.8.3", "Direct",
        "It limits who can use resources and information, matching access control and information access restriction."),
    "Full Disk Encryption": ("A.8.24", "Direct",
        "Encrypting the disk is a use of cryptography."),
    "Network Segmentation": ("", "None",
        "Network separation is not covered by any control in the shortlist."),
    "Automated Backup": ("", "None",
        "Backup is not covered by any control in the shortlist."),
    "Firmware Patch Management": ("A.8.8", "Direct",
        "Firmware patches fix known technical vulnerabilities."),
    "Encryption at Rest": ("A.8.24", "Direct",
        "Encrypting stored data is a use of cryptography."),
    "Administrative MFA": ("A.8.5; A.8.2", "Direct",
        "MFA on administrator accounts secures sign-in and protects privileged access rights."),
    "Configuration Backup": ("A.8.9", "Partial",
        "Saving configurations supports configuration management, but backup itself is not in the shortlist."),
    "Logging": ("A.8.15", "Direct",
        "Recording events is what the logging control covers."),
    "Configuration Hardening": ("A.8.9", "Direct",
        "Hardening sets secure configurations on systems, which is what configuration management covers."),
    "Change Management": ("", "None",
        "Change management controls how changes are approved and made. A change-management control is not in the shortlist."),
    "Database Activity Logging": ("A.8.15", "Direct",
        "It records activity on databases, which is what the logging control covers."),
    "Access Control List": ("A.5.15; A.8.3", "Direct",
        "An access control list states who may use a resource, applying access rules and restricting access to information."),
    "File Access Logging": ("A.8.15", "Direct",
        "It records who accessed files, which is a form of logging."),
    "Database Access Control": ("A.5.15; A.8.3", "Direct",
        "It limits who can reach database information, matching access control and information access restriction."),
    "Secrets Management": ("A.5.17; A.8.24", "Direct",
        "Secrets such as passwords and keys are authentication information (A.5.17). Where the secrets are cryptographic keys, A.8.24 also relates."),
    "Bucket/Access Policy Enforcement": ("A.5.15; A.8.3", "Direct",
        "Storage access policies decide who can read the stored data."),
    "Access Logging": ("A.8.15", "Direct",
        "It records access events, which is a form of logging."),
    "MFA for Administrative Access": ("A.8.5; A.8.2", "Direct",
        "MFA on administrator access secures sign-in and protects privileged access rights."),
    "Offsite/Immutable Replication": ("", "None",
        "It keeps protected copies of data away from the main site. Backup and redundancy are not in the shortlist."),
    "Retention Policy Enforcement": ("", "None",
        "It keeps or deletes information after a set period. A retention or deletion control is not in the shortlist."),
    "MFA / SSO": ("A.8.5; A.5.16", "Direct",
        "MFA secures sign-in (A.8.5). Single sign-on relies on one managed identity per user (A.5.16)."),
    "Application Logging": ("A.8.15", "Direct",
        "It records events inside applications, which is a form of logging."),
    "Backup Integrity Verification": ("", "None",
        "It checks that backups can be restored. Backup is not in the shortlist."),
    "Role-Based Access Control": ("A.5.15; A.5.18", "Direct",
        "Roles decide who gets which access, matching access control and access rights."),
    "Third-Party Vendor Risk Review": ("", "None",
        "It reviews the risk of suppliers. Supplier relationships are not in the shortlist."),
    "Data Loss Prevention (DLP)": ("A.8.12", "Direct",
        "DLP stops sensitive data from leaving the organization, which is data leakage prevention."),
    "Activity Logging": ("A.8.15", "Direct",
        "It records user and system activity, which is a form of logging."),
    "Conditional Access Policies": ("A.5.15; A.8.5", "Partial",
        "These policies set conditions for sign-in, which relates to access control and secure authentication. Partial because the conditions vary by product."),
    "Logging and Monitoring": ("A.8.15; A.8.16", "Direct",
        "It covers both recording events and watching them for unusual behaviour."),
    "Log Integrity Protection": ("A.8.15", "Partial",
        "It protects logs from tampering. Logging is the nearest topic in the shortlist."),
    "Retention Policy": ("", "None",
        "It sets how long information is kept. A retention or deletion control is not in the shortlist."),
    "Rate Limiting": ("", "None",
        "It limits how many requests a user or system can make. No defensible match in the shortlist."),
    "Web Application Firewall (WAF)": ("", "None",
        "It filters web traffic to an application. Network and web security are not in the shortlist."),
    "Privileged Access Management (PAM)": ("A.8.2", "Direct",
        "PAM manages and controls administrator-level accounts, which is privileged access rights."),
    "TLS/Encryption in Transit": ("A.8.24; A.5.14", "Direct",
        "Encrypting data in transit is use of cryptography and protects information while it is transferred."),
    "Periodic Access Review": ("A.5.18", "Direct",
        "Reviewing who has access and removing what is no longer needed is the management of access rights."),
}


def get_erg_control_to_iso():
    """Return Table 2 as a DataFrame (one row per ERG control name)."""
    valid = set(get_iso_reference()["iso_control_id"])
    rows = []
    for name, (ids, fit, why) in ERG_CONTROL_TO_ISO.items():
        for one_id in [i for i in ids.split("; ") if i]:
            assert one_id in valid, name + ": " + one_id + " is not in the ISO reference"
        rows.append((name, ids, fit, why, "No"))
    return pd.DataFrame(rows, columns=["erg_control_name", "candidate_iso_ids", "fit",
                                       "mapping_rationale", "reviewed_by_human"])


# ---------------------------------------------------------------- Part 3
# Risk factor -> candidate ISO control. Feature names are the real columns
# of the model. A factor is ACTIONABLE only when someone could change it by
# acting on a control. Everything else is DESCRIPTIVE: it describes the
# combination, and we return "no mapping" for it.
MAPPING_STATUS = "Candidate - needs human review"

# feature -> (how the feature is computed, proposed action, evidence required)
_FACTOR_INFO = {
    "mfa_coverage": (
        "Share of selected assets that have an MFA-type control (MFA, MFA / SSO, Administrative MFA, MFA for Administrative Access) recorded as Implemented or Partially Implemented in 02e_Controls. Partially Implemented counts as present.",
        "Review whether sign-in to the selected assets without MFA can be strengthened with multi-factor authentication.",
        "MFA configuration or enforcement report for each selected asset; the implementation status recorded in 02e_Controls."),
    "encryption_coverage": (
        "Share of selected assets with Encryption at Rest or Full Disk Encryption recorded as Implemented or Partially Implemented. Limitation: data_loader.py also lists 'Encryption in Transit', which is not a control name in the data, so TLS/Encryption in Transit is not counted.",
        "Review whether stored data on the selected assets without encryption should be encrypted.",
        "Encryption settings for each selected asset; key management records; the implementation status in 02e_Controls."),
    "monitoring_coverage": (
        "Share of selected assets with a logging or monitoring control (Logging, Logging and Monitoring, Activity Logging, Access Logging, Application Logging, File Access Logging, Database Activity Logging, Log Integrity Protection) recorded as Implemented or Partially Implemented.",
        "Review whether activity on the selected assets without logging is recorded and whether anyone watches the logs.",
        "Log configuration and sample log records for each selected asset; evidence that logs are reviewed or alerted on."),
    "monitoring_gap_score": (
        "Equals 1 minus monitoring_coverage, so it carries the same information as monitoring_coverage.",
        "Review whether activity on the selected assets without logging is recorded and whether anyone watches the logs.",
        "Log configuration and sample log records for each selected asset; evidence that logs are reviewed or alerted on."),
    "known_exploited_present": (
        "True when at least one selected asset has a vulnerability marked as known exploited in the vulnerability data.",
        "Review the known-exploited vulnerabilities on the selected assets and check whether patches or other fixes are in place.",
        "Vulnerability scan results; patch records; the date each fix was applied."),
    "vulnerability_severity": (
        "Highest CVSS score among the vulnerabilities of the selected assets.",
        "Review the most severe vulnerabilities on the selected assets and check their remediation status.",
        "Vulnerability scan results; patch or remediation records."),
    "common_vulnerability_count": (
        "Number of vulnerability categories that appear on more than one selected asset.",
        "Review the vulnerability categories shared by the selected assets and check whether they are patched.",
        "Vulnerability scan results for each selected asset; patch records."),
    "vulnerability_interaction_score": (
        "Combines common_vulnerability_count with a bonus when a known-exploited vulnerability is present.",
        "Review shared and known-exploited vulnerabilities on the selected assets.",
        "Vulnerability scan results; patch records."),
    "common_weakness_score": (
        "Derived from common_vulnerability_count (count divided by 3, capped at 1).",
        "Review the vulnerability categories shared by the selected assets.",
        "Vulnerability scan results; patch records."),
    "privileged_access_present": (
        "True when at least one user has privileged access to two or more of the selected assets.",
        "Review who holds privileged access across the selected assets and whether each person needs it.",
        "List of privileged accounts per asset; approval records for each privileged right."),
    "privilege_escalation_potential": (
        "Built from two facts: shared privileged access (2 points) and an authenticates_to relationship between the assets (1 point). Only the first fact can be acted on directly.",
        "Review shared privileged access between the selected assets.",
        "List of privileged accounts per asset; approval records."),
    "shared_user_count": (
        "Number of users who have access to two or more of the selected assets.",
        "Review the users who can reach more than one selected asset and remove access that is no longer needed.",
        "Access lists per asset; the latest access review record."),
    "shared_user_strength": (
        "Derived from shared_user_count (count divided by 3, capped at 1).",
        "Review the users who can reach more than one selected asset.",
        "Access lists per asset; the latest access review record."),
    "access_overlap_score": (
        "Built from shared_user_count and the number of shared privileged users.",
        "Review the users who can reach more than one selected asset, including privileged users.",
        "Access lists per asset; the latest access review record."),
    "shared_identity_score": (
        "Derived from the number of users shared across the selected assets.",
        "Review whether the same identities are used across several selected assets and whether that is intended.",
        "Account lists per asset; identity management records."),
    "data_flow_present": (
        "True when at least one relationship between the selected assets records a data flow.",
        "Check how information moves between the selected assets and whether the transfer is controlled.",
        "Data flow documentation; transfer rules or agreements between the systems."),
}

# (feature, iso id, fit, why this ISO control relates to the feature)
_FACTOR_LINKS = [
    ("mfa_coverage", "A.8.5", "Direct", "MFA is a way of securing sign-in, which is secure authentication."),
    ("encryption_coverage", "A.8.24", "Direct", "Encryption is a use of cryptography."),
    ("monitoring_coverage", "A.8.15", "Direct", "Logging records the activity that monitoring depends on."),
    ("monitoring_coverage", "A.8.16", "Partial", "Monitoring means watching activity for unusual behaviour; the data only shows whether a logging-type control exists."),
    ("monitoring_gap_score", "A.8.15", "Direct", "It is the opposite of monitoring_coverage, which depends on logging controls."),
    ("monitoring_gap_score", "A.8.16", "Partial", "It is the opposite of monitoring_coverage; the data does not show whether logs are watched."),
    ("known_exploited_present", "A.8.8", "Direct", "Known-exploited vulnerabilities are technical vulnerabilities to be managed."),
    ("vulnerability_severity", "A.8.8", "Direct", "Severity of technical vulnerabilities is part of managing them."),
    ("common_vulnerability_count", "A.8.8", "Direct", "Shared vulnerability categories are technical vulnerabilities to be managed."),
    ("vulnerability_interaction_score", "A.8.8", "Direct", "It is built from technical vulnerabilities."),
    ("common_weakness_score", "A.8.8", "Direct", "It is built from shared technical vulnerabilities."),
    ("privileged_access_present", "A.8.2", "Direct", "Shared privileged access is a question of privileged access rights."),
    ("privileged_access_present", "A.5.18", "Partial", "Reviewing who holds privileged access is part of managing access rights."),
    ("privilege_escalation_potential", "A.8.2", "Partial", "Part of the score comes from shared privileged access."),
    ("shared_user_count", "A.5.18", "Direct", "Users with access to several assets are a question of access rights."),
    ("shared_user_strength", "A.5.18", "Direct", "It is derived from shared_user_count."),
    ("access_overlap_score", "A.5.18", "Direct", "It is built from users with access to several assets."),
    ("shared_identity_score", "A.5.18", "Partial", "It is derived from shared users; identity management (A.5.16) may also apply."),
    ("data_flow_present", "A.5.14", "Partial", "A recorded data flow raises the question of how the transfer is controlled."),
]


# Factors that are actionable only through the actual control records of the
# selected assets. The ISO control then comes from Table 2 (part 2), not from
# a fixed link here.
ACTIONABLE_VIA_CONTROL_RECORDS = {
    "control_gap_count": "Number of control records on the selected assets with control_gap = True, which in this dataset means Low control effectiveness (it includes Not Implemented and Planned). It is a dataset convention, not an ISO finding.",
    "control_gap_interaction": "Derived from control_gap_count and the number of selected assets.",
    "control_effectiveness": "Average control effectiveness score of the selected assets.",
    "combined_control_effectiveness": "Average control effectiveness score of the selected assets.",
}

# Factors that describe the combination. They are not mapped.
DESCRIPTIVE_FACTORS = {
    "emergent_capability_score": "A researcher-defined composite of other features. It describes the combination and is not something a control can change directly.",
    "risk_amplification_score": "A composite score. It describes the combination.",
    "contextual_information_gain": "Describes how much more sensitive the combined data is than each asset alone.",
    "combined_information_sensitivity": "Describes how sensitive the data is. Sensitivity is a property of the data, not a control state.",
    "combined_asset_value": "Describes asset value. It is not a control state.",
    "combined_exposure_score": "Describes exposure. It is not a control state.",
    "information_overlap_score": "Describes which data categories the assets share.",
    "information_complementarity_score": "Describes how the assets' data types combine.",
    "information_reconstruction_potential": "Describes what could be rebuilt from the combined data.",
    "data_linkability_score": "Describes how easily the data could be linked.",
    "shared_information_count": "Describes how many data categories are shared.",
    "relationship_count": "Describes how many relationships exist between the assets.",
    "relationship_density": "Describes how connected the assets are.",
    "relationship_strength": "Describes how strong the relationships are.",
    "dependency_count": "Describes dependencies between the assets.",
    "dependency_strength": "Describes dependencies between the assets.",
    "network_connectivity": "Describes how connected the assets are.",
    "authentication_dependency": "Describes whether one asset authenticates to another.",
    "authentication_relationship_present": "Describes whether one asset authenticates to another.",
    "exploit_chain_potential": "A composite score built from several other features.",
    "attack_feasibility_score": "A composite score built from several other features.",
    "threat_interaction_score": "Describes how many threats apply.",
    "threat_severity": "Describes threat severity.",
    "common_threat_count": "Describes how many threats apply.",
    "combination_size": "The number of selected assets.",
    "asset_type_diversity": "The number of different asset types selected.",
}

# Business-context and requirement features: they describe the business side.
for _name in ["availability_requirement", "confidentiality_requirement", "integrity_requirement",
              "business_process_importance", "shared_business_process", "shared_business_process_strength",
              "operational_dependency", "financial_exposure", "regulatory_exposure", "reputational_exposure",
              "potential_financial_impact", "potential_operational_impact",
              "potential_regulatory_impact", "potential_reputational_impact"]:
    DESCRIPTIVE_FACTORS[_name] = "Describes business context, requirements or impact. It is not a control state."

DEFAULT_DESCRIPTIVE_REASON = "No defensible mapping to a control in the shortlist, so no ISO control is returned."


def get_risk_factor_to_control():
    """Return Table 3 as a DataFrame (one row per feature + ISO control pair)."""
    valid = set(get_iso_reference()["iso_control_id"])
    rows = []
    for i, (feature, iso_id, fit, why) in enumerate(_FACTOR_LINKS, start=1):
        assert feature in _FACTOR_INFO, feature + " has no entry in _FACTOR_INFO"
        assert iso_id in valid, feature + ": " + iso_id + " is not in the ISO reference"
        data_note, action, evidence = _FACTOR_INFO[feature]
        rows.append(("RF-" + str(i).zfill(2), feature, "Actionable", iso_id, fit,
                     why, action, evidence, data_note, MAPPING_STATUS))
    return pd.DataFrame(rows, columns=["mapping_id", "risk_factor", "factor_type", "iso_control_id",
                                       "fit", "mapping_rationale", "proposed_action",
                                       "evidence_required", "dataset_evidence", "status"])


# ---------------------------------------------------------------- Part 4
# map_to_iso(): takes the prediction and the explanation results and returns
# candidate ISO controls, proposed actions and the evidence to verify.
# It never loads or trains a model and never invents a feature or a value.

# coverage feature -> (flag name in inv.control_flags, plain name of the control)
_COVERAGE_FLAG = {
    "mfa_coverage": ("has_mfa", "an MFA control"),
    "encryption_coverage": ("has_encryption", "encryption at rest or full disk encryption"),
    "monitoring_coverage": ("has_monitoring", "a logging or monitoring control"),
}


def _to_number(value):
    """Turn a feature value into a number, or None if that is not possible."""
    if isinstance(value, str):
        low = value.strip().lower()
        if low in ("true", "yes"):
            return 1.0
        if low in ("false", "no"):
            return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _shows_gap(feature, value):
    """True when the feature value points to something that could be acted on."""
    number = _to_number(value)
    if number is None:
        return True                      # cannot tell, so keep it and let a human check
    if feature in _COVERAGE_FLAG:
        return number < 1.0              # 1.0 means every selected asset has the control
    return number > 0


def _find_feature(text, names):
    """Find the feature name inside a LIME rule such as 'mfa_coverage <= 0.50'."""
    matches = [n for n in names if n in str(text)]
    return max(matches, key=len) if matches else None


def _pairs(asset_ids):
    return [(asset_ids[i], asset_ids[j])
            for i in range(len(asset_ids)) for j in range(i + 1, len(asset_ids))]


def _asset_evidence(feature, asset_ids, inv):
    """Plain-language observations from the real data for ONE feature."""
    notes = []
    if feature in _COVERAGE_FLAG:
        flag, control_text = _COVERAGE_FLAG[feature]
        for a in asset_ids:
            if not inv.control_flags[a][flag]:
                notes.append((a, "No " + control_text + " recorded as Implemented or Partially Implemented."))
    elif feature == "monitoring_gap_score":
        for a in asset_ids:
            if not inv.control_flags[a]["has_monitoring"]:
                notes.append((a, "No logging or monitoring control recorded as Implemented or Partially Implemented."))
    elif feature == "known_exploited_present":
        for a in asset_ids:
            if inv.vuln_info[a]["known_exploited"]:
                notes.append((a, "Has a vulnerability marked as known exploited."))
    elif feature == "vulnerability_severity":
        for a in asset_ids:
            notes.append((a, "Highest CVSS score: " + str(inv.vuln_info[a]["max_cvss"])))
    elif feature in ("common_vulnerability_count", "vulnerability_interaction_score", "common_weakness_score"):
        for a1, a2 in _pairs(asset_ids):
            shared = set(inv.vuln_info[a1]["categories"]) & set(inv.vuln_info[a2]["categories"])
            if shared:
                notes.append((a1 + " and " + a2, "Share vulnerability categories: " + ", ".join(sorted(map(str, shared)))))
    elif feature in ("privileged_access_present", "privilege_escalation_potential"):
        for a1, a2 in _pairs(asset_ids):
            shared = inv.access_priv[a1] & inv.access_priv[a2]
            if shared:
                notes.append((a1 + " and " + a2, str(len(shared)) + " user(s) hold privileged access to both."))
    elif feature in ("shared_user_count", "shared_user_strength", "access_overlap_score", "shared_identity_score"):
        for a1, a2 in _pairs(asset_ids):
            shared = inv.access_all[a1] & inv.access_all[a2]
            if shared:
                notes.append((a1 + " and " + a2, str(len(shared)) + " user(s) have access to both."))
    elif feature == "data_flow_present":
        for a1, a2 in _pairs(asset_ids):
            for rel_type, _, flow in inv.rel_detail.get(tuple(sorted([a1, a2])), []):
                if flow is not None and str(flow) not in ("None", "nan"):
                    notes.append((a1 + " and " + a2, "Relationship '" + str(rel_type) + "' records a data flow: " + str(flow)))
    return notes


def map_to_iso(asset_ids, predicted_label, probability, shap_table, lime_table, inv,
               feature_values=None, feature_names=None, top_n=10):
    """
    asset_ids       : the selected assets, for example ["AST0084", "AST0120"]
    predicted_label : "Low", "Medium" or "High" from the trained model
    probability     : the model's probability for the predicted class (shown, not used)
    shap_table      : your shap_table (columns feature, value, shap) for the predicted class
    lime_table      : your lime_table (a rule column and a weight column) for the predicted class
    inv             : your EnterpriseInventory object
    feature_values  : optional dict of raw feature values (your raw_features)
    feature_names   : optional list of all model column names (your feature_cols)
    top_n           : how many of the strongest positive SHAP rows to consider

    Returns a dict of tables. Every row is a CANDIDATE for human review.
    """
    asset_ids = list(asset_ids)
    names = set(feature_names) if feature_names is not None else (
        set(_FACTOR_INFO) | set(ACTIONABLE_VIA_CONTROL_RECORDS) | set(DESCRIPTIVE_FACTORS))
    feature_values = feature_values or {}

    empty_cols = {
        "recommendations": ["risk_factor", "factor_value", "shap_value", "lime_weight", "explained_by",
                            "iso_control_id", "iso_control_title", "fit", "mapping_rationale",
                            "proposed_action", "evidence_required", "status"],
        "asset_evidence": ["scope", "risk_factor", "observation"],
        "control_record_candidates": ["asset_id", "erg_control_name", "implementation_status",
                                     "control_effectiveness", "candidate_iso_ids", "fit", "status"],
        "not_mapped": ["risk_factor", "explained_by", "reason"],
    }
    result = {"asset_ids": asset_ids, "predicted_label": predicted_label, "probability": probability,
              "caution": "All items are candidates for human review. A predicted High or Medium "
                         "combination does not prove ISO non-compliance."}
    for key, cols in empty_cols.items():
        result[key] = pd.DataFrame(columns=cols)

    if predicted_label not in ("Medium", "High"):
        result["summary"] = ("The prediction is " + str(predicted_label) +
                             ", so no recommendations are produced for this combination.")
        return result

    # ---- 1. factors that pushed toward the predicted class, from SHAP and from LIME
    for needed in ("feature", "shap"):
        if needed not in shap_table.columns:
            raise ValueError("shap_table needs a column named '" + needed + "'. It has: " + str(list(shap_table.columns)))
    factors = {}
    shap_pos = shap_table[shap_table["shap"] > 0].sort_values("shap", ascending=False).head(top_n)
    for _, r in shap_pos.iterrows():
        factors.setdefault(r["feature"], {})["shap"] = float(r["shap"])
        factors[r["feature"]]["value"] = r["value"]

    rule_col = next((c for c in lime_table.columns if "condition" in c.lower() or "rule" in c.lower()),
                    lime_table.columns[0])
    weight_col = next((c for c in lime_table.columns if "weight" in c.lower()), None)
    if weight_col is None:
        raise ValueError("lime_table needs a weight column. It has: " + str(list(lime_table.columns)))
    for _, r in lime_table[lime_table[weight_col] > 0].iterrows():
        feat = _find_feature(r[rule_col], names)
        if feat is None:
            feat = str(r[rule_col])
        factors.setdefault(feat, {})["lime"] = float(r[weight_col])

    # ---- 2. sort each factor into: mapped, control-record, or not mapped
    link_table = get_risk_factor_to_control()
    iso_titles = get_iso_reference().set_index("iso_control_id")["iso_control_title"].to_dict()
    erg_map = get_erg_control_to_iso().set_index("erg_control_name")
    recs, evid, ctrl_rows, skipped = [], [], [], []
    need_control_records = False

    for feat, info in factors.items():
        source = " and ".join(s for s, k in (("SHAP", "shap"), ("LIME", "lime")) if k in info)
        value = info.get("value", feature_values.get(feat))
        if feat in ACTIONABLE_VIA_CONTROL_RECORDS:
            if _shows_gap(feat, value):
                need_control_records = True
            else:
                skipped.append((feat, source, "Pushes toward the prediction, but the data shows no gap (value = " + str(value) + ")."))
        elif feat in set(link_table["risk_factor"]):
            if not _shows_gap(feat, value):
                skipped.append((feat, source, "Pushes toward the prediction, but the data shows no gap (value = " + str(value) + ")."))
                continue
            for _, link in link_table[link_table["risk_factor"] == feat].iterrows():
                recs.append({"risk_factor": feat, "factor_value": value,
                             "shap_value": info.get("shap"), "lime_weight": info.get("lime"),
                             "explained_by": source, "iso_control_id": link["iso_control_id"],
                             "iso_control_title": iso_titles[link["iso_control_id"]], "fit": link["fit"],
                             "mapping_rationale": link["mapping_rationale"],
                             "proposed_action": link["proposed_action"],
                             "evidence_required": link["evidence_required"], "status": MAPPING_STATUS})
            for scope, note in _asset_evidence(feat, asset_ids, inv):
                evid.append({"scope": scope, "risk_factor": feat, "observation": note})
        elif feat in DESCRIPTIVE_FACTORS:
            skipped.append((feat, source, "Descriptive. " + DESCRIPTIVE_FACTORS[feat]))
        else:
            base = next((b for b in DESCRIPTIVE_FACTORS if feat.startswith(b + "_")), None)
            reason = ("Descriptive. " + DESCRIPTIVE_FACTORS[base]) if base else DEFAULT_DESCRIPTIVE_REASON
            skipped.append((feat, source, reason))

    # ---- 3. control gaps: ISO candidates come from the real control records (Table 2)
    if need_control_records:
        records = inv.controls_df[inv.controls_df["asset_id"].isin(asset_ids)
                                  & (inv.controls_df["control_gap"] == True)]
        for _, r in records.iterrows():
            m = erg_map.loc[r["control_name"]]
            ctrl_rows.append({"asset_id": r["asset_id"], "erg_control_name": r["control_name"],
                              "implementation_status": r["implementation_status"],
                              "control_effectiveness": r["control_effectiveness"],
                              "candidate_iso_ids": m["candidate_iso_ids"] if m["candidate_iso_ids"] else "no mapping",
                              "fit": m["fit"], "status": MAPPING_STATUS})

    # ---- 4. merge repeated evidence lines, then build the result tables
    if evid:
        evid_df = pd.DataFrame(evid)
        evid = (evid_df.groupby(["scope", "observation"], sort=False)["risk_factor"]
                .agg(", ".join).reset_index()[empty_cols["asset_evidence"]].to_dict("records"))

    for key, rows in (("recommendations", recs), ("asset_evidence", evid),
                      ("control_record_candidates", ctrl_rows), ("not_mapped", skipped)):
        if rows:
            result[key] = pd.DataFrame(rows, columns=empty_cols[key]) if key == "not_mapped" else pd.DataFrame(rows)
    if len(result["recommendations"]):
        result["recommendations"] = result["recommendations"].sort_values(
            "shap_value", ascending=False, na_position="last").reset_index(drop=True)

    result["summary"] = (
        "Prediction: " + str(predicted_label) + ". Considered " + str(len(factors)) +
        " contributing factor(s): " + str(result["recommendations"]["risk_factor"].nunique()) +
        " mapped to candidate ISO controls, " + str(len(ctrl_rows)) +
        " control-gap record(s) listed, " + str(len(skipped)) + " not mapped.")
    return result


def show_report(result):
    """Print a map_to_iso() result in a readable order."""
    print(result["summary"])
    print(result["caution"])

    print("\nCANDIDATE ISO CONTROLS")
    recs = result["recommendations"]
    if len(recs):
        print(recs[["risk_factor", "explained_by", "iso_control_id", "iso_control_title", "fit"]].to_string(index=False))
        print("\nWHAT TO CHECK (proposed action and evidence, once per factor)")
        for feat in recs["risk_factor"].drop_duplicates():
            first = recs[recs["risk_factor"] == feat].iloc[0]
            print("- " + feat + ":")
            print("    Action  : " + first["proposed_action"])
            print("    Evidence: " + first["evidence_required"])
    else:
        print("(none)")

    print("\nCONTROL-GAP RECORDS (ISO candidates from Table 2)")
    gaps = result["control_record_candidates"]
    print(gaps[["asset_id", "erg_control_name", "implementation_status", "control_effectiveness",
                "candidate_iso_ids", "fit"]].to_string(index=False) if len(gaps) else "(none)")

    print("\nEVIDENCE FROM THE DATA")
    ev = result["asset_evidence"]
    if len(ev):
        for _, r in ev.iterrows():
            print("- " + str(r["scope"]) + " [" + r["risk_factor"] + "]: " + r["observation"])
    else:
        print("(none)")

    print("\nNOT MAPPED (one line per factor)")
    nm = result["not_mapped"]
    if len(nm):
        for _, r in nm.iterrows():
            print("- " + r["risk_factor"] + " (" + r["explained_by"] + "): " + r["reason"])
    else:
        print("(none)")


# ---------------------------------------------------------------- Part 5
# Maximum Coverage (built in small steps).
#
# Universe element  = (combination, ISO control) pair. It exists when the
#                     combination is flagged Medium or High AND one of its
#                     assets has a control-gap record whose control maps to
#                     that ISO control in Table 2.
# Candidate action  = one control-gap record of one asset (a row of
#                     02e_Controls with control_gap = True and at least one
#                     ISO candidate). The action covers every pair of every
#                     flagged combination that contains that asset.
# "Covered" means: at least one asset in the combination has a selected
# action for that ISO control. It does NOT mean the combination is compliant.

def build_coverage_inputs(inv, combinations_df, labels_df, flagged=("Medium", "High")):
    """Return the universe, the candidate actions and some counts."""
    erg = get_erg_control_to_iso().set_index("erg_control_name")

    # 1. flagged combinations (stored labels) and the assets inside each one
    merged = combinations_df[["combination_id", "asset_ids"]].merge(
        labels_df[["combination_id", "combined_criticality"]], on="combination_id")
    merged = merged[merged["combined_criticality"].isin(flagged)]
    assets_of = {r.combination_id: [a.strip() for a in str(r.asset_ids).split(",")]
                 for r in merged.itertuples()}
    label_of = dict(zip(merged["combination_id"], merged["combined_criticality"]))
    combos_of_asset = {}
    for cid, assets in assets_of.items():
        for a in assets:
            combos_of_asset.setdefault(a, []).append(cid)

    # 2. candidate actions from control-gap records
    gaps = inv.controls_df[inv.controls_df["control_gap"] == True]
    actions, covers, unmapped = [], {}, 0
    for g in gaps.itertuples():
        ids = [i for i in erg.loc[g.control_name, "candidate_iso_ids"].split("; ") if i]
        if not ids:
            unmapped += 1
            continue
        pairs = {(cid, iso) for cid in combos_of_asset.get(g.asset_id, []) for iso in ids}
        covers[g.control_id] = pairs
        actions.append({"action_id": g.control_id, "asset_id": g.asset_id,
                        "erg_control_name": g.control_name,
                        "implementation_status": g.implementation_status,
                        "iso_ids": "; ".join(ids), "fit": erg.loc[g.control_name, "fit"],
                        "pairs_covered": len(pairs)})

    universe = set().union(*covers.values()) if covers else set()
    return {"label_of": label_of, "assets_of": assets_of, "covers": covers,
            "universe": universe, "actions": pd.DataFrame(actions),
            "n_flagged": len(assets_of),
            "n_flagged_with_pair": len({cid for cid, _ in universe}),
            "n_gap_records": len(gaps), "n_gap_records_unmapped": unmapped}


def greedy_max_coverage(cov, k):
    """
    Greedy Maximum Coverage: at each step pick the action that covers the
    most pairs not yet covered (the largest marginal gain). Ties go to the
    lowest action_id so the result is the same every time.
    Stops early if no action adds anything new.
    For a limit of k actions this greedy method is guaranteed to reach at
    least 63% (1 - 1/e) of the best possible coverage. It is not guaranteed
    to find the best possible set.
    """
    meta = cov["actions"].set_index("action_id")
    remaining = dict(cov["covers"])
    covered, rows = set(), []
    for step in range(1, k + 1):
        best_id, best_gain = None, 0
        for action_id in sorted(remaining):
            gain = len(remaining[action_id] - covered)
            if gain > best_gain:
                best_id, best_gain = action_id, gain
        if best_id is None:
            break
        covered |= remaining.pop(best_id)
        touched = {cid for cid, _ in covered}
        high = sum(1 for c in touched if cov["label_of"][c] == "High")
        m = meta.loc[best_id]
        rows.append({"step": step, "action_id": best_id, "asset_id": m["asset_id"],
                     "erg_control_name": m["erg_control_name"],
                     "implementation_status": m["implementation_status"],
                     "iso_ids": m["iso_ids"], "fit": m["fit"],
                     "new_pairs": best_gain, "total_pairs_covered": len(covered),
                     "pct_of_universe": round(100.0 * len(covered) / len(cov["universe"]), 1),
                     "combinations_touched": len(touched), "high_touched": high,
                     "medium_touched": len(touched) - high,
                     "status": "Candidate - needs human review"})
    return pd.DataFrame(rows)
