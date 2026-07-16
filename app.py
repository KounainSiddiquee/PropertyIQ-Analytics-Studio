from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load our pre-trained machine learning model pipeline components
try:
    model = joblib.load('property_model.pkl')
    model_features = joblib.load('model_features.pkl')
except FileNotFoundError:
    model = None
    model_features = None

@app.route('/predict', methods=['POST'])
def predict_price():
    if not model:
        return jsonify({"error": "Machine learning model file not trained yet. Run train_model.py first."}), 500
        
    data = request.get_json()
    
    # Extract structured parameters sent by a client application
    try:
        sqft = float(data['Square_Feet'])
        bedrooms = float(data['Bedrooms'])
        age = float(data['Age_Years'])
        location = data.get('Location_Grade', 'B')
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid input formatting features provided."}), 400

    # Build an empty base dataframe row matching exactly what our trained model expects
    input_row = pd.DataFrame(0.0, index=[0], columns=model_features)
    
    # Assign baseline values
    input_row.at[0, 'Square_Feet'] = sqft
    input_row.at[0, 'Bedrooms'] = bedrooms
    input_row.at[0, 'Age_Years'] = age
    
    # Account for encoded location columns dummy flags dynamically
    loc_col = f"Location_Grade_{location}"
    if loc_col in input_row.columns:
        input_row.at[0, loc_col] = 1.0

    # Run data through machine learning model
    predicted_val = model.predict(input_row)[0]
    
    return jsonify({
        "status": "Success",
        "predicted_property_price_usd": round(predicted_val, 2),
        "input_summary": {
            "Square_Feet": sqft,
            "Bedrooms": bedrooms,
            "Age_Years": age,
            "Location_Grade": location
        }
    })

if __name__ == '__main__':
    print("Starting ReadyNest micro-service API on port 5000...")
    app.run(port=5000, debug=True)