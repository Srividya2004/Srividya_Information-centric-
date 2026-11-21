Information-Centric Contextual Risk Assessment of Low-Criticality Asset Combinations Using Explainable AI and Intelligent Compliance Mapping


1. Project Overview

Project Title: Information-Centric Contextual Risk Assessment of Low-Criticality Asset Combinations Using Explainable Machine Learning

GRC Pro is a research-based project that focuses on identifying contextual risks that may emerge when multiple enterprise assets, which are individually classified as Low-criticality, are combined.

The main idea is that individually Low-criticality assets may create a different risk level when considered together because of shared access, information sensitivity, vulnerabilities, relationships, business dependencies and security control gaps.

The research implementation uses enterprise asset data, contextual feature extraction, supervised machine learning and Explainable AI to assess and interpret the combined criticality of selected assets.

2. Research Objective

The primary objectives are:

- Analyze combinations of 2–4 individually Low-criticality enterprise assets.
- Extract contextual features from asset information and relationships.
- Predict combined criticality as Low, Medium or High.
- Compare multiple machine learning algorithms.
- Explain model predictions using SHAP and LIME.
- Map relevant risk factors to candidate ISO/IEC 27001:2022 Annex A controls.
- Prioritize candidate mitigation actions using a Maximum Coverage approach.

3. Research Pipeline

The GRC Pro research notebook follows the pipeline below.

Step 1 – Environment Setup

Import the required Python libraries and configure the notebook environment.

A random seed is set to 42 to improve reproducibility of random operations.

Step 2 – Enterprise Inventory Loading

The `EnterpriseInventory` class from `data_loader.py` loads enterprise information from the `ERG.xlsx` workbook.

The inventory contains:

- Enterprise asset information
- Asset information and sensitivity
- Existing asset risk information
- Asset relationships
- User and access information
- Threat information
- Vulnerability information
- Security controls
- Business processes

The inventory module also builds lookup structures to access asset-related information efficiently.

Step 3 – Dataset Loading

The research implementation reads the following sheets from the enterprise workbook:


| 05_Combination_Features | Contextual features of asset combinations |
| 06_Combined_Criticality_Labels | Combined criticality labels |
| 11_Model_TrainTest_Split | Predefined dataset split assignments |

Dataset overview:

| Total enterprise assets | 1,082 |
| Low-criticality assets | 649 |
| Asset combinations | 14,000 |
| Raw feature columns | 60 |
| Model input columns after encoding | 71 |

Target class distribution:

| Criticality | Records |
| Low | 5,705 |
| Medium | 5,507 |
| High | 2,788 |

Step 4 – Data Preprocessing

The dataset uses predefined training, validation and testing assignments.

| Dataset | Records |
| Training | 9,799 |
| Validation | 2,101 |
| Testing | 2,100 |

Preprocessing includes:

- Merging feature and label records using combination_id
- Label encoding of the target classes.
- One-hot encoding of categorical features.
- Preparing model input columns.

Five categorical feature columns are expanded during one-hot encoding, resulting in 71 model input columns.

Step 5 – Asset Combination Selection

The notebook allows selection of 2–4 asset IDs from the Low-criticality asset pool.

The selection is validated to ensure:

- At least two and at most four assets are selected.
- Duplicate asset IDs are not allowed.
- Every selected asset belongs to the Low-criticality asset pool.

Step 6 – Contextual Feature Extraction

The compute_features() function from feature_extraction.py analyzes the selected asset combination.

It generates 60 contextual features covering areas such as:

- Asset characteristics and type diversity
- Information sensitivity
- Asset relationships and dependencies
- Shared users and privileged access
- Common vulnerabilities
- Threat-related information
- Security control effectiveness and gaps
- Business, financial and reputational impact
- Emergent capability and risk amplification

emergent_capability_score = information angle × technical angle, when both are above 0. Otherwise it is 0.3 × their sum.
attack_feasibility_score = 0.4 × vulnerability interaction + 0.3 × privilege escalation + 0.3 × (1 − control effectiveness ÷ 10).
risk_amplification_score = 0.5 × emergent + 0.3 × attack feasibility + 0.2 × contextual information gain.

The generated feature dictionary is used for model input preparation.

Step 7 – Machine Learning Model Training and Comparison

