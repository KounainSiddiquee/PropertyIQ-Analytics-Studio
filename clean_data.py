import pandas as pd
import numpy as np

# 1. CREATE A MESSY DATASET FOR DEMO PURPOSES
def generate_messy_data():
    np.random.seed(42)
    n_samples = 200
    
    data = {
        'Square_Feet': np.random.randint(800, 3500, size=n_samples).astype(float),
        'Bedrooms': np.random.randint(1, 5, size=n_samples).astype(float),
        'Age_Years': np.random.randint(0, 30, size=n_samples).astype(float),
        'Location_Grade': np.random.choice(['A', 'B', 'C', None], size=n_samples, p=[0.3, 0.4, 0.2, 0.1]),
        'Price_USD': np.random.randint(150000, 700000, size=n_samples).astype(float)
    }
    
    df = pd.DataFrame(data)
    
    # Inject dirty data elements intentionally
    df.iloc[10:20, 0] = np.nan       # Missing Square Feet
    df.iloc[35:40, 1] = np.nan       # Missing Bedrooms
    df.iloc[50, 4] = 9500000.0       # Insane Outlier Price
    
    df.to_csv('dataset/raw_properties.csv', index=False)
    print("✓ Raw messy dataset created at 'dataset/raw_properties.csv'")

# 2. THE CLEANING PIPELINE FUNCTIONS
def clean_dataset():
    # Load the data
    df = pd.read_csv('dataset/raw_properties.csv')
    print(f"Original dataset shape: {df.shape}")
    
    # Handle Missing Values (Imputation)
    # Fill missing Square Feet with the median value
    sqft_median = df['Square_Feet'].median()
    df['Square_Feet'] = df['Square_Feet'].fillna(sqft_median)
    
    # Fill missing Bedrooms with the most frequent value (mode)
    bedroom_mode = df['Bedrooms'].mode()[0]
    df['Bedrooms'] = df['Bedrooms'].fillna(bedroom_mode)
    
    # Fill missing categorical values with a label placeholder
    df['Location_Grade'] = df['Location_Grade'].fillna('Unknown')
    
    # Handle Outliers using the Interquartile Range (IQR) rule on Price
    Q1 = df['Price_USD'].quantile(0.25)
    Q3 = df['Price_USD'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)
    
    # Filter dataset rows to keep values strictly within normal statistical boundaries
    df = df[(df['Price_USD'] >= lower_bound) & (df['Price_USD'] <= upper_bound)]
    print(f"Cleaned dataset shape (after outlier removal): {df.shape}")
    
    # Save clean dataset
    df.to_csv('dataset/cleaned_properties.csv', index=False)
    print("✓ Cleaned dataset saved safely at 'dataset/cleaned_properties.csv'")

if __name__ == '__main__':
    generate_messy_data()
    clean_dataset()