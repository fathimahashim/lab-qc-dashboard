import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
sys.path.insert(0, '.')

try:
    from analysis.control_charts import plot_xbar_chart
    from analysis.statistics import run_full_analysis, build_deviation_log
    from reports.report_generator import generate_pdf_report
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

st.set_page_config(page_title="Lab QC Dashboard", layout="wide")

st.title("🧪 Laboratory QC Dashboard")
st.markdown("**Statistical Process Control for Wine Quality Measurements**")

# Cloud-safe data loading
@st.cache_data
def load_data():
    csv_files = ['data/winequality-red.csv', 'data/lab_measurements.csv']
    for csv in csv_files:
        if os.path.exists(csv):
            try:
                if 'red.csv' in csv:
                    df = pd.read_csv(csv, sep=';')
                else:
                    df = pd.read_csv(csv)
                df.to_csv('data/lab_measurements.csv', index=False)
                return df
            except Exception as e:
                st.error(f"Data load error: {e}")
                return None
    return None

df = load_data()
if df is None:
    st.error("❌ No data found. Needs data/winequality-red.csv")
    st.stop()

st.success(f"✅ Loaded {len(df)} wine measurements")
st.dataframe(df[['pH', 'alcohol', 'quality']].head(5), use_container_width=True)

# Safe parameter list
PARAMS = ['pH', 'volatile acidity', 'citric acid', 'residual sugar', 
          'chlorides', 'alcohol']
PARAMS = [p for p in PARAMS if p in df.columns]

col1, col2 = st.columns(2)
with col1:
    selected_param = st.selectbox("Select Parameter", PARAMS, index=0)
with col2:
    subgroup_size = st.slider("Subgroup Size", 3, 10, 5)

if st.button("📊 Run SPC Analysis", type="primary"):
    with st.spinner("Analyzing process capability..."):
        try:
            # Analysis with error handling
            analysis = run_full_analysis(df, [selected_param])
            fig, limits, vbp = plot_xbar_chart(df, selected_param, subgroup_size)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # SAFE metrics (check keys exist)
            st.subheader("📈 Process Capability")
            col1, col2, col3 = st.columns(3)
            
            cp_val = analysis.get('Cp', {}).get(selected_param, 0.0)
            cpk_val = analysis.get('Cpk', {}).get(selected_param, 0.0)
            norm_p = analysis.get('norm_p', {}).get(selected_param, 1.0)
            
            with col1: st.metric("Cp", f"{cp_val:.2f}")
            with col2: st.metric("Cpk", f"{cpk_val:.2f}")
            with col3: st.metric("Norm p-val", f"{norm_p:.3f}")
            
            # PDF Report (safe)
            try:
                dev = build_deviation_log(df, {selected_param: vbp})
                os.makedirs('reports', exist_ok=True)
                generate_pdf_report(df, analysis, {selected_param: vbp}, dev, 
                                   ('2024-01-01','2024-12-31'), 'reports/QC_Report.pdf')
                with open('reports/QC_Report.pdf', 'rb') as f:
                    st.download_button("📥 Download PDF Report", f.read(), 
                                     "QC_Report.pdf", "application/pdf")
            except Exception as pdf_e:
                st.warning(f"PDF generation skipped: {pdf_e}")
                
        except Exception as e:
            st.error(f"Analysis error: {e}")
            st.info("Metrics shown as defaults. Check analysis modules.")

# Data info sidebar
with st.sidebar:
    st.info(f"**Dataset**: {len(df)} wine samples")
    st.info("**Parameters**: pH, acidity, alcohol")
    st.markdown("[GitHub](https://github.com/fathimahashim/lab-qc-dashboard)")