Five supervised machine learning algorithms are evaluated:

1. Naive Bayes
2. Random Forest
3. XGBoost
4. LightGBM
5. CatBoost

The models are compared using the held-out test dataset.

Recorded test accuracy:

| Algorithm | Accuracy |
| Naive Bayes | 73.57% |
| Random Forest | 94.86% |
| XGBoost | 96.81% |
| LightGBM | 96.95% |
| CatBoost | 97.43% |

CatBoost achieved the highest test accuracy among the evaluated models and was selected for subsequent prediction and explanation.

Step 8 – Risk Prediction

The selected asset combination is converted into model-ready input using prepare_inference_row() from model_utils.py.

The trained CatBoost classifier predicts the combined criticality:

- Low
- Medium
- High

The prediction stage also provides class probabilities.

Step 9 – Explainable AI

The project uses two explainability techniques.

SHAP (SHapley Additive exPlanations)**

- Explains how individual features contribute to a model prediction.
- Identifies features that increase or decrease the model output.

LIME (Local Interpretable Model-agnostic Explanations)**

- Explains an individual prediction using a locally interpretable approximation.
- Helps understand the model's behaviour around a selected input.

The notebook also compares the SHAP and LIME explanations.

Step 10 – ISO/IEC 27001:2022 Control Mapping

The compliance mapping component connects relevant risk factors and control-gap information to candidate ISO/IEC 27001:2022 Annex A controls.

It identifies relevant candidate controls that may help address the contextual risk factors.



Step 11 – Maximum Coverage Optimization

The research implementation uses a greedy Maximum Coverage approach to prioritize candidate mitigation actions.

The objective is to select a limited number of actions that address the maximum number of defined combination-control pairs.

The algorithm repeatedly selects the action that covers the largest number of currently uncovered pairs.

The coverage output supports prioritization of potential mitigation activities.

4. Python Project Modules

The research implementation uses separate Python modules to organize reusable functionality.

| Python Module | Main Component / Function | Responsibility |
|---|---|---|
| data_loader.py| EnterpriseInventory| Loads enterprise workbook data and builds lookup structures |
| feature_extraction.py | compute_features() | Generates contextual features for selected asset combinations |
| model_utils.py | prepare_inference_row() | Prepares raw features in the model's expected input format |
| model_utils.py | train_and_save()| Provides functionality to train and save a CatBoost model |
| model_utils.py | load_model() | Provides functionality to load a saved model bundle |
| compliance_mapper.py | Mapping and coverage functions | Handles ISO control mapping and Maximum Coverage operations |
| explain.py | shap_explain(), lime_explain() | Provides reusable SHAP and LIME explanation functions |
| report.py | build_report(), print_report() | Provides report-generation functionality |

Important implementation note:

In GRC_Pro_clean.ipynb:

- data_loader.py is used to load the enterprise inventory.
- feature_extraction.py is used to generate contextual features.
- prepare_inference_row() from model_utils.py is used to prepare the selected combination for prediction.
- compliance_mapper.py is used in the compliance and Maximum Coverage stages.
- explain.py and report.py are imported in the notebook, but their functions are not called in the clean notebook execution.

The five machine learning algorithms are trained and compared in the notebook itself. The `train_and_save()` and `load_model()` functions in `model_utils.py` are available utilities, but they are not called in this notebook.

5. Python Libraries and Technologies

| Library / Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Excel reading and data manipulation |
| NumPy | Numerical operations |
| Scikit-learn | Preprocessing, label encoding and model evaluation |
| CatBoost | Gradient boosting classification |
| XGBoost | Gradient boosting classification |
| LightGBM | Gradient boosting classification |
| SHAP | Model explainability |
| LIME | Local model explainability |
| Joblib | Model serialization and loading |
| OpenPyXL | Excel workbook support |

6. Input and Output

Inputs:

- Enterprise inventory workbook (ERG.xlsx)
- Selected Low-criticality asset IDs
- Predefined combination feature and label data
- Predefined training, validation and testing assignments

Feature Value Generation and Data Representation

1. Overview

The compute_features() function in feature_extraction.py generates 60 contextual features for a selected combination of Low-criticality assets.

These features contain three types of data:

- Numerical values
- Categorical values
- Boolean values

