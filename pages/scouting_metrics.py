# pages/scouting_metrics.py

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

@st.cache_data
def load_data():
    try:
        return pd.read_csv('forwards_clean_with_market_values_updated.csv')
    except FileNotFoundError:
        st.error("Data file not found.")
        return pd.DataFrame()

def main():
    # Enhanced CSS for Scouting Metrics page
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary: #00c6ff;
        --secondary: #0072ff;
        --accent: #00e676;
        --purple: #8b5cf6;
        --orange: #ff6b35;
        --gold: #ffd700;
        --pink: #ec4899;
        --red: #ff4757;
        --bg: #0a0a0b;
        --surface: #1a1a1b;
        --card: rgba(255,255,255,0.08);
        --text: #ffffff;
        --text-muted: #a0a0a0;
        --border: rgba(255,255,255,0.1);
        --shadow: 0 8px 32px rgba(0,0,0,0.4);
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--bg) 0%, #1a1a2e 50%, var(--bg) 100%) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .page-header {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,107,53,0.1));
        border-radius: 25px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,215,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .page-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 30% 20%, rgba(255,215,0,0.1), transparent 60%),
                    radial-gradient(circle at 70% 80%, rgba(255,107,53,0.1), transparent 60%);
        pointer-events: none;
        animation: metricsGlow 7s ease-in-out infinite alternate;
    }
    
    @keyframes metricsGlow {
        0% { transform: scale(1) rotate(0deg); opacity: 0.8; }
        100% { transform: scale(1.08) rotate(1deg); opacity: 1; }
    }
    
    .page-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--gold), var(--orange), var(--red));
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        margin: 0;
        position: relative;
        z-index: 2;
        animation: titleShine 5s ease-in-out infinite alternate;
    }
    
    .page-subtitle {
        font-size: 1.3rem;
        color: var(--text-muted);
        margin-top: 0.5rem;
        position: relative;
        z-index: 2;
        font-weight: 400;
    }
    
    @keyframes titleShine {
        0% { filter: drop-shadow(0 0 15px rgba(255,215,0,0.6)); }
        100% { filter: drop-shadow(0 0 30px rgba(255,107,53,0.8)); }
    }
    
    .metrics-panel {
        background: var(--card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
    }
    
    .metrics-panel::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, var(--gold), var(--orange));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metrics-panel:hover::before {
        opacity: 1;
    }
    
    .control-section {
        margin-bottom: 2rem;
    }
    
    .control-label {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .chart-container {
        background: var(--card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .chart-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(255,215,0,0.02), rgba(255,107,53,0.02));
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
    }
    
    .chart-container:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 32px rgba(255,215,0,0.15);
    }
    
    .chart-container:hover::before {
        opacity: 1;
    }
    
    .section-title {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 1.5rem;
        text-align: center;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, var(--gold), var(--orange));
        border-radius: 2px;
    }
    
    .metric-card {
        background: linear-gradient(145deg, var(--surface), rgba(255,255,255,0.05));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, var(--gold)08, var(--orange)08);
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(255,215,0,0.2);
        border-color: var(--gold);
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
        position: relative;
        z-index: 2;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--gold);
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        z-index: 2;
    }
    
    .insight-panel {
        background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,107,53,0.1));
        border: 1px solid rgba(255,215,0,0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .insight-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--gold);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .insight-item {
        background: var(--surface);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }
    
    .insight-item:hover {
        transform: translateY(-2px);
        border-color: var(--gold);
        box-shadow: 0 8px 16px rgba(255,215,0,0.1);
    }
    
    .insight-metric {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--gold);
        margin-bottom: 0.5rem;
    }
    
    .insight-desc {
        color: var(--text-muted);
        font-size: 0.95rem;
        line-height: 1.4;
    }
    
    .filter-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        margin: 1rem 0;
    }
    
    .filter-chip {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .filter-chip::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, var(--gold)10, var(--orange)10);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .filter-chip:hover {
        transform: translateY(-2px);
        border-color: var(--gold);
        box-shadow: 0 4px 8px rgba(255,215,0,0.2);
    }
    
    .filter-chip:hover::before {
        opacity: 1;
    }
    
    .filter-chip.active {
        background: linear-gradient(135deg, var(--gold), var(--orange));
        color: white;
        border-color: var(--gold);
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(255,107,53,0.1), rgba(255,71,87,0.1));
        border: 1px solid rgba(255,107,53,0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* Hide empty containers */
    .element-container:empty {
        display: none !important;
    }
    
    .stContainer > div:empty {
        display: none !important;
    }
    
    div[data-testid="stVerticalBlock"]:empty {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Page Header
    st.markdown('''
    <div class="page-header">
        <h1 class="page-title">📊 Scouting Metrics</h1>
        <p class="page-subtitle">Advanced performance visualization and statistical analysis</p>
    </div>
    ''', unsafe_allow_html=True)
    
    df = load_data()
    if df.empty:
        return

    # Enhanced Control Panel
    st.markdown("### ⚡ Visualization Controls")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Get available numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        # Remove market_value if it has too many NaN values
        if 'market_value' in numeric_cols and df['market_value'].isna().sum() > len(df) * 0.5:
            numeric_cols.remove('market_value')
        
        if len(numeric_cols) < 2:
            st.error("Not enough numeric columns available for visualization.")
            return
        
        x_metric = st.selectbox("📈 X-Axis Metric", numeric_cols, index=0)
        y_metric = st.selectbox("📊 Y-Axis Metric", numeric_cols, 
                               index=1 if len(numeric_cols) > 1 else 0)
        
        # Size metric with proper handling
        size_options = ["None"] + [col for col in numeric_cols if col not in [x_metric, y_metric]]
        size_metric = st.selectbox("📏 Bubble Size (Optional)", size_options)
        
        # Color coding options
        color_options = ["None", "League", "Position", "Age_Group"] + numeric_cols
        color_metric = st.selectbox("🎨 Color Coding", color_options)
    
    with col2:
        st.markdown("### 📊 Quick Metrics")
        
        total_players = len(df)
        avg_age = df['Age'].mean() if 'Age' in df.columns else 0
        
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-icon">👥</div>
            <div class="metric-value">{total_players}</div>
            <div class="metric-label">Total Players</div>
        </div>
        ''', unsafe_allow_html=True)
        
        if avg_age > 0:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-icon">📅</div>
                <div class="metric-value">{avg_age:.1f}</div>
                <div class="metric-label">Avg Age</div>
            </div>
            ''', unsafe_allow_html=True)

    # FIXED: Data preparation with proper size handling
    plot_df = df.copy()
    
    # Remove rows with NaN values in selected metrics
    plot_df = plot_df.dropna(subset=[x_metric, y_metric])
    
    if plot_df.empty:
        st.markdown('''
        <div class="warning-box">
            <strong>⚠️ No data available</strong><br>
            The selected metrics contain no valid data points.
        </div>
        ''', unsafe_allow_html=True)
        return
    
    # FIXED: Handle size metric properly
    size_values = None
    if size_metric != "None":
        # Remove rows with NaN in size metric
        plot_df = plot_df.dropna(subset=[size_metric])
        if not plot_df.empty:
            # Transform size values to positive range
            raw_size = plot_df[size_metric].values
            
            # Handle negative values by shifting to positive range
            min_val = raw_size.min()
            if min_val < 0:
                # Shift all values to be positive, then scale
                shifted_values = raw_size - min_val + 1  # +1 to avoid zero
                # Scale to reasonable bubble size range (5-30)
                max_shifted = shifted_values.max()
                size_values = 5 + (shifted_values / max_shifted) * 25
            else:
                # Values are already positive, just scale them
                max_val = raw_size.max()
                if max_val > 0:
                    size_values = 5 + (raw_size / max_val) * 25
                else:
                    size_values = [10] * len(raw_size)  # Default size
        else:
            size_metric = "None"  # Fallback if no valid data
    
    # Handle color coding
    color_values = None
    if color_metric != "None":
        if color_metric == "Age_Group":
            # Create age groups
            if 'Age' in plot_df.columns:
                plot_df['Age_Group'] = pd.cut(plot_df['Age'], 
                                            bins=[0, 23, 27, 32, 50], 
                                            labels=['Young (≤23)', 'Prime (24-27)', 'Experienced (28-32)', 'Veteran (33+)'])
                color_values = plot_df['Age_Group']
        else:
            color_values = plot_df[color_metric]

    # Enhanced Scatter Plot
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">📊 {x_metric} vs {y_metric} Analysis</div>', unsafe_allow_html=True)
    
    if plot_df.empty:
        st.warning("No data points available after filtering.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Create the scatter plot
    fig = go.Figure()
    
    if color_values is not None:
        # Colored scatter plot
        if color_metric in ['League', 'Position', 'Age_Group']:
            # Categorical coloring
            unique_categories = color_values.unique()
            colors = px.colors.qualitative.Set3[:len(unique_categories)]
            
            for i, category in enumerate(unique_categories):
                if pd.isna(category):
                    continue
                    
                mask = color_values == category
                category_df = plot_df[mask]
                
                fig.add_trace(go.Scattergl(
                    x=category_df[x_metric],
                    y=category_df[y_metric],
                    mode='markers',
                    name=str(category),
                    marker=dict(
                        size=size_values[mask] if size_values is not None else 10,
                        color=colors[i % len(colors)],
                        opacity=0.7,
                        line=dict(width=1, color='white')
                    ),
                    text=category_df['Name'] if 'Name' in category_df.columns else None,
                    hovertemplate=
                    "<b>%{text}</b><br>" +
                    f"{x_metric}: %{{x:.2f}}<br>" +
                    f"{y_metric}: %{{y:.2f}}<br>" +
                    f"{color_metric}: {category}<br>" +
                    "<extra></extra>"
                ))
        else:
            # Continuous coloring
            fig.add_trace(go.Scattergl(
                x=plot_df[x_metric],
                y=plot_df[y_metric],
                mode='markers',
                marker=dict(
                    size=size_values if size_values is not None else 10,
                    color=color_values,
                    colorscale='Viridis',
                    opacity=0.7,
                    colorbar=dict(title=color_metric),
                    line=dict(width=1, color='white')
                ),
                text=plot_df['Name'] if 'Name' in plot_df.columns else None,
                hovertemplate=
                "<b>%{text}</b><br>" +
                f"{x_metric}: %{{x:.2f}}<br>" +
                f"{y_metric}: %{{y:.2f}}<br>" +
                f"{color_metric}: %{{marker.color:.2f}}<br>" +
                "<extra></extra>",
                showlegend=False
            ))
    else:
        # Single color scatter plot
        fig.add_trace(go.Scattergl(
            x=plot_df[x_metric],
            y=plot_df[y_metric],
            mode='markers',
            marker=dict(
                size=size_values if size_values is not None else 10,
                color='#00c6ff',
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            text=plot_df['Name'] if 'Name' in plot_df.columns else None,
            hovertemplate=
            "<b>%{text}</b><br>" +
            f"{x_metric}: %{{x:.2f}}<br>" +
            f"{y_metric}: %{{y:.2f}}<br>" +
            "<extra></extra>",
            showlegend=False
        ))
    
    # Enhanced layout
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
        xaxis=dict(
            title=dict(text=x_metric, font=dict(size=16, color='white')),
            tickfont=dict(size=14, color='white'),
            gridcolor='rgba(255,255,255,0.2)',
            zerolinecolor='rgba(255,255,255,0.3)'
        ),
        yaxis=dict(
            title=dict(text=y_metric, font=dict(size=16, color='white')),
            tickfont=dict(size=14, color='white'),
            gridcolor='rgba(255,255,255,0.2)',
            zerolinecolor='rgba(255,255,255,0.3)'
        ),
        legend=dict(
            font=dict(size=12, color='white'),
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        ),
        margin=dict(t=20, b=20, l=20, r=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Enhanced Statistical Insights
    st.markdown('''
    <div class="insight-panel">
        <div class="insight-title">
            <span>🔍</span>
            <span>Statistical Insights</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Generate insights
    col1, col2, col3 = st.columns(3)
    
    # Correlation analysis
    if len(plot_df) > 1:
        correlation = plot_df[x_metric].corr(plot_df[y_metric])
        with col1:
            st.markdown(f'''
            <div class="insight-item">
                <div class="insight-metric">{correlation:.3f}</div>
                <div class="insight-desc">Correlation between {x_metric} and {y_metric}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Top performer
    if 'Name' in plot_df.columns:
        top_x = plot_df.loc[plot_df[x_metric].idxmax(), 'Name']
        top_y = plot_df.loc[plot_df[y_metric].idxmax(), 'Name']
        
        with col2:
            st.markdown(f'''
            <div class="insight-item">
                <div class="insight-metric">{top_x}</div>
                <div class="insight-desc">Highest {x_metric} ({plot_df[x_metric].max():.2f})</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="insight-item">
                <div class="insight-metric">{top_y}</div>
                <div class="insight-desc">Highest {y_metric} ({plot_df[y_metric].max():.2f})</div>
            </div>
            ''', unsafe_allow_html=True)

    # Distribution Analysis
    st.markdown("### 📈 Distribution Analysis")
    
    tab1, tab2 = st.tabs([f"📊 {x_metric} Distribution", f"📈 {y_metric} Distribution"])
    
    with tab1:
        fig_hist1 = px.histogram(
            plot_df, 
            x=x_metric, 
            nbins=20,
            title="",
            color_discrete_sequence=['#00c6ff']
        )
        fig_hist1.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        st.plotly_chart(fig_hist1, use_container_width=True)
    
    with tab2:
        fig_hist2 = px.histogram(
            plot_df, 
            x=y_metric, 
            nbins=20,
            title="",
            color_discrete_sequence=['#ff6b35']
        )
        fig_hist2.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        st.plotly_chart(fig_hist2, use_container_width=True)

    # Back button
    st.markdown("---")
    if st.button("🔙 Back to Dashboard", key="back_btn", use_container_width=True):
        st.session_state.current_page = "dashboard"

if __name__ == "__main__":
    main()
