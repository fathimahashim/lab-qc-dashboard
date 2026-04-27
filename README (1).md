# 🧪 Laboratory QC Dashboard

> Statistical Process Control for Wine Quality Measurements

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python) ![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-red?logo=streamlit) ![Plotly](https://img.shields.io/badge/Plotly-5.24.1-informational) ![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Project Overview

A **Laboratory Quality Control Dashboard** built to monitor physicochemical measurements (pH, acidity, alcohol) using **Statistical Process Control (SPC)** methods from manufacturing standards.

**Dataset:** UCI Wine Quality — 1,599 samples × 11 parameters — used as a laboratory measurement proxy.

---

## 📸 Screenshots

### Dashboard Interface
![Dashboard Interface](screenshots/dashboard.png)

### X-bar Control Chart & Process Capability
![X-bar Chart and Process Capability](screenshots/xbar_chart.png)

---

## 🚀 Features

| Feature | Technical Implementation | Relevance |
|---|---|---|
| X-bar & CUSUM Charts | Plotly + subgroup analysis | Deviation detection |
| Western Electric Rules | 8 statistical tests | Outlier identification |
| Cp / Cpk Indices | SciPy + specification limits | Process capability |
| Shapiro-Wilk Test | Pingouin normality test | Statistical validation |
| Automated PDF Reports | FPDF2 + embedded charts | Compliance reporting |
| Interactive Filters | Streamlit sidebar | User assistance |

---

## 📊 Sample Results (pH Analysis)

| Metric | Value | Status |
|---|---|---|
| Mean | 3.31 | ✅ Within limits |
| Cp | 1.00 | ✅ Capable |
| Cpk | 2.23 | ✅ Well-centred |
| Normality p-value | 1.000 | ✅ Normal |
| 3σ Violations | 4 / 319 | ⚠️ Alert |

---

## 🛠️ Tech Stack

```
🌐 Frontend  : Streamlit 1.38.0
📊 Data      : Pandas 2.2.2, NumPy 2.0.1
📈 Viz       : Plotly 5.24.1, Matplotlib 3.9.2
🔬 Stats     : SciPy 1.14.1, Pingouin 0.5.3
📄 Reports   : FPDF2 2.8.1
🐍 Runtime   : Python 3.11 | ~2.3k LOC
```

---

## 📁 Repository Structure

```
lab-qc-dashboard/
├── app.py                      # Streamlit main app
├── requirements.txt            # Python dependencies
├── packages.txt                # System packages
├── README.md                   # You're reading it
├── screenshots/
│   ├── dashboard.png           # Dashboard interface screenshot
│   └── xbar_chart.png          # X-bar chart screenshot
├── data/
│   └── winequality-red.csv     # 1,599 lab measurements
├── analysis/
│   ├── __init__.py
│   ├── control_charts.py       # X-bar, CUSUM, Western Electric rules
│   └── statistics.py           # Cp/Cpk, normality testing
└── reports/
    ├── __init__.py
    └── report_generator.py     # Automated PDF generation
```

---

## ⚡ Quick Start

```bash
# Clone & install
git clone https://github.com/fathimahashim/lab-qc-dashboard.git
cd lab-qc-dashboard
pip install -r requirements.txt

# Run dashboard
streamlit run app.py
```

Opens at: `http://localhost:8501`

---

## 📈 Business Impact

- ✅ **Deviation detection** — flags measurement outliers automatically (4/1,599 identified)
- ✅ **Compliance reporting** — Cp ≥ 1.0 achieved; PDF reports auto-generated
- ✅ **Automation** — replaces manual weekly/monthly QC reporting
- ✅ **Accessibility** — interactive interface suited for lab technicians
- ✅ **Scalability** — applicable to any continuous measurement data

---

## 🔗 Resources

- 📂 **Source:** [github.com/fathimahashim/lab-qc-dashboard](https://github.com/fathimahashim/lab-qc-dashboard)
- 📊 **Dataset:** [UCI Wine Quality](https://archive.ics.uci.edu/ml/datasets/wine+quality)
- 📖 **SPC Theory:** [Process Capability](https://en.wikipedia.org/wiki/Process_capability)

---

<div align="center">

👩‍🔬 Built by **Fathima Hashim**  
Kollam, Kerala · April 2026  
*For Quality Control Analyst Applications*

</div>
