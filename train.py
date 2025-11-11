#!/usr/bin/env python
# coding: utf-8

# 0. Importing the libs and read the data

# Data manipulation and visualization
import pandas as pd
import matplotlib.pyplot as plt

# Machine Learning models
import xgboost as xgb

# Data splitting and preprocessing
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer

# Save the model
import pickle

# Read the data
df = pd.read_csv('./data/food-allergy-analysis-Zenodo.csv')

# 1. Data preparation and data cleaning

# All the column names that contain '_END' in their name along with specific asthma-related columns
end_columns = [col for col in df.columns if '_END' in col] + ['FIRST_ASTHMARX', 'LAST_ASTHMARX', 'NUM_ASTHMARX']
df = df.drop(columns=end_columns)

# Mapping dictionary for gender values
gender_mapping = {
    'S1 - Female': 'F',
    'S0 - Male': 'M'
}
# Map the gender values
df['GENDER_FACTOR'] = df['GENDER_FACTOR'].map(gender_mapping)

# Mapping dictionary for race values
race_mapping = {
    'R0 - White': 'White',
    'R1 - Black': 'African American',
    'R2 - Asian or Pacific Islander': 'Asian/Pacific Islander',
    'R3 - Other': 'Other',
    'R4 - Unknown': 'Unknown'
}
# Map the race values
df['RACE_FACTOR'] = df['RACE_FACTOR'].map(race_mapping)

# Mapping dictionary for ethnicity values
ethnicity_mapping = {
    'E0 - Non-Hispanic': 'Non-Hispanic',
    'E1 - Hispanic': 'Hispanic'
}
# Map the race values
df['ETHNICITY_FACTOR'] = df['ETHNICITY_FACTOR'].map(ethnicity_mapping)

# Mapping dictionary for payer values
payer_mapping = {
    'P0 - Non-Medicaid': 'Non-Medicaid',
    'P1 - Medicaid': 'Medicaid'
}
# Map the race values
df['PAYER_FACTOR'] = df['PAYER_FACTOR'].map(payer_mapping)

# All the column names that end with '_START'
start_columns = [col for col in df.columns if col.endswith('_START')]
# Create new binary columns fit the classification machine learning model
for col in start_columns:
    new_col_name = col.replace('_START', '')
    df[new_col_name] = df[col].notnull().astype(bool)

# Get all the alergy boolean columns
allergy_bool_columns = df.select_dtypes(include=['bool']).columns.tolist()
if 'ATOPIC_MARCH_COHORT' in allergy_bool_columns: allergy_bool_columns.remove('ATOPIC_MARCH_COHORT')

# Create a new column 'NUM_ALLERGIES' that counts the number of allergies for each subject
df['NUM_ALLERGIES'] = df[allergy_bool_columns].sum(axis=1).astype(int)

## 3.1. Split the data - Classification Model
# - Split the data in train/val/test sets with 60%/20%/20% distribution.

classification_features = [
    'BIRTH_YEAR',
    'GENDER_FACTOR',
    'RACE_FACTOR',
    'ETHNICITY_FACTOR',
    'PAYER_FACTOR',
    'ATOPIC_MARCH_COHORT',
    'AGE_START_YEARS',
    'NUM_ALLERGIES'
]

target_allergy = ['ASTHMA']
df_classification = df[classification_features + target_allergy]

df_class_full_train, df_class_test = train_test_split(df_classification, test_size=0.2, random_state=1)
df_class_train, df_class_val = train_test_split(df_class_full_train, test_size=0.25, random_state=1)

df_class_train = df_class_train.reset_index(drop=True)
df_class_val = df_class_val.reset_index(drop=True)
df_class_test = df_class_test.reset_index(drop=True)

y_class_train = df_class_train['ASTHMA'].values
y_class_val = df_class_val['ASTHMA'].values
y_class_test = df_class_test['ASTHMA'].values

del df_class_train['ASTHMA']
del df_class_val['ASTHMA']
del df_class_test['ASTHMA']

df_class_train_dicts = df_class_train.to_dict(orient='records')
df_class_val_dicts = df_class_val.to_dict(orient='records')
df_class_test_dicts = df_class_test.to_dict(orient='records')

dv = DictVectorizer(sparse=True)
X_class_train = dv.fit_transform(df_class_train_dicts)
X_class_val = dv.transform(df_class_val_dicts)
X_class_test = dv.transform(df_class_test_dicts)

features = list(dv.get_feature_names_out())
dtrain = xgb.DMatrix(X_class_train, label=y_class_train, feature_names=features)
dval = xgb.DMatrix(X_class_val, label=y_class_val, feature_names=features)

## 3.4. Hyperparameter tuning - XGBoost - Classification Model
# Tuning the following parameters:
# - `eta`
# - `max_depth`
# - `min_child_weight`

eta_class = 0.05
max_depth_class = 6
min_child_weight_class = 30


