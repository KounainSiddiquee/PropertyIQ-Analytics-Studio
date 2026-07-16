import os
import subprocess
import sys

def execute_stage(script_name, description):
    print(f"\n==================================================")
    print(f"🚀 STAGE: {description} ({script_name})")
    print(f"==================================================")
    
    try:
        # Executes the sub-script cleanly and streams terminal prints live
        result = subprocess.run([sys.executable, script_name], check=True, text=True)
        if result.returncode == 0:
            print(f"✓ {script_name} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR encountered in {script_name}!")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    print("🎯 STARTING AN END-TO-END PREDICTIVE PIPELINE...")
    
    # 1. Clean data layer
    execute_stage("clean_data.py", "Data Cleansing, Imputation & IQR Outlier Removal")
    
    # 2. Build visuals
    execute_stage("visualizer.py", "Programmatic Data Visualization & Exploratory Plots")
    
    # 3. Train ML Models
    execute_stage("train_model.py", "Model Benchmarking, Valuation & Feature Weight Extraction")
    
    # 4. Generate automated final documents
    execute_stage("document_generator.py", "Automated Business Analytics PDF Performance Reporting")
    
    print("\n==================================================")
    print("🎉 ALL PREDICTIVE PIPELINE STAGES COMPLETED FLAWLESSLY!")
    print("==================================================")
    print("ReadyNest Deliverables Package generated:")
    print(" -> dataset/cleaned_properties.csv")
    print(" -> distribution_plot.png & scatter_plot.png")
    print(" -> property_model.pkl & model_features.pkl")
    print(" -> ReadyNest_System_Performance_Report.pdf")
    print("\n👉 To run your live prediction API service web endpoint, use: python app.py")