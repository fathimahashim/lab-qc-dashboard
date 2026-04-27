import streamlit as st
import pandas as pd
import os
import sys
sys.path.insert(0, '.')

from analysis.control_charts import plot_xbar_chart
from analysis.statistics import run_full_analysis, build_deviation_log
from reports.report_generator import generate_pdf_report

st.set_page_config(page_title="Lab QC Dashboard", layout="wide")

st.title("🧪 Laboratory QC Dashboard")
st.markdown("**Statistical Process Control for measurement data quality**")

# Cloud-safe data loading
@st.cache_data
def load_data():
    csv_files = ['data/winequality-red.csv', 'data/lab_measurements.csv']
    for csv in csv_files:
        if os.path.exists(csv):
            try:
                if csv.endswith('red.csv'):
                    df = pd.read_csv(csv, sep=';')
                else:
                    df = pd.read_csv(csv)
                # Save standardized
                df.to_csv('data/lab_measurements.csv', index=False)
                return df
            except:
                pass
    st.error("❌ No data file found. Add data/winequality-red.csv")
    st.stop()

df = load_data()
st.success(f"✅ Loaded {len(df)} measurements")

# Parameters (wine columns)
PARAMS = ['pH', 'volatile acidity', 'citric acid', 'residual sugar', 
          'chlorides', 'alcohol']
PARAMS = [p for p in PARAMS if p in df.columns]

col1, col2 = st.columns(2)
with col1:
    selected_param = st.selectbox("Parameter", PARAMS)
with col2:
    subgroup_size = st.slider("Subgroup size", 3, 10, 5)

if st.button("📊 Generate Analysis"):
    with st.spinner("Running SPC analysis..."):
        analysis = run_full_analysis(df, [selected_param])
        fig, limits, vbp = plot_xbar_chart(df, selected_param, subgroup_size)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📈 Process Capability")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Cp", f"{analysis['Cp'][selected_param]:.2f}")
        with col2: st.metric("Cpk", f"{analysis['Cpk'][selected_param]:.2f}")
        with col3: st.metric("Normality p", f"{analysis['norm_p'][selected_param]:.3f}")
        
        # PDF Report
        dev = build_deviation_log(df, {selected_param: vbp})
        generate_pdf_report(df, analysis, {selected_param: vbp}, dev, 
                           ('2024-01-01','2024-12-31'), 'reports/QC_Report.pdf')
        with open('reports/QC_Report.pdf', 'rb') as f:
            st.download_button("📥 Download PDF Report", f.read(), 
                             "QC_Report.pdf", "application/pdf")