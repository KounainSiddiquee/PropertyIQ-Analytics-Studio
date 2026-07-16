import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_plots():
    # Set professional presentation styles
    sns.set_theme(style="whitegrid")
    
    # 1. Look for the cleaned dataset file dynamically
    cleaned_file = 'dataset/cleaned_properties.csv'
    if not os.path.exists(cleaned_file):
        # Fallback if your script saved it under a different common name
        possible_paths = ['dataset/cleaned_data.csv', 'dataset/boutique_intelligence.csv']
        cleaned_file = next((p for p in possible_paths if os.path.exists(p)), None)
        
    if not cleaned_file:
        raise FileNotFoundError("Could not locate your cleaned dataset inside the dataset/ directory.")

    df = pd.read_csv(cleaned_file)
    print(f"Reading dataset for plotting. Total rows available: {len(df)}")
    
    # 2. Automatically discover target transaction/premium numeric columns 
    possible_targets = ['Price_USD', 'TotalAmount', 'premium', 'Price', 'Total_Amount', 'Amount']
    target_col = next((col for col in possible_targets if col in df.columns), None)
    
    if not target_col:
        # Fallback to the last numerical column if no matching string names are found
        target_col = df.select_dtypes(include=['number']).columns[-1]
    
    # 3. Automatically discover a baseline structural feature to plot against
    possible_features = ['Square_Feet', 'Quantity', 'age_in_days', 'Age_Years', 'Income', 'Quantity_Ordered']
    feature_col = next((col for col in possible_features if col in df.columns), None)
    
    if not feature_col or feature_col == target_col:
        feature_col = df.select_dtypes(include=['number']).columns[0]

    print(f"Generating charts using target: '{target_col}' and feature: '{feature_col}'")

    # Chart 1: Revenue / Value Distribution Profile
    plt.figure(figsize=(7, 4))
    # Sample a maximum of 20,000 rows for faster generation speed over large data structures
    plot_df = df.sample(min(20000, len(df)), random_state=42)
    
    sns.histplot(plot_df[target_col], kde=True, color='#2ca02c', bins=30)
    plt.title(f'Distribution Analysis of {target_col.replace("_", " ")}')
    plt.xlabel(target_col.replace("_", " "))
    plt.ylabel('Count Density')
    plt.tight_layout()
    plt.savefig('distribution_plot.png', dpi=150)
    plt.close()
    
    # Chart 2: Matrix Scatter Relationship Trend
    plt.figure(figsize=(7, 4))
    sns.scatterplot(x=feature_col, y=target_col, data=plot_df, alpha=0.4, color='#1f77b4')
    plt.title(f'{feature_col.replace("_", " ")} vs {target_col.replace("_", " ")} Regression Profile')
    plt.xlabel(feature_col.replace("_", " "))
    plt.ylabel(target_col.replace("_", " "))
    plt.tight_layout()
    plt.savefig('scatter_plot.png', dpi=150)
    plt.close()
    
    print("✓ Professional visualizations successfully rendered and saved to the root folder!")

if __name__ == '__main__':
    generate_plots()