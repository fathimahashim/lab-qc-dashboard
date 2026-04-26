import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data.generate_data import generate_lab_data
from analysis.control_charts import plot_xbar_chart
from analysis.statistics import run_full_analysis, build_deviation_log
from reports.report_generator import generate_pdf_report
import os

st.set_page_config(page_title="Lab QC Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = generate_lab_data()
    return df

df = load_data()
st.title("🧪 Laboratory QC Dashboard")
st.markdown("**Statistical Process Control for Wine Quality Measurements**")

# Sidebar controls
st.sidebar.header("Analysis Controls")
params = ['pH', 'volatile_acidity', 'citric_acid', 'residual_sugar', 
          'chlorides', 'free_SO2', 'total_SO2', 'alcohol']
selected_param = st.sidebar.selectbox("Select Parameter", params)
subgroup_size = st.sidebar.slider("Subgroup Size", 3, 10, 5)

date_col1, date_col2 = st.sidebar.columns(2)
date_start = date_col1.date_input("Start Date", df['timestamp'].min().date())
date_end = date_col2.date_input("End Date", df['timestamp'].max().date())
filtered_df = df[(df['timestamp'] >= pd.Timestamp(date_start)) & 
                 (df['timestamp'] <= pd.Timestamp(date_end))]

# Main analysis
col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Control Chart")
    fig, limits, deviations = plot_xbar_chart(filtered_df, selected_param, subgroup_size)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Stats")
    analysis = run_full_analysis(filtered_df, [selected_param])
    stats_df = pd.DataFrame([analysis[selected_param]])
    st.dataframe(stats_df)

with col2:
    st.subheader("Deviation Log")
    vbp = {selected_param: limits}
    dev_log = build_deviation_log(filtered_df, vbp)
    if not dev_log.empty:
        st.dataframe(dev_log)
    else:
        st.success("✅ No violations detected")

# Generate Report Button
if st.button("📄 Generate PDF Report"):
    vbp = {p: plot_xbar_chart(filtered_df, p, 5)[1] for p in params[:3]}
    dev = build_deviation_log(filtered_df, vbp)
    os.makedirs('reports', exist_ok=True)
    generate_pdf_report(filtered_df, analysis, vbp, dev, 
                       (date_start, date_end), 'reports/QC_Report.pdf')
    st.success("✅ Report generated: reports/QC_Report.pdf")
    with open('reports/QC_Report.pdf', 'rb') as f:
        st.download_button("💾 Download Report", f.read(), 
                          "QC_Report_Wine.pdf", "application/pdf")

# Raw data preview
with st.expander("📋 View Raw Data"):
    st.dataframe(df.head(20))