The values are obtained from the enterprise inventory workbook (`ERG.xlsx`) and processed using Python operations such as sum(), max(), min(), len(), any(), averages, conditional statements and predefined mappings.

The function does not generate all values randomly or assign them manually. Most values are retrieved from existing inventory records or calculated using predefined rules in the feature extraction code.

2. Source of Feature Values

The EnterpriseInventory class in data_loader.py loads the required Excel worksheets and builds lookup dictionaries for efficient access.

| Excel Worksheet | Information Used |

| 01_Enterprise_Assets | Asset type and business process |
| 01b_Asset_Information | Information categories, sensitivity and sensitive-data flags |
| 01c_Asset_Risk_Info | Asset value, exposure, impact and control effectiveness scores |
| 02_Asset_Relationships | Asset relationships, relationship strength and data flow |
| 02b_Users_and_Access | Employee IDs and privileged access |
| 02c_Threats | Applicable threats and numerical threat severity |
| 02d_Vulnerabilities | Vulnerability categories, CVSS scores and known-exploited status |
| 02e_Controls | Control implementation status, control gaps and security control coverage |
| 00_Business_Processes | Business process importance |

The loaded records are converted into Python dictionaries, sets and DataFrames. The feature extraction function uses these structures to calculate combination-level features.

3. How Different Data Types Are Generated

A. Numerical Values

Numerical features are obtained either directly from the inventory or calculated using mathematical operations.

1. Direct numerical values**

Some values are retrieved directly from the asset records.

Examples:
- asset_value
- exposure_score
- financial_impact
- operational_impact
- regulatory_impact
- reputational_impact
- control_effectiveness_score
- cvss_score

2. Sum-based calculations

The values of selected assets are added together.

Example:

combined_asset_value = sum(
    inv.risk_lookup[a]["asset_value"]
    for a in asset_ids
)

3. Average-based calculations

The average impact and control effectiveness are calculated across the selected assets.

Formula:

Average = Sum of individual asset scores / Number of selected assets

Example:

fin_impact = sum(
    inv.risk_lookup[a]["financial_impact"]
    for a in asset_ids
) / n

4. Maximum-based calculations

The highest value among selected assets is identified using max().

Examples:
- Maximum information sensitivity
- Maximum vulnerability CVSS score

5. Derived numerical scores

Some features are calculated from other extracted features.

Examples:

information_overlap_score = min(
    shared_information_count / 3.0, 1.0
)

financial_exposure = fin_impact / 10.0

monitoring_gap_score = 1.0 - monitoring_coverage

These calculations produce numerical features, generally represented as counts, averages or decimal scores.

B. Categorical Values

Categorical features represent descriptive information such as Low, Medium, High or business-process importance.

Some categorical values are retrieved directly from the inventory, while others are generated using conditional rules.

1. Information sensitivity mapping**

The data_loader.py module converts sensitivity levels into numerical values:

SENS_NUM = {
    "Low": 3,
    "Medium": 6,
    "High": 9
}

The maximum sensitivity across the selected assets is identified.

max_sens_num = max(
    inv.info_flags[a]["max_sens_num"]
    for a in asset_ids
)

The maximum value is converted back into a categorical label:

combined_information_sensitivity = {
    3: "Low",
    6: "Medium",
    9: "High"
}[max_sens_num]

For example, if the selected assets have sensitivity values of 3, 6 and 9, the resulting combined sensitivity is High.

2. Confidentiality requirement

This feature uses the same value as the combined information sensitivity.

confidentiality_requirement = combined_information_sensitivity

3. Integrity requirement

This feature is assigned using conditional logic:

integrity_requirement = (
    "High" if max_sens_num == 9
    else ("Medium" if max_sens_num >= 6 else "Low")
)

4. Business-process importance

The business-process importance is retrieved from the corresponding business-process record when all selected assets belong to the same process. Otherwise, the value is set to - mixed.

5. Availability requirement

The current implementation selects one of the following values using a seeded random generator:

availability_requirement = rng_local.choice(
    ["Low", "Medium", "High"]
)

The seed makes the selection reproducible. This value is not calculated from the Excel availability-impact column in the current implementation.

C. Boolean Values (True / False)

Boolean features represent whether a particular condition exists.

They are derived using source flags and logical conditions.

