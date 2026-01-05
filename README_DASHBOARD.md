# Data Pipeline Visualization Dashboard

A clean, professional Streamlit UI for visualizing data preprocessing pipeline results.

## Features

### 5 Interactive Tabs

1. **Overview** - Compare metrics between pipeline stages (rows, columns, missing %, duplicates, column changes)
2. **Missing/Imputation** - Visualize missing data patterns with bar charts and detailed tables
3. **Outliers** - IQR-based outlier detection with interactive histograms and boxplots
4. **Preview** - Browse first 200 rows and view detailed column statistics
5. **Export** - Download any stage CSV with one click

## Installation & Usage

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

## File Requirements

The app expects these CSV files in the same directory:

**Dionaea Dataset:**
- `dionaeaClean2.csv` (raw)
- `dionaea_cleaned.csv`
- `dionaea_encoded.csv`
- `dionaea_final.csv`

**AWS Dataset:**
- `AWS_Honeypot_marx-geo.csv` (raw)
- `aws_cleaned.csv`
- `aws_encoded.csv`
- `aws_final.csv`

## How to Use

1. **Select Dataset**: Choose between Dionaea or AWS in the sidebar
2. **Select Stage Comparison**: Choose which pipeline stages to compare (e.g., raw → cleaned)
3. **Explore Tabs**: Navigate through different analysis views
4. **Export Results**: Download any stage CSV from the Export tab

## Error Handling

If a CSV file is missing, the dashboard will display a warning instead of crashing. You can still explore available files.

## Notes

- This is a **read-only visualization tool** - it does not modify your pipeline scripts
- All metrics are calculated on-the-fly from the CSV files
- Charts and statistics update automatically when you change selections
- The app uses caching for fast performance on large datasets
