"""
feature_extraction.py
----------------------
This is compute_features_v2() extracted from the research pipeline
(redesign_part1.py) into a standalone, reusable function. IT IS THE SAME
LOGIC used to build all 14,000 training rows -- nothing about the formula
changes for a new combination. The only difference is WHEN it's called:
during research, it was called in a loop over pre-sampled combos; here, it's
called once, on demand, for whatever asset_ids an analyst just selected.
"""
import itertools
import numpy as np

from data_loader import STRENGTH_NUM


def compute_features(asset_ids, inv, rng_seed=202):
    """
    asset_ids: list of 2-5 Low-critical asset_id strings (analyst-selected)
    inv: an EnterpriseInventory instance (built once, reused across calls)
    Returns: dict of 61 features, IDENTICAL schema to 05_Combination_Features
    """
    import random
    rng_local = random.Random(rng_seed)

    n = len(asset_ids)
    types_present = set(inv.asset_type_by_id[a] for a in asset_ids)
    asset_type_diversity = len(types_present)

    combined_asset_value = sum(inv.risk_lookup[a]["asset_value"] for a in asset_ids)
    combined_exposure = sum(inv.risk_lookup[a]["exposure_score"] for a in asset_ids)
    fin_impact = sum(inv.risk_lookup[a]["financial_impact"] for a in asset_ids) / n
    op_impact = sum(inv.risk_lookup[a]["operational_impact"] for a in asset_ids) / n
    reg_impact = sum(inv.risk_lookup[a]["regulatory_impact"] for a in asset_ids) / n
    rep_impact = sum(inv.risk_lookup[a]["reputational_impact"] for a in asset_ids) / n
    control_eff_avg = sum(inv.risk_lookup[a]["control_effectiveness_score"] for a in asset_ids) / n

    max_sens_num = max(inv.info_flags[a]["max_sens_num"] for a in asset_ids)
    combined_information_sensitivity = {3: "Low", 6: "Medium", 9: "High"}[max_sens_num]

    pii_assets = {a for a in asset_ids if inv.info_flags[a]["pii"]}
    cred_assets = {a for a in asset_ids if inv.info_flags[a]["credentials"]}
    fin_assets = {a for a in asset_ids if inv.info_flags[a]["financial"]}
    priv_assets = {a for a in asset_ids if inv.info_flags[a]["privileged"]}

    pair_checks = [
        len(pii_assets) > 0 and len(cred_assets - pii_assets) > 0,
        len(pii_assets) > 0 and len(priv_assets - pii_assets) > 0,
        len(fin_assets) > 0 and len(cred_assets - fin_assets) > 0,
        len(fin_assets) > 0 and len(priv_assets - fin_assets) > 0,
        len(pii_assets) > 0 and len(fin_assets - pii_assets) > 0,
        len(cred_assets) > 0 and len(priv_assets - cred_assets) > 0,
    ]
    information_complementarity_score = round(sum(pair_checks) / len(pair_checks), 2)

    cat_asset_count = {}
    for a in asset_ids:
        for cat in inv.info_flags[a]["categories"]:
            cat_asset_count[cat] = cat_asset_count.get(cat, 0) + 1
    shared_information_count = sum(1 for v in cat_asset_count.values() if v > 1)
    information_overlap_score = round(min(shared_information_count / 3.0, 1.0), 2)

    distinct_categories = len(cat_asset_count)
    data_linkability_score = round(min((len(pii_assets) > 0) * (distinct_categories / 5.0), 1.0), 2)

    sensitive_categories_multi_asset = sum(1 for cat, cnt in cat_asset_count.items()
                                            if cnt > 1 and cat in {"PII", "Credentials", "Privileged", "Financial/PII", "Financial/HR"})
    information_reconstruction_potential = round(min(sensitive_categories_multi_asset / 2.0, 1.0), 2)

    avg_asset_sens = np.mean([inv.info_flags[a]["max_sens_num"] for a in asset_ids])
    contextual_information_gain = round(max(0.0, (max_sens_num - avg_asset_sens) / 9.0), 2)

    confidentiality_requirement = combined_information_sensitivity
    integrity_requirement = "High" if max_sens_num == 9 else ("Medium" if max_sens_num >= 6 else "Low")
    availability_requirement = rng_local.choice(["Low", "Medium", "High"])

    pairs = list(itertools.combinations(asset_ids, 2))
    rel_hits = []
    for a1, a2 in pairs:
        key = tuple(sorted([a1, a2]))
        rel_hits.extend(inv.rel_detail.get(key, []))
    relationship_count = len(rel_hits)
    relationship_strength = round(sum(STRENGTH_NUM.get(s, 3) for _, s, _ in rel_hits) / relationship_count, 2) if relationship_count else 0.0
    dep_types = {"depends_on", "authenticates_to", "backs_up", "replicates_to", "administers"}
    dependency_count = sum(1 for t, _, _ in rel_hits if t in dep_types)
    dependency_strength = round(min(dependency_count / 3.0, 1.0), 2)
    data_flow_present = any(df_ != "None" and df_ is not None and not (isinstance(df_, float) and np.isnan(df_)) for _, _, df_ in rel_hits)
    authentication_relationship_present = any(t == "authenticates_to" for t, _, _ in rel_hits)
    max_possible_edges = len(pairs)
    relationship_density = round(relationship_count / max_possible_edges, 2) if max_possible_edges else 0.0
    network_connectivity = round(min(relationship_density * 1.5, 1.0), 2)

    processes = set(inv.process_by_asset.get(a) for a in asset_ids)
    shared_business_process = len(processes) == 1
    business_process_importance = (
        inv.business_processes_df.set_index("process_id").loc[list(processes)[0], "business_importance"]
        if shared_business_process else "mixed"
    )
    shared_business_process_strength = round(1.0 if shared_business_process else (1.0 / len(processes)), 2)

    all_shared_users, all_shared_priv = set(), set()
    for a1, a2 in pairs:
        all_shared_users |= (inv.access_all[a1] & inv.access_all[a2])
        all_shared_priv |= (inv.access_priv[a1] & inv.access_priv[a2])
    shared_user_count = len(all_shared_users)
    shared_user_strength = round(min(shared_user_count / 3.0, 1.0), 2)
    privileged_access_present = len(all_shared_priv) > 0
    access_overlap_score = round(min((shared_user_count + 2 * len(all_shared_priv)) / 5.0, 1.0), 2)
    shared_identity_score = round(min(len(all_shared_users) / max(n, 1) / 2.0, 1.0), 2)
    privilege_escalation_potential = round(min((2 if privileged_access_present else 0) +
                                                (1 if authentication_relationship_present else 0), 3) / 3.0, 2)
    authentication_dependency = round(1.0 if authentication_relationship_present else 0.0, 2)

    combo_vuln_cats = [inv.vuln_info[a]["categories"] for a in asset_ids]
    cat_count_vuln = {}
    for cs in combo_vuln_cats:
        for c in cs:
            cat_count_vuln[c] = cat_count_vuln.get(c, 0) + 1
    common_vulnerability_count = sum(1 for v in cat_count_vuln.values() if v > 1)
    vulnerability_severity = round(max((inv.vuln_info[a]["max_cvss"] for a in asset_ids), default=0.0), 2)
    known_exploited_present = any(inv.vuln_info[a]["known_exploited"] for a in asset_ids)
    vulnerability_interaction_score = round(min((common_vulnerability_count / 2.0) + (0.3 if known_exploited_present else 0), 1.0), 2)
    common_weakness_score = round(min(common_vulnerability_count / 3.0, 1.0), 2)

    applicable_threats = None
    frames = [inv.threats_by_type[t] for t in types_present if t in inv.threats_by_type]
    import pandas as pd
    applicable_threats = pd.concat(frames) if frames else pd.DataFrame()
    common_threat_count = len(applicable_threats)
    threat_severity = round(applicable_threats.severity_numeric.mean(), 2) if len(applicable_threats) else 0.0
    threat_interaction_score = round(min(common_threat_count / 6.0, 1.0), 2)

    control_gap_count = sum(inv.control_flags[a]["gap_count"] for a in asset_ids)
    exploit_chain_potential = round(min((1 if dependency_count > 0 else 0) +
                                         (1 if known_exploited_present else 0) +
                                         (1 if control_gap_count > 0 else 0), 3) / 3.0, 2)

    mfa_coverage = round(sum(inv.control_flags[a]["has_mfa"] for a in asset_ids) / n, 2)
    encryption_coverage = round(sum(inv.control_flags[a]["has_encryption"] for a in asset_ids) / n, 2)
    monitoring_coverage = round(sum(inv.control_flags[a]["has_monitoring"] for a in asset_ids) / n, 2)
    combined_control_effectiveness = round(control_eff_avg, 2)
    control_gap_interaction = round(min(control_gap_count / (2 * n), 1.0), 2)
    monitoring_gap_score = round(1.0 - monitoring_coverage, 2)

    financial_exposure = round(fin_impact / 10.0, 2)
    operational_dependency = round(min(op_impact / 10.0 + dependency_strength * 0.3, 1.0), 2)
    regulatory_exposure = round(reg_impact / 10.0, 2)
    reputational_exposure = round(rep_impact / 10.0, 2)

    info_angle = max(information_complementarity_score, information_reconstruction_potential)
    technical_angle = max(privilege_escalation_potential, exploit_chain_potential)
    emergent_capability_score = round(info_angle * technical_angle, 2) if (info_angle > 0 and technical_angle > 0) else round(0.3 * (info_angle + technical_angle), 2)

    attack_feasibility_score = round(min(
        0.4 * vulnerability_interaction_score + 0.3 * privilege_escalation_potential +
        0.3 * (1 - combined_control_effectiveness / 10.0), 1.0), 2)

    risk_amplification_score = round(min(
        emergent_capability_score * 0.5 + attack_feasibility_score * 0.3 +
        contextual_information_gain * 0.2, 1.0), 2)

    feats = {
        "combination_size": n, "asset_type_diversity": asset_type_diversity,
        "combined_asset_value": round(combined_asset_value, 2),
        "combined_information_sensitivity": combined_information_sensitivity,
        "information_complementarity_score": information_complementarity_score,
        "shared_information_count": shared_information_count,
        "information_overlap_score": information_overlap_score,
        "data_linkability_score": data_linkability_score,
        "information_reconstruction_potential": information_reconstruction_potential,
        "contextual_information_gain": contextual_information_gain,
        "confidentiality_requirement": confidentiality_requirement,
        "integrity_requirement": integrity_requirement,
        "availability_requirement": availability_requirement,
        "relationship_count": relationship_count, "relationship_strength": relationship_strength,
        "dependency_count": dependency_count, "dependency_strength": dependency_strength,
        "data_flow_present": data_flow_present,
        "relationship_density": relationship_density, "network_connectivity": network_connectivity,
        "shared_business_process": shared_business_process, "business_process_importance": business_process_importance,
        "shared_business_process_strength": shared_business_process_strength,
        "shared_user_count": shared_user_count, "shared_user_strength": shared_user_strength,
        "privileged_access_present": privileged_access_present,
        "access_overlap_score": access_overlap_score, "shared_identity_score": shared_identity_score,
        "privilege_escalation_potential": privilege_escalation_potential,
        "authentication_relationship_present": authentication_relationship_present,
        "authentication_dependency": authentication_dependency,
        "common_threat_count": common_threat_count, "threat_severity": threat_severity,
        "threat_interaction_score": threat_interaction_score,
        "common_vulnerability_count": common_vulnerability_count, "vulnerability_severity": vulnerability_severity,
        "vulnerability_interaction_score": vulnerability_interaction_score, "common_weakness_score": common_weakness_score,
        "known_exploited_present": known_exploited_present, "combined_exposure_score": round(combined_exposure, 2),
        "exploit_chain_potential": exploit_chain_potential,
        "control_gap_count": control_gap_count, "control_effectiveness": round(control_eff_avg, 2),
        "combined_control_effectiveness": combined_control_effectiveness,
        "control_gap_interaction": control_gap_interaction, "monitoring_gap_score": monitoring_gap_score,
        "mfa_coverage": mfa_coverage, "encryption_coverage": encryption_coverage, "monitoring_coverage": monitoring_coverage,
        "potential_financial_impact": round(fin_impact, 2), "potential_operational_impact": round(op_impact, 2),
        "potential_regulatory_impact": round(reg_impact, 2), "potential_reputational_impact": round(rep_impact, 2),
        "financial_exposure": financial_exposure, "operational_dependency": operational_dependency,
        "regulatory_exposure": regulatory_exposure, "reputational_exposure": reputational_exposure,
        "emergent_capability_score": emergent_capability_score,
        "attack_feasibility_score": attack_feasibility_score,
        "risk_amplification_score": risk_amplification_score,
    }
    return feats
