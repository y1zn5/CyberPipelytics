# 📊 CyberPipelytics: Data Pipeline Visualization Dashboard

An interactive Streamlit dashboard designed to visualize, analyze, and diagnose each stage of the data preprocessing pipeline for cybersecurity datasets (e.g., Honeypot logs like Dionaea and AWS). 

This tool enables data scientists and cybersecurity analysts to track dataset transformations from raw ingestion to the final analysis-ready stage.

---

## 🌟 Key Features

* **Pipeline Stage Comparisons:** Seamlessly compare metrics between `raw`, `cleaned`, `encoded`, and `final` stages.
* **Missing Data & Imputation Tracking:** Visual distribution of missing values across pipeline stages via dynamic bar charts.
* **Outlier Diagnostics:** Detect and analyze numerical outliers using the Interquartile Range (IQR) method with Histograms and Boxplots.
* **Data Preview & Feature Drift:** Track added, removed, or retained columns along with statistical breakdowns (`describe()`).
* **One-Click Export:** Download CSV files directly from any stage of the pipeline.

---

## 📁 Supported Datasets & Stages

The dashboard monitors data transformation across 4 main stages:
1. **Raw (`raw`):** Original unprocessed dataset.
2. **Cleaned (`cleaned`):** Dataset with handled missing values and removed duplicates.
3. **Encoded (`encoded`):** Categorical variables converted into numerical representations.
4. **Final (`final`):** Fully feature-engineered and formatted dataset.

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Installation
Clone the repository and install the required dependencies:

```bash
git clone [https://github.com/y1zn5/DataScience.git](https://github.com/y1zn5/DataScience.git)
cd DataScience
pip install streamlit pandas numpy matplotlib seaborn
3. Running the App
Place your CSV files (dionaeaClean2.csv, aws_cleaned.csv, etc.) in the root directory and run:

Bash
streamlit run app.py
🛠️ Tech Stack
Frontend / Framework: Streamlit

Data Processing: Pandas, NumPy

Data Visualization: Matplotlib, Seaborn

📝 License
This project is open-source and available under the MIT License.
