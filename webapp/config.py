"""Application settings. Nothing here changes research logic."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESEARCH_DIR = BASE_DIR / "research"          # your original modules, copied unchanged
ERG_PATH = Path(os.environ.get("GRC_ERG_PATH", BASE_DIR / "data" / "ERG.xlsx"))

# Selection rules copied from notebook GRC_Pro_clean.ipynb (the asset-selection cell):
#   "You must select between 2 and 4 assets"
MIN_ASSETS = 2
MAX_ASSETS = 4

SEARCH_MAX_QUERY_LEN = 100
SEARCH_DEFAULT_LIMIT = 25
SEARCH_MAX_LIMIT = 100
MAX_INPUT_ITEMS = 50          # refuse absurdly long lists before processing
MAX_ID_LEN = 32

# ---- Phase 2+ ----
MODEL_PATH = Path(os.environ.get("GRC_MODEL_PATH", BASE_DIR / "data" / "trained_model.pkl"))
DB_PATH = Path(os.environ.get("GRC_DB_PATH", BASE_DIR / "instance" / "grc.db"))

# LIME settings copied from notebook cell "LIME" (not from explain.py):
LIME_BACKGROUND_ROWS = 300      # X_train.sample(300, random_state=42)
LIME_RANDOM_STATE = 42
LIME_NUM_FEATURES = 10
LIME_NUM_SAMPLES = 3000
SHAP_TOP_N = 10                 # notebook shows the top 10 by absolute SHAP

# Presentation only (does not change any result): show a caution when LIME's local fit is weaker.
# 0.5 is MY default - not from your notebook; change it here if your guide prefers another cutoff.
LIME_R2_WARN_BELOW = 0.5

COVERAGE_DEFAULT_K = 10
COVERAGE_MAX_K = 50             # notebook examined K = 1, 3, 5, 10, 20, 50
