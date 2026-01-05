import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')
sns.set_style('whitegrid')

st.set_page_config(
    page_title="Data Pipeline Visualizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATASET_FILES = {
    'Dionaea': {
        'raw': 'dionaeaClean2.csv',
        'cleaned': 'dionaea_cleaned.csv',
        'encoded': 'dionaea_encoded.csv',
        'final': 'dionaea_final.csv'
    },
    'AWS': {
        'raw': 'AWS_Honeypot_marx-geo.csv',
        'cleaned': 'aws_cleaned.csv',
        'encoded': 'aws_encoded.csv',
        'final': 'aws_final.csv'
    }
}

STAGE_ORDER = ['raw', 'cleaned', 'encoded', 'final']

@st.cache_data
def load_csv(filepath):
    try:
        if not Path(filepath).exists():
            return None
        return pd.read_csv(filepath, low_memory=False)
    except Exception as e:
        st.error(f"Error loading {filepath}: {str(e)}")
        return None

def calculate_metrics(df):
    if df is None:
        return None

    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()
    missing_pct = (missing_cells / total_cells * 100) if total_cells > 0 else 0

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    duplicates = df.duplicated().sum()

    return {
        'rows': df.shape[0],
        'columns': df.shape[1],
        'missing_cells': missing_cells,
        'missing_pct': missing_pct,
        'duplicates': duplicates,
        'numeric_cols': len(numeric_cols),
        'categorical_cols': len(categorical_cols),
        'numeric_col_names': numeric_cols,
        'categorical_col_names': categorical_cols
    }

def get_outliers_count(series):
    if series.dtype not in [np.float64, np.int64, np.float32, np.int32]:
        return 0

    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = ((series < lower_bound) | (series > upper_bound)).sum()
    return outliers

def plot_distribution(df_before, df_after, column, stage_before, stage_after):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Distribution Analysis: {column}', fontsize=16, fontweight='bold')

    if column in df_before.columns:
        axes[0, 0].hist(df_before[column].dropna(), bins=50, color='#3498db', edgecolor='black', alpha=0.7)
        axes[0, 0].set_title(f'{stage_before.title()} - Histogram', fontsize=12, fontweight='bold')
        axes[0, 0].set_xlabel('Value')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].grid(True, alpha=0.3)

        axes[0, 1].boxplot(df_before[column].dropna(), vert=True)
        axes[0, 1].set_title(f'{stage_before.title()} - Boxplot', fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel('Value')
        axes[0, 1].grid(True, alpha=0.3)
    else:
        axes[0, 0].text(0.5, 0.5, f'Column not in {stage_before}', ha='center', va='center')
        axes[0, 0].axis('off')
        axes[0, 1].text(0.5, 0.5, f'Column not in {stage_before}', ha='center', va='center')
        axes[0, 1].axis('off')

    if column in df_after.columns:
        axes[1, 0].hist(df_after[column].dropna(), bins=50, color='#2ecc71', edgecolor='black', alpha=0.7)
        axes[1, 0].set_title(f'{stage_after.title()} - Histogram', fontsize=12, fontweight='bold')
        axes[1, 0].set_xlabel('Value')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].grid(True, alpha=0.3)

        axes[1, 1].boxplot(df_after[column].dropna(), vert=True)
        axes[1, 1].set_title(f'{stage_after.title()} - Boxplot', fontsize=12, fontweight='bold')
        axes[1, 1].set_ylabel('Value')
        axes[1, 1].grid(True, alpha=0.3)
    else:
        axes[1, 0].text(0.5, 0.5, f'Column not in {stage_after}', ha='center', va='center')
        axes[1, 0].axis('off')
        axes[1, 1].text(0.5, 0.5, f'Column not in {stage_after}', ha='center', va='center')
        axes[1, 1].axis('off')

    plt.tight_layout()
    return fig

st.title("📊 Data Pipeline Visualization Dashboard")
st.markdown("### Explore preprocessing pipeline results at each stage")

