import pickle
import xgboost as xgb
from flask import Flask, request, jsonify

# Load the classification model
class_model_file = 'models/model_xgb_class_eda=0.05_max_depth=6_min_child_weight=30.bin'
with open(class_model_file, 'rb') as f_in:
    (dv_class, model_class) = pickle.load(f_in)

# Load the regression model
reg_model_file = 'models/model_xgb_reg_eda=0.05_max_depth=6_min_child_weight=30.bin'
with open(reg_model_file, 'rb') as f_in:
    (dv_reg, model_reg) = pickle.load(f_in)

app = Flask('asthma_prediction')

# Define required features for classification model
REQUIRED_CLASSIFICATION_FEATURES = [
    'BIRTH_YEAR',
    'GENDER_FACTOR',
    'RACE_FACTOR',
    'ETHNICITY_FACTOR',
    'PAYER_FACTOR',
    'ATOPIC_MARCH_COHORT',
    'AGE_START_YEARS',
    'NUM_ALLERGIES'
]

# Define required features for regression model
REQUIRED_REGRESSION_FEATURES = [
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
    'ALLERGIC_RHINITIS_START'
]

@app.route('/predict', methods=['POST'])
def predict():
    patient = request.get_json()
    
    # Check if all required classification features are present
    missing_class_features = [feature for feature in REQUIRED_CLASSIFICATION_FEATURES 
                              if feature not in patient]
    
    if missing_class_features:
        # Cannot make classification prediction without all required features
        result = {
            'error': 'Cannot predict asthma risk. Missing required patient information.',
            'missing_features': missing_class_features
        }
        return jsonify(result), 400
    
    # Transform the input data using classification DictVectorizer
    X_class = dv_class.transform([patient])
    
    # Get feature names for DMatrix
    features_class = list(dv_class.get_feature_names_out())
    
    # Create DMatrix for XGBoost prediction
    dmatrix_class = xgb.DMatrix(X_class, feature_names=features_class)
    
    # Get prediction probability
    y_pred = model_class.predict(dmatrix_class)[0]
    
    # Determine if patient has asthma (threshold: 0.5)
    asthma = y_pred >= 0.5
    
    result = {
        'asthma_probability': float(y_pred),
        'asthma': bool(asthma)
    }
    
    # If asthma probability > 0.5, check if we can predict asthma start age
    if y_pred > 0.5:
        # Check if all required regression features are present
        missing_reg_features = [feature for feature in REQUIRED_REGRESSION_FEATURES 
                               if feature not in patient]
        
        if missing_reg_features:
            # Warning: cannot make reliable prediction without all features
            result['warning'] = (
                'Patient is at risk for asthma, but asthma start age cannot be predicted reliably. '
                'Missing allergy and condition history data required for age prediction.'
            )
            result['missing_features'] = missing_reg_features
        else:
            # All features present, proceed with regression prediction
            # Add the predicted probability to patient data for regression
            patient_reg = patient.copy()
            patient_reg['ASTHMA_PRED_PROBA'] = float(y_pred)
            
            # Transform the input data using regression DictVectorizer
            X_reg = dv_reg.transform([patient_reg])
            
            # Get feature names for regression DMatrix
            features_reg = list(dv_reg.get_feature_names_out())
            
            # Create DMatrix for XGBoost regression prediction
            dmatrix_reg = xgb.DMatrix(X_reg, feature_names=features_reg)
            
            # Get predicted asthma start age
            asthma_start_pred = model_reg.predict(dmatrix_reg)[0]
            
            result['asthma_start_age_predicted'] = float(asthma_start_pred)
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)