# ReadyNest: Production-Grade Predictive Analytics System

An end-to-end Machine Learning and Automated Business Intelligence pipeline that ingests high-volume real-world transaction data (100,000+ rows), performs statistical data cleaning, handles extreme outliers, benchmarks predictive models, and exposes a micro-service API.

## 📊 System Architecture & Pipeline Flow
1. **ETL Data Preprocessing (`clean_data.py`)**: Implements Median Imputation for missing numbers and utilizes the Interquartile Range (IQR) method to eliminate volatile pricing/value skewness.
2. **Data Visualization (`visualizer.py`)**: Programmatically maps distribution curves and regression metrics, downsampling large arrays cleanly to optimize memory utilization.
3. **Machine Learning Core (`train_model.py`)**: One-hot encodes categorical text and trains both a baseline Linear Regression and an advanced Random Forest Regressor. Generates feature importance weight maps to guarantee total transparency into model logic.
4. **Micro-API Service (`app.py`)**: A live predictive POST endpoint `/predict` built in Flask that serves predictions dynamically from the serialized (`.pkl`) model weights.
5. **Automated Document Compiler (`document_generator.py`)**: Programmatically binds analysis plots and metrics into a publication-ready PDF evaluation document.

## 🚀 Getting Started & Execution

Run the complete pipeline end-to-end with a single automation command:
```bash
python run_all.py