## 3.5. Training the model tunned - XGBoost - Classification Model
xgb_params = {
    'eta': eta_class, 
    'max_depth': max_depth_class,
    'min_child_weight': min_child_weight_class,
    
    'objective': 'binary:logistic',
    'eval_metric': 'auc',

    'nthread': 8,
    'seed': 1,
    'verbosity': 1,
}

final_class_model = xgb.train(xgb_params, dtrain, num_boost_round=200)

## 3.7. Save the Model - XGBoost - Classification Model

class_output_file = f'./models/model_xgb_class_eda={eta_class}_max_depth={max_depth_class}_min_child_weight={min_child_weight_class}.bin'
with open(class_output_file, 'wb') as f_out:
    pickle.dump((dv, final_class_model), f_out)


# 4. Regression Model Process
# ## 4.1. Split the data - Regression Model
# - Split the data in train/val/test sets with 60%/20%/20% distribution.

# Add predicted probabilities to the original dataframe
df_for_prediction = df[classification_features].copy()
df_for_prediction_dicts = df_for_prediction.to_dict(orient='records')

X_full_dataset = dv.transform(df_for_prediction_dicts)
dfull = xgb.DMatrix(X_full_dataset, feature_names=features)
df['ASTHMA_PRED_PROBA'] = final_class_model.predict(dfull)

regression_features = [
   'BIRTH_YEAR',
   'GENDER_FACTOR',
   'RACE_FACTOR',
   'ETHNICITY_FACTOR',
   'PAYER_FACTOR',
   'ATOPIC_MARCH_COHORT',
   'AGE_START_YEARS',
   'NUM_ALLERGIES',
   'SHELLFISH_ALG_START',
   'FISH_ALG_START',
   'MILK_ALG_START',
   'SOY_ALG_START',
   'EGG_ALG_START',
   'WHEAT_ALG_START',
   'PEANUT_ALG_START',
   'SESAME_ALG_START',
   'TREENUT_ALG_START',
   'WALNUT_ALG_START',
   'PECAN_ALG_START',
   'PISTACH_ALG_START',
   'ALMOND_ALG_START',
   'BRAZIL_ALG_START',
   'HAZELNUT_ALG_START',
   'CASHEW_ALG_START',
   'ATOPIC_DERM_START',
   'ALLERGIC_RHINITIS_START',

   # Add predicted probability as feature
   'ASTHMA_PRED_PROBA'
]
target_regression = ['ASTHMA_START']
df_regression_filtered = df[df['ASTHMA_START'].notna()]

df_regression = df_regression_filtered[regression_features + target_regression]

df_reg_full_train, df_reg_test = train_test_split(df_regression, test_size=0.2, random_state=1)
df_reg_train, df_reg_val = train_test_split(df_reg_full_train, test_size=0.25, random_state=1)

df_reg_train = df_reg_train.reset_index(drop=True)
df_reg_val = df_reg_val.reset_index(drop=True)
df_reg_test = df_reg_test.reset_index(drop=True)

y_reg_train = df_reg_train['ASTHMA_START'].values
y_reg_val = df_reg_val['ASTHMA_START'].values
y_reg_test = df_reg_test['ASTHMA_START'].values

del df_reg_train['ASTHMA_START']
del df_reg_val['ASTHMA_START']
del df_reg_test['ASTHMA_START']

df_reg_train_dicts = df_reg_train.to_dict(orient='records')
df_reg_val_dicts = df_reg_val.to_dict(orient='records')
df_reg_test_dicts = df_reg_test.to_dict(orient='records')

dv = DictVectorizer(sparse=True)
X_reg_train = dv.fit_transform(df_reg_train_dicts)
X_reg_val = dv.transform(df_reg_val_dicts)
X_reg_test = dv.transform(df_reg_test_dicts)

features_reg = list(dv.get_feature_names_out())
dtrai_reg = xgb.DMatrix(X_reg_train, label=y_reg_train, feature_names=features_reg)
dval_reg = xgb.DMatrix(X_reg_val, label=y_reg_val, feature_names=features_reg)

# ## 3.4. Hyperparameter tuning - XGBoost - Classification Model
# 
# Tuning the following parameters:
# - `eta`
# - `max_depth`
# - `min_child_weight`

eta_reg = 0.05
max_depth_reg = 6
min_child_weight_reg = 30

# ## 4.5. Training the model tunned - XGBoost - Regression Model

# In[435]:

xgb_params_reg = {
    'eta': eta_reg,
    'max_depth': max_depth_reg,
    'min_child_weight': min_child_weight_reg,

    'objective': 'reg:squarederror',
    'eval_metric': 'rmse',

    'nthread': 8,
    'seed': 1,
    'verbosity': 1
}

final_reg_model = xgb.train(xgb_params_reg, dtrai_reg, num_boost_round=200)

## 4.7. Save the Model - XGBoost - Regression Model
reg_output_file = f'./models/model_xgb_reg_eda={eta_reg}_max_depth={max_depth_reg}_min_child_weight={min_child_weight_reg}.bin'
with open(reg_output_file, 'wb') as f_out:
    pickle.dump((dv, final_reg_model), f_out)
