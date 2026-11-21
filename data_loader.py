"""
data_loader.py
--------------
Loads the enterprise inventory (ERG.xlsx) ONCE and builds fast lookup
structures. This is what "storing the enterprise asset inventory" means in
practice -- these are plain Python dicts/sets, rebuilt from the 7 raw tables,
not a precomputed table of combination outputs.

WHAT ALREADY EXISTED (from the research pipeline): the logic to build these
exact lookups was scattered across full_part3.py-full_part6.py, built once
for a batch run. This module extracts and generalizes that logic into
reusable, importable functions -- no modeling logic changes.
"""
import pandas as pd
import numpy as np

STRENGTH_NUM = {"Weak": 3, "Moderate": 6, "Strong": 9}
SENS_NUM = {"Low": 3, "Medium": 6, "High": 9}
MFA_NAMES = {"MFA", "MFA / SSO", "Administrative MFA", "MFA for Administrative Access"}
ENCRYPTION_NAMES = {"Encryption at Rest", "Encryption in Transit", "Full Disk Encryption"}
MONITORING_NAMES = {"Logging", "Logging and Monitoring", "Activity Logging", "Access Logging",
                     "Application Logging", "File Access Logging", "Database Activity Logging",
                     "Log Integrity Protection"}


class EnterpriseInventory:
    """
    Loads all 7 raw tables once and exposes fast per-asset lookups.
    This object is built ONCE at framework startup (or refreshed on a
    schedule, e.g. nightly) -- NOT rebuilt per query.
    """

    def __init__(self, xlsx_path):
        self.xlsx_path = xlsx_path
        self._load_raw_tables()
        self._build_lookups()

    def _load_raw_tables(self):
        p = self.xlsx_path
        self.assets_df = pd.read_excel(p, sheet_name="01_Enterprise_Assets")
        self.info_df = pd.read_excel(p, sheet_name="01b_Asset_Information")
        self.risk_df = pd.read_excel(p, sheet_name="01c_Asset_Risk_Info")
        self.rel_df = pd.read_excel(p, sheet_name="02_Asset_Relationships")
        self.access_df = pd.read_excel(p, sheet_name="02b_Users_and_Access")
        self.threats_df = pd.read_excel(p, sheet_name="02c_Threats")
        self.vuln_df = pd.read_excel(p, sheet_name="02d_Vulnerabilities")
        self.controls_df = pd.read_excel(p, sheet_name="02e_Controls")
        self.business_processes_df = pd.read_excel(p, sheet_name="00_Business_Processes")
        # existing combinations -- used ONLY to prove a query combo is "new", never for lookup
        self.existing_combos_df = pd.read_excel(p, sheet_name="04_Generated_Combinations")

    def _build_lookups(self):
        risk = self.risk_df
        self.low_asset_ids = set(risk[risk.existing_criticality == "Low"].asset_id)
        print(f"[EnterpriseInventory] Loaded {len(self.assets_df)} assets, "
              f"{len(self.low_asset_ids)} Low-critical, from {self.xlsx_path}")

        # --- information flags per asset (from Asset_Information) ---
        self.info_flags = {}
        info_by_asset = self.info_df.groupby("asset_id")
        for a in self.low_asset_ids:
            try:
                df = info_by_asset.get_group(a)
            except KeyError:
                df = self.info_df.iloc[0:0]
            self.info_flags[a] = {
                "pii": bool(df.contains_pii.any()) if len(df) else False,
                "credentials": bool(df.contains_credentials.any()) if len(df) else False,
                "financial": bool(df.contains_financial_information.any()) if len(df) else False,
                "privileged": bool(df.contains_privileged_information.any()) if len(df) else False,
                "ip": bool(df.contains_intellectual_property.any()) if len(df) else False,
                "categories": set(df.information_category.tolist()) if len(df) else set(),
                "max_sens_num": SENS_NUM.get(
                    "High" if len(df) and "High" in df.data_sensitivity.values else
                    ("Medium" if len(df) and "Medium" in df.data_sensitivity.values else "Low"), 3),
            }

        # --- access lookups (from Users_and_Access) ---
        self.access_all, self.access_priv = {}, {}
        access_by_asset = self.access_df.groupby("asset_id")
        for a in self.low_asset_ids:
            try:
                df = access_by_asset.get_group(a)
            except KeyError:
                df = self.access_df.iloc[0:0]
            self.access_all[a] = set(df.employee_id.tolist())
            self.access_priv[a] = set(df[df.privileged_access == True].employee_id.tolist())

        # --- vulnerability lookups ---
        self.vuln_info = {}
        vuln_by_asset = self.vuln_df.groupby("asset_id")
        for a in self.low_asset_ids:
            try:
                df = vuln_by_asset.get_group(a)
            except KeyError:
                df = self.vuln_df.iloc[0:0]
            self.vuln_info[a] = {
                "categories": set(df.vulnerability_category.tolist()) if len(df) else set(),
                "known_exploited": bool(df.known_exploited.any()) if len(df) else False,
                "max_cvss": float(df.cvss_score.max()) if len(df) else 0.0,
            }

        # --- control lookups ---
        self.control_flags = {}
        controls_by_asset = self.controls_df.groupby("asset_id")
        for a in self.low_asset_ids:
            try:
                df = controls_by_asset.get_group(a)
            except KeyError:
                df = self.controls_df.iloc[0:0]
            implemented = df[df.implementation_status.isin(["Implemented", "Partially Implemented"])] if len(df) else df
            self.control_flags[a] = {
                "gap_count": int(df.control_gap.sum()) if len(df) else 0,
                "has_mfa": bool(implemented.control_name.isin(MFA_NAMES).any()) if len(implemented) else False,
                "has_encryption": bool(implemented.control_name.isin(ENCRYPTION_NAMES).any()) if len(implemented) else False,
                "has_monitoring": bool(implemented.control_name.isin(MONITORING_NAMES).any()) if len(implemented) else False,
            }

        # --- risk / business-impact lookup ---
        self.risk_lookup = self.risk_df.set_index("asset_id").to_dict("index")

        # --- asset type / business process lookups ---
        self.process_by_asset = self.assets_df.set_index("asset_id")["business_process_id"].to_dict()
        self.asset_type_by_id = self.assets_df.set_index("asset_id")["asset_type"].to_dict()

        # --- relationship lookup (only edges between two Low-critical assets) ---
        self.rel_detail = {}
        rel_low = self.rel_df[self.rel_df.source_asset_id.isin(self.low_asset_ids) &
                                self.rel_df.target_asset_id.isin(self.low_asset_ids)]
        for _, r in rel_low.iterrows():
            key = tuple(sorted([r.source_asset_id, r.target_asset_id]))
            self.rel_detail.setdefault(key, []).append((r.relationship_type, r.relationship_strength, r.data_flow))

        # --- threats grouped by applicable asset type ---
        self.threats_by_type = {t: g for t, g in self.threats_df.groupby("applicable_asset_type")}

        # --- existing combination set (for "is this new?" checks only) ---
        self.existing_combo_sets = set(
            frozenset(x.strip() for x in ids.split(","))
            for ids in self.existing_combos_df.asset_ids
        )

    def is_new_combination(self, asset_ids):
        """True if this exact asset set was NOT among the 14,000 training combinations."""
        return frozenset(asset_ids) not in self.existing_combo_sets

    def asset_summary(self, asset_id):
        row = self.assets_df[self.assets_df.asset_id == asset_id].iloc[0]
        return {
            "asset_id": asset_id, "asset_type": row.asset_type, "asset_subtype": row.asset_subtype,
            "department": row.department, "technology_platform": row.technology_platform,
            "existing_criticality": self.risk_lookup[asset_id]["existing_criticality"],
        }


if __name__ == "__main__":
    inv = EnterpriseInventory("ERG.xlsx")
    print("Sample Low-critical asset IDs:", list(inv.low_asset_ids)[:5])