1. Sensitive information flags**

The data_loader.py module checks whether any record for an asset contains a particular information type.

Example:

"pii": bool(df.contains_pii.any())

If at least one record indicates PII, the result is True. Otherwise, it is False.

The same approach is used for credentials, financial information and privileged information.

2. Privileged access

The function checks whether at least one privileged user is shared between selected assets.


privileged_access_present = len(all_shared_priv) > 0

3. Known exploited vulnerability

known_exploited_present = any(
    inv.vuln_info[a]["known_exploited"]
    for a in asset_ids
)

If any selected asset has a known-exploited vulnerability, the result is True.

4. Data flow

The function checks whether any recorded relationship has a valid data-flow value.

5. Shared business process

shared_business_process = len(processes) == 1

If all selected assets belong to the same business process, the result is True.

Other Boolean features include:
- data_flow_present
- authentication_relationship_present
- known_exploited_present
- privileged_access_present
- shared_business_process

4. Numerical Mapping of Relationship Strength

Relationship strength is converted into numerical values using a predefined mapping in `data_loader.py`.

STRENGTH_NUM = {
    "Weak": 3,
    "Moderate": 6,
    "Strong": 9
}

The numerical values are used to calculate average relationship strength.

This allows categorical relationship-strength values to be represented numerically during feature extraction.

5. Model Input Preprocessing

After calculating the 60 raw contextual features, the prepare_inference_row() function in model_utils.py prepares them for the trained CatBoost model.

The preprocessing includes:

1. Converting Boolean columns into integer values:
   - True becomes 1
   - False becomes 0

2. Applying one-hot encoding to categorical columns using pandas.get_dummies().

3. Aligning the resulting columns with the exact feature names and order used during model training.

4. Filling any missing encoded columns with 0.

The original research pipeline uses five categorical columns, which expand the 60 raw features into 71 model input columns.

6. Example of Feature Generation

For the selected assets:

asset_ids = 
    "AST0001",
    "AST0002",
    "AST0005"

The feature extraction function calculates values such as:

| Feature | Output | Generation Method |
| combination_size | 3 | Number of selected assets |
| combined_asset_value | 8.6 | Sum of asset values |
| combined_information_sensitivity | Medium | Maximum sensitivity mapping |
| shared_business_process | True | Business-process comparison |
| relationship_count | 0 | Count of recorded relationships |
| threat_severity | 6.0 | Average applicable threat severity |
| vulnerability_severity | 6.5 | Maximum CVSS score |
| control_effectiveness | 4.81 | Average control effectiveness |
| monitoring_gap_score | 1.0 | One minus monitoring coverage |
| potential_financial_impact | 1.6 | Average financial impact |
| financial_exposure | 0.16 | Financial impact divided by 10 |

These values represent the extracted contextual characteristics of the selected asset combination.

7. Final Prediction

The processed feature vector is passed to the trained CatBoost classifier.

The model evaluates the combination of numerical, categorical and Boolean features and predicts one of the criticality classes:

- Low
- Medium
- High

For the example combination `AST0001`, `AST0002` and `AST0005`, the model predicted Medium.

The predicted class is generated by CatBoost and is not directly copied from the existing dataset label.


Outputs:

- Contextual feature values for selected asset combinations
- Predicted combined criticality
- Class probabilities
- SHAP feature contributions
- LIME local explanations
- SHAP and LIME comparison
- Candidate ISO control mappings
- Maximum Coverage action prioritization results

7. Important Research Scope and Limitations

- The research scope focuses on combinations of 2–4 individually Low-criticality assets.
- The 14,000 combination records and their target labels are loaded from the prepared workbook.
- Model accuracy is measured against the stored dataset labels; it should not be interpreted as independently validated real-world risk detection accuracy.
- ISO control mappings are candidate mappings and require human review.
- Maximum Coverage identifies candidate coverage, not confirmed risk elimination or completed compliance.
- The clean research notebook trains and compares models in memory; it does not load `trained_model.pkl`.

8. Expected Outcome

GRC Pro provides a research workflow that moves from enterprise asset information to contextual risk prediction, model explanation, candidate compliance control mapping and mitigation action prioritization.

The objective is to support more informed risk assessment when individually Low-criticality assets are evaluated as a combination rather than only as isolated assets.
