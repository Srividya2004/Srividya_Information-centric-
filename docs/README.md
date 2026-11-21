Project documentation and architecture diagrams.


<img width="1400" height="722" alt="image" src="https://github.com/user-attachments/assets/1fda8749-10da-4852-b450-9146be8aaec3" />
Architecture Overview

The above diagram illustrates the overall architecture of our Information-Centric Contextual Risk Assessment system.

The system starts by loading enterprise asset information from the ERG dataset. The data loader processes the inventory, and the feature extraction module generates contextual features for selected asset combinations.

The CatBoost machine learning model predicts the contextual risk level as Low, Medium, or High. SHAP and LIME are used to explain the model's predictions.

The compliance mapper connects relevant risk factors to candidate ISO/IEC 27001:2022 Annex A controls. The Maximum Coverage algorithm then prioritizes security actions based on their coverage of identified combination-control pairs.

Finally, the Flask web application integrates these components and presents risk predictions, explanations, compliance recommendations, and reports through a user interface.
