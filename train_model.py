import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

def train_predictive_system():
    df = pd.read_csv('dataset/cleaned_properties.csv')
    
    # Convert text data to numbers (One-Hot Encoding)
    df = pd.get_dummies(df, columns=['Location_Grade'], drop_first=True)
    
    # Separate input features (X) from the target output value we want to predict (y)
    X = df.drop('Price_USD', axis=1)
    y = df['Price_USD']
    
    # Split into 80% training data and 20% testing data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model 1: Linear Regression (Our Baseline)
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_preds = lr_model.predict(X_test)
    
    # Model 2: Random Forest (Our Advanced Machine Learning Model)
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)
    
    # Calculate performance metrics
    rf_r2 = r2_score(y_test, rf_preds)
    rf_mae = mean_absolute_error(y_test, rf_preds)
    
    print("=== MODEL PERFORMANCE ANALYSIS ===")
    print(f"Baseline Linear Regression R² Score: {r2_score(y_test, lr_preds):.4f}")
    print(f"Advanced Random Forest R² Score: {rf_r2:.4f}")
    print(f"Random Forest Mean Absolute Error: ${rf_mae:,.2f}")
    
    # Extract Feature Importances to explain model logic
    importances = rf_model.feature_importances_
    features = X.columns
    
    print("\n=== INSIGHT GENERATION (FEATURE IMPORTANCE) ===")
    for feat, imp in zip(features, importances):
        print(f"Feature: {feat:<25} | Importance Weight: {imp*100:.2f}%")
        
    # Save the absolute best model and the features structure list for deployment
    joblib.dump(rf_model, 'property_model.pkl')
    joblib.dump(list(features), 'model_features.pkl')
    print("\n✓ Top performing model exported safely as 'property_model.pkl'")

if __name__ == '__main__':
    train_predictive_system()