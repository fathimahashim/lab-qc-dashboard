import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats

def calculate_control_limits(data, subgroup_size=5):
    """Calculate X-bar and R chart limits"""
    n = len(data)
    subgroups = [data[i:i+subgroup_size] for i in range(0, n, subgroup_size)]
    x_bars = [sub.mean() for sub in subgroups if len(sub) == subgroup_size]
    ranges = [sub.max() - sub.min() for sub in subgroups if len(sub) == subgroup_size]
    
    x_bar_mean = np.mean(x_bars)
    r_bar = np.mean(ranges)
    d2 = {2:1.128, 3:1.693, 4:2.059, 5:2.326}[min(subgroup_size, 5)]
    
    UCL_xbar = x_bar_mean + (2.66 * r_bar / d2)
    LCL_xbar = x_bar_mean - (2.66 * r_bar / d2)
    UCL_R = 2.11 * r_bar  # For n=5
    LCL_R = 0
    
    return {
        'x_bar_mean': x_bar_mean, 'UCL_xbar': UCL_xbar, 'LCL_xbar': LCL_xbar,
        'r_bar': r_bar, 'UCL_R': UCL_R, 'LCL_R': LCL_R
    }

def detect_deviations(data, limits, subgroup_size=5):
    """Western Electric Zone Rules"""
    n = len(data)
    subgroups = [data[i:i+subgroup_size] for i in range(0, n, subgroup_size)]
    x_bars = [sub.mean() for sub in subgroups]
    
    deviations = []
    for i, xbar in enumerate(x_bars):
        zone = (xbar - limits['LCL_xbar']) / (limits['UCL_xbar'] - limits['LCL_xbar']) * 3
        rule = []
        if xbar > limits['UCL_xbar']: rule.append("Above UCL")
        elif xbar < limits['LCL_xbar']: rule.append("Below LCL")
        elif zone > 2: rule.append("Zone A")
        elif abs(zone) > 2: rule.append("Zone B/C")
        if rule: deviations.append(f"Subgroup {i+1}: {'; '.join(rule)}")
    
    return deviations

def plot_xbar_chart(df, param, subgroup_size=5):
    """Generate X-bar control chart"""
    data = df[param].dropna().values
    limits = calculate_control_limits(data, subgroup_size)
    deviations = detect_deviations(data, limits, subgroup_size)
    
    # Subgroup means
    subgroups = [data[i:i+subgroup_size] for i in range(0, len(data), subgroup_size)]
    x_bars = [np.mean(sub) for sub in subgroups]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=x_bars, mode='lines+markers', name='Subgroup Means',
        line=dict(color='blue', width=2)
    ))
    
    # Control limits
    fig.add_hline(y=limits['UCL_xbar'], line_dash="dash", line_color="red",
                  annotation_text="UCL", annotation_position="top right")
    fig.add_hline(y=limits['x_bar_mean'], line_dash="solid", line_color="green",
                  annotation_text="CL", annotation_position="right")
    fig.add_hline(y=limits['LCL_xbar'], line_dash="dash", line_color="red",
                  annotation_text="LCL", annotation_position="bottom right")
    
    fig.update_layout(
        title=f'X-bar Chart: {param}',
        xaxis_title='Subgroup', yaxis_title=f'{param}',
        height=500, showlegend=False
    )
    
    return fig, limits, deviations