# Machine Learning Models for Asthma Prediction

This folder contains the trained machine learning models.
These models are serialized as `.bin` files using Python's `pickle` and can be loaded directly for inference.

---

## 📂 Models Included

1. **Classification Model**  
`model_xgb_class_eda=0.05_max_depth=6_min_child_weight=30.bin`  

- **Purpose:** Predicts the probability of a patient having asthma.
- **Algorithm:** XGBoost classifier.
- **Preprocessing:** Uses a DictVectorizer (`dv_class`) to transform input patient features.
- **Key Features Required:**
  - `BIRTH_YEAR`
  - `GENDER_FACTOR`
  - `RACE_FACTOR`
  - `ETHNICITY_FACTOR`
  - `PAYER_FACTOR`
  - `ATOPIC_MARCH_COHORT`
  - `AGE_START_YEARS`
  - `NUM_ALLERGIES`

2. **Regression Model**  
`model_xgb_reg_eda=0.05_max_depth=6_min_child_weight=30.bin`

- **Purpose:** Predicts the age at which a patient may develop asthma, **if at risk**.
- **Algorithm:** XGBoost regressor.
- **Preprocessing:** Uses a DictVectorizer (`dv_reg`) to transform input patient features, including predicted asthma probability.
- **Key Features Required:**
  - Allergy start ages (`SHELLFISH_ALG_START`, `FISH_ALG_START`, `MILK_ALG_START`, etc.)
  - Atopic conditions (`ATOPIC_DERM_START`, `ALLERGIC_RHINITIS_START`)
  - `ASTHMA_PRED_PROBA` (predicted probability from classification model)
