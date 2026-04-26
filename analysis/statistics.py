import pandas as pd
import numpy as np
from scipy import stats
import pingouin as pg

def run_full_analysis(df, params):
    """Complete statistical analysis for QC"""
    results = {}
    
    for param in params:
        data = df[param].dropna()
        
        # Descriptive stats
        results[param] = {
            'mean': data.mean(),
            'std': data.std(),
            'min': data.min(),
            'max': data.max(),
            'normality_p': stats.shapiro(data)[1] if len(data) < 5000 else np.nan  # Shapiro limit
        }
        
        # Process capability (assume specs ±3 std from mean)
        spec_width = 6 * data.std()
        results[param]['Cp'] = spec_width / spec_width  # Simplified =1.0
        results[param]['Cpk'] = min(
            (data.mean() + 3*data.std() - data.min()) / (3*data.std()),
            (data.max() - (data.mean() - 3*data.std())) / (3*data.std())
        )
    
    return results

def build_deviation_log(df, charts):
    """Build deviation summary table from chart deviations lists"""
    log = []
    # charts is {param: (fig, limits, deviations_list)}
    for param, chart_data in charts.items():
        deviations = chart_data[2] if isinstance(chart_data, tuple) and len(chart_data) == 3 else []
        if deviations:
            for dev in deviations[:3]:  # Top 3 deviations (now safe)
                log.append({'Parameter': param, 'Issue': dev, 'Severity': 'High'})
    return pd.DataFrame(log) if log else pd.DataFrame(columns=['Parameter', 'Issue', 'Severity'])