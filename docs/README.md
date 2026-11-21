Project documentation and architecture diagrams.


<img width="1400" height="722" alt="image" src="https://github.com/user-attachments/assets/1fda8749-10da-4852-b450-9146be8aaec3" />
Architecture Overview

The above diagram illustrates the overall architecture of our Information-Centric Contextual Risk Assessment system.

The system starts by loading enterprise asset information from the ERG dataset. The data loader processes the inventory, and the feature extraction module generates contextual features for selected asset combinations.

The CatBoost machine learning model predicts the contextual risk level as Low, Medium, or High. SHAP and LIME are used to explain the model's predictions.

The compliance mapper connects relevant risk factors to candidate ISO/IEC 27001:2022 Annex A controls. The Maximum Coverage algorithm then prioritizes security actions based on their coverage of identified combination-control pairs.

Finally, the Flask web application integrates these components and presents risk predictions, explanations, compliance recommendations, and reports through a user interface.

Project Workflow diagram

<img width="1772" height="1256" alt="image" src="https://github.com/user-attachments/assets/f734dc5e-4408-4483-b9f4-ff99abc4e2fa" />

### Project Workflow

The workflow begins with loading enterprise asset information from the ERG dataset. The selected low-criticality assets are combined to assess their contextual risk.

The system extracts 60 contextual features based on asset characteristics, relationships, vulnerabilities, information sensitivity, and security controls. These features are aligned with the model's expected input schema and passed to the trained CatBoost classifier.

The model predicts the combined risk category as Low, Medium, or High. SHAP and LIME provide explanations for the prediction by identifying influential features.

The compliance mapping module connects relevant risk factors and enterprise security controls to candidate ISO/IEC 27001:2022 Annex A controls. Finally, the Greedy Maximum Coverage algorithm prioritizes security actions based on their coverage of identified combination-control pairs.

The results are presented through the Flask web application for assessment, review, and reporting.