st.sidebar.header("Configuration")
dataset = st.sidebar.selectbox("Select Dataset", list(DATASET_FILES.keys()))

stage_options = [
    "raw → cleaned",
    "cleaned → encoded",
    "encoded → final",
    "raw → final"
]
stage_comparison = st.sidebar.selectbox("Select Stage Comparison", stage_options)

stage_before, stage_after = stage_comparison.split(" → ")

file_before = DATASET_FILES[dataset][stage_before]
file_after = DATASET_FILES[dataset][stage_after]

df_before = load_csv(file_before)
df_after = load_csv(file_after)

if df_before is None:
    st.error(f"⚠️ Could not load {file_before}. Please ensure the file exists in the project directory.")
if df_after is None:
    st.error(f"⚠️ Could not load {file_after}. Please ensure the file exists in the project directory.")

if df_before is not None or df_after is not None:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview",
        "🔍 Missing/Imputation",
        "📊 Outliers",
        "👁️ Preview",
        "💾 Export"
    ])

    with tab1:
        st.header("Pipeline Stage Overview")
        st.markdown(f"**Comparing:** `{file_before}` → `{file_after}`")

        metrics_before = calculate_metrics(df_before)
        metrics_after = calculate_metrics(df_after)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"📥 {stage_before.title()} Stage")
            if metrics_before:
                st.metric("Rows", f"{metrics_before['rows']:,}")
                st.metric("Columns", metrics_before['columns'])
                st.metric("Missing Cells", f"{metrics_before['missing_cells']:,}")
                st.metric("Missing %", f"{metrics_before['missing_pct']:.2f}%")
                st.metric("Duplicates", f"{metrics_before['duplicates']:,}")
                st.metric("Numeric Columns", metrics_before['numeric_cols'])
                st.metric("Categorical Columns", metrics_before['categorical_cols'])
            else:
                st.warning("Data not available")

        with col2:
            st.subheader(f"📤 {stage_after.title()} Stage")
            if metrics_after:
                st.metric("Rows", f"{metrics_after['rows']:,}")
                st.metric("Columns", metrics_after['columns'])
                st.metric("Missing Cells", f"{metrics_after['missing_cells']:,}")
                st.metric("Missing %", f"{metrics_after['missing_pct']:.2f}%")
                st.metric("Duplicates", f"{metrics_after['duplicates']:,}")
                st.metric("Numeric Columns", metrics_after['numeric_cols'])
                st.metric("Categorical Columns", metrics_after['categorical_cols'])
            else:
                st.warning("Data not available")

        if metrics_before and metrics_after:
            st.divider()
            st.subheader("📋 Column Changes")

            cols_before = set(df_before.columns)
            cols_after = set(df_after.columns)

            added = cols_after - cols_before
            removed = cols_before - cols_after
            unchanged = cols_before & cols_after

            change_col1, change_col2, change_col3 = st.columns(3)

            with change_col1:
                st.metric("Columns Added", len(added))
                if added:
                    with st.expander("View added columns"):
                        for col in sorted(added):
                            st.text(f"+ {col}")

            with change_col2:
                st.metric("Columns Removed", len(removed))
                if removed:
                    with st.expander("View removed columns"):
                        for col in sorted(removed):
                            st.text(f"- {col}")

            with change_col3:
                st.metric("Columns Unchanged", len(unchanged))

    with tab2:
        st.header("Missing Data Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"{stage_before.title()} Stage")
            if df_before is not None:
                missing_before = df_before.isnull().sum()
                missing_pct_before = (missing_before / len(df_before) * 100).sort_values(ascending=False)
                missing_pct_before = missing_pct_before[missing_pct_before > 0]

                if len(missing_pct_before) > 0:
                    top_missing = missing_pct_before.head(30)

                    fig, ax = plt.subplots(figsize=(10, max(6, len(top_missing) * 0.3)))
                    top_missing.plot(kind='barh', ax=ax, color='#e74c3c')
                    ax.set_xlabel('Missing %', fontsize=12)
                    ax.set_ylabel('Column', fontsize=12)
                    ax.set_title(f'Top {len(top_missing)} Columns by Missing %', fontsize=14, fontweight='bold')
                    ax.grid(True, alpha=0.3, axis='x')
                    plt.tight_layout()
                    st.pyplot(fig)

                    st.dataframe(
                        pd.DataFrame({
                            'Column': top_missing.index,
                            'Missing %': top_missing.values.round(2)
                        }).reset_index(drop=True),
                        use_container_width=True,
                        height=400
                    )
                else:
                    st.success("No missing values detected!")
            else:
                st.warning("Data not available")

        with col2:
            st.subheader(f"{stage_after.title()} Stage")
            if df_after is not None:
                missing_after = df_after.isnull().sum()
                missing_pct_after = (missing_after / len(df_after) * 100).sort_values(ascending=False)
                missing_pct_after = missing_pct_after[missing_pct_after > 0]

                if len(missing_pct_after) > 0:
                    top_missing = missing_pct_after.head(30)

                    fig, ax = plt.subplots(figsize=(10, max(6, len(top_missing) * 0.3)))
                    top_missing.plot(kind='barh', ax=ax, color='#27ae60')
                    ax.set_xlabel('Missing %', fontsize=12)
                    ax.set_ylabel('Column', fontsize=12)
                    ax.set_title(f'Top {len(top_missing)} Columns by Missing %', fontsize=14, fontweight='bold')
                    ax.grid(True, alpha=0.3, axis='x')
                    plt.tight_layout()
                    st.pyplot(fig)

                    st.dataframe(
                        pd.DataFrame({
                            'Column': top_missing.index,
                            'Missing %': top_missing.values.round(2)
                        }).reset_index(drop=True),
                        use_container_width=True,
                        height=400
                    )
                else:
                    st.success("No missing values detected!")
            else:
                st.warning("Data not available")

    with tab3:
        st.header("Outliers Diagnostics")
        st.markdown("**Method:** IQR (Interquartile Range) - values outside [Q1 - 1.5×IQR, Q3 + 1.5×IQR]")

        if df_before is not None and df_after is not None:
            numeric_cols_before = df_before.select_dtypes(include=[np.number]).columns.tolist()
            numeric_cols_after = df_after.select_dtypes(include=[np.number]).columns.tolist()
            all_numeric = sorted(set(numeric_cols_before + numeric_cols_after))

            if all_numeric:
                st.subheader("Outlier Count Summary")

                outlier_data = []
                for col in all_numeric:
                    count_before = get_outliers_count(df_before[col]) if col in df_before.columns else 0
                    count_after = get_outliers_count(df_after[col]) if col in df_after.columns else 0
                    outlier_data.append({
                        'Column': col,
                        f'{stage_before.title()} Outliers': count_before,
                        f'{stage_after.title()} Outliers': count_after,
                        'Change': count_after - count_before
                    })

                outlier_df = pd.DataFrame(outlier_data)
                outlier_df = outlier_df[
                    (outlier_df[f'{stage_before.title()} Outliers'] > 0) |
                    (outlier_df[f'{stage_after.title()} Outliers'] > 0)
                ].sort_values(f'{stage_before.title()} Outliers', ascending=False)

                if len(outlier_df) > 0:
                    st.dataframe(outlier_df, use_container_width=True, height=400)
                else:
                    st.info("No outliers detected in any numeric columns")

                st.divider()
                st.subheader("Visual Comparison")

                selected_col = st.selectbox(
                    "Select numeric column for detailed view",
                    all_numeric,
                    key='outlier_col_select'
                )

                if selected_col:
                    fig = plot_distribution(df_before, df_after, selected_col, stage_before, stage_after)
                    st.pyplot(fig)

                    col1, col2 = st.columns(2)
                    with col1:
                        if selected_col in df_before.columns:
                            st.write(f"**{stage_before.title()} Statistics:**")
                            st.dataframe(
                                df_before[selected_col].describe().to_frame().T,
                                use_container_width=True
                            )

                    with col2:
                        if selected_col in df_after.columns:
                            st.write(f"**{stage_after.title()} Statistics:**")
                            st.dataframe(
                                df_after[selected_col].describe().to_frame().T,
                                use_container_width=True
                            )
            else:
                st.info("No numeric columns available for outlier analysis")
        else:
            st.warning("Both datasets required for outlier analysis")

    with tab4:
        st.header("Data Preview")

        preview_stage = st.radio(
            "Select stage to preview",
            [stage_before.title(), stage_after.title()],
            horizontal=True
        )

        preview_df = df_before if preview_stage == stage_before.title() else df_after

        if preview_df is not None:
            st.subheader(f"First 200 rows - {preview_stage} Stage")
            st.dataframe(preview_df.head(200), use_container_width=True, height=400)

            st.divider()
            st.subheader("Column Statistics")

            selected_preview_col = st.selectbox(
                "Select column for detailed statistics",
                preview_df.columns.tolist(),
                key='preview_col_select'
            )

            if selected_preview_col:
                col_stats = preview_df[selected_preview_col].describe(include='all').to_frame()
                col_stats.columns = ['Value']
                st.dataframe(col_stats, use_container_width=True)

                if preview_df[selected_preview_col].dtype in [np.float64, np.int64, np.float32, np.int32]:
                    st.write("**Distribution Histogram:**")
                    fig, ax = plt.subplots(figsize=(10, 4))
                    ax.hist(preview_df[selected_preview_col].dropna(), bins=50, color='#3498db', edgecolor='black', alpha=0.7)
                    ax.set_xlabel('Value', fontsize=11)
                    ax.set_ylabel('Frequency', fontsize=11)
                    ax.set_title(f'{selected_preview_col} Distribution', fontsize=13, fontweight='bold')
                    ax.grid(True, alpha=0.3)
                    plt.tight_layout()
                    st.pyplot(fig)
        else:
            st.warning("Data not available for preview")

    with tab5:
        st.header("Export Data")
        st.markdown("Download CSV files from any pipeline stage")

        export_col1, export_col2 = st.columns(2)

        with export_col1:
            st.subheader(f"{stage_before.title()} Stage")
            if df_before is not None:
                csv_before = df_before.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"Download {file_before}",
                    data=csv_before,
                    file_name=file_before,
                    mime='text/csv',
                    use_container_width=True
                )
                st.info(f"Rows: {len(df_before):,} | Columns: {len(df_before.columns)}")
            else:
                st.warning("Data not available")

        with export_col2:
            st.subheader(f"{stage_after.title()} Stage")
            if df_after is not None:
                csv_after = df_after.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"Download {file_after}",
                    data=csv_after,
                    file_name=file_after,
                    mime='text/csv',
                    use_container_width=True
                )
                st.info(f"Rows: {len(df_after):,} | Columns: {len(df_after.columns)}")
            else:
                st.warning("Data not available")

        st.divider()
        st.subheader("All Available Files")

        for ds_name, files in DATASET_FILES.items():
            with st.expander(f"{ds_name} Dataset"):
                for stage_name, filename in files.items():
                    df_temp = load_csv(filename)
                    if df_temp is not None:
                        csv_data = df_temp.to_csv(index=False).encode('utf-8')
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.text(f"{stage_name.title()}: {filename}")
                        with col_b:
                            st.download_button(
                                label="Download",
                                data=csv_data,
                                file_name=filename,
                                mime='text/csv',
                                key=f"download_{ds_name}_{stage_name}",
                                use_container_width=True
                            )
                    else:
                        st.text(f"{stage_name.title()}: {filename} (not found)")
else:
    st.error("Unable to load any data. Please check that CSV files exist in the project directory.")

st.sidebar.divider()
st.sidebar.markdown("### About")
st.sidebar.info(
    "This dashboard visualizes data preprocessing pipeline results. "
    "Select a dataset and stage comparison to explore metrics, missing data, "
    "outliers, and preview the data at each stage."
)
