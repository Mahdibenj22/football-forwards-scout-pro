# pages/exploration_3d.py

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
    # Enhanced CSS for 3D Exploration page
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary: #00c6ff;
        --secondary: #0072ff;
        --accent: #00e676;
        --purple: #8b5cf6;
        --orange: #f59e0b;
        --pink: #ec4899;
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
        padding: 2rem 0;
        background: linear-gradient(135deg, rgba(139,92,246,0.1), rgba(236,72,153,0.1));
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(139,92,246,0.2);
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
        background: radial-gradient(circle at 30% 20%, rgba(139,92,246,0.1), transparent 50%),
                    radial-gradient(circle at 70% 80%, rgba(236,72,153,0.1), transparent 50%);
        pointer-events: none;
    }
    
    .page-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--purple), var(--pink), var(--primary));
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        margin: 0;
        position: relative;
        z-index: 2;
    }
    
    .page-subtitle {
        font-size: 1.2rem;
        color: var(--text-muted);
        margin-top: 0.5rem;
        position: relative;
        z-index: 2;
    }
    
    .insight-panel {
        background: linear-gradient(135deg, rgba(0,230,118,0.1), rgba(0,198,255,0.1));
        border: 1px solid rgba(0,230,118,0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 2rem 0;
    }
    
    .insight-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--accent);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .data-info {
        background: rgba(0,198,255,0.1);
        border: 1px solid rgba(0,198,255,0.2);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* Hide empty containers and unnecessary elements */
    .element-container:empty {
        display: none !important;
    }
    
    .stContainer > div:empty {
        display: none !important;
    }
    
    .stForm {
        border: none !important;
        background: transparent !important;
    }
    
    /* Hide any empty vertical blocks */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="element-container"]:empty {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Page Header
    st.markdown('''
    <div class="page-header">
        <h1 class="page-title">🎯 3D Exploration</h1>
        <p class="page-subtitle">Interactive Multi-Dimensional Player Analysis</p>
    </div>
    ''', unsafe_allow_html=True)
    
    df = load_data()
    if df.empty:
        return

    # Find available features
    possible_features = ["PACE", "SHOOTING", "DRIBBLING", "PASSING", "PHYSICAL", "AERIAL", "MENTAL", "OVR", "Age"]
    features = [f for f in possible_features if f in df.columns]
    
    if len(features) < 3:
        st.error(f"Need at least 3 numeric features; found: {features}")
        return

    # Enhanced Control Panel
    st.markdown("### 🎨 Visualization Mode")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mode_scatter = st.button("🌟 Performance Cluster", key="mode1", use_container_width=True)
    with col2:
        mode_league = st.button("🏆 League Analysis", key="mode2", use_container_width=True)
    with col3:
        mode_value = st.button("💰 Market Value", key="mode3", use_container_width=True)
    
    # Feature Selection
    st.markdown("### 📊 Select 3 Features for Analysis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        x_feature = st.selectbox("X-Axis", features, index=0, key="x_feat")
    with col2:
        y_feature = st.selectbox("Y-Axis", features, index=1 if len(features) > 1 else 0, key="y_feat")
    with col3:
        z_feature = st.selectbox("Z-Axis", features, index=2 if len(features) > 2 else 0, key="z_feat")
    
    # Validate feature selection
    if len(set([x_feature, y_feature, z_feature])) != 3:
        st.warning("⚠️ Please select 3 different features for meaningful 3D visualization.")
        return

    # Generate 3D Visualization based on mode
    if mode_scatter or (not mode_league and not mode_value):
        # Performance Cluster Mode (default)
        st.markdown("### 🌟 Performance Cluster Analysis")
        
        # Create enhanced scatter plot
        fig = go.Figure()
        
        # Fix size values - transform to positive range
        if "OVR" in df.columns:
            # Transform OVR values to positive range for size
            ovr_values = df["OVR"].values
            # Scale to 5-25 range for marker size
            min_ovr, max_ovr = ovr_values.min(), ovr_values.max()
            size_values = 5 + ((ovr_values - min_ovr) / (max_ovr - min_ovr)) * 20
        else:
            size_values = [10] * len(df)  # Default size
        
        # Color by performance level
        if "OVR" in df.columns:
            color_values = df["OVR"]
            colorscale = "viridis"
        else:
            color_values = df[x_feature]
            colorscale = "plasma"
        
        fig.add_trace(go.Scatter3d(
            x=df[x_feature],
            y=df[y_feature],
            z=df[z_feature],
            mode='markers',
            marker=dict(
                size=size_values,
                color=color_values,
                colorscale=colorscale,
                opacity=0.8,
                colorbar=dict(title="Performance Level"),
                line=dict(width=1, color='rgba(255,255,255,0.5)')
            ),
            text=df["Name"],
            hovertemplate=
            "<b>%{text}</b><br>" +
            f"{x_feature}: %{{x:.2f}}<br>" +
            f"{y_feature}: %{{y:.2f}}<br>" +
            f"{z_feature}: %{{z:.2f}}<br>" +
            "<extra></extra>",
            name="Players"
        ))
        
    elif mode_league:
        # League Analysis Mode - FIXED
        st.markdown("### 🏆 League Comparison Analysis")
        
        if "League" not in df.columns:
            st.error("League column not found in data")
            return
        
        fig = go.Figure()
        
        # Get unique leagues and assign colors
        leagues = df["League"].unique()[:8]  # Limit to 8 leagues for clarity
        colors = ['#00c6ff', '#ff4757', '#2ed573', '#ffa502', '#8b5cf6', '#ec4899', '#f59e0b', '#06d6a0']
        
        for i, league in enumerate(leagues):
            league_data = df[df["League"] == league]
            
            # FIXED: Handle size values properly - use Age or OVR as fallback
            if "market_value" in df.columns and not league_data["market_value"].isna().all():
                # Use market_value if available, fill NaN with mean
                mv_values = league_data["market_value"].fillna(league_data["market_value"].mean())
                mv_values = np.maximum(mv_values.values, 0.1)  # Ensure positive values
                size_values = 5 + (mv_values / df["market_value"].max()) * 15
            elif "Age" in df.columns:
                # Use Age as backup for sizing
                age_values = league_data["Age"].fillna(25).values  # Fill NaN with 25
                size_values = 5 + ((age_values - 15) / 25) * 15  # Scale age 15-40 to size 5-20
            else:
                # Default uniform size
                size_values = [10] * len(league_data)
            
            fig.add_trace(go.Scatter3d(
                x=league_data[x_feature],
                y=league_data[y_feature],
                z=league_data[z_feature],
                mode='markers',
                marker=dict(
                    size=size_values,
                    color=colors[i % len(colors)],
                    opacity=0.7,
                    line=dict(width=1, color='rgba(255,255,255,0.3)')
                ),
                text=league_data["Name"],
                name=f"{league} ({len(league_data)} players)",
                hovertemplate=
                "<b>%{text}</b><br>" +
                f"League: {league}<br>" +
                f"{x_feature}: %{{x:.2f}}<br>" +
                f"{y_feature}: %{{y:.2f}}<br>" +
                f"{z_feature}: %{{z:.2f}}<br>" +
                "<extra></extra>"
            ))
        
    elif mode_value:
        # Market Value Analysis Mode - FIXED
        st.markdown("### 💰 Market Value Analysis")
        
        if "market_value" not in df.columns:
            st.error("Market value column not found in data")
            return
        
        # FIXED: Filter out players without market value
        df_with_value = df[df["market_value"].notna() & (df["market_value"] > 0)].copy()
        
        if df_with_value.empty:
            st.error("No players with valid market value found")
            return
        
        # Show data info
        st.markdown(f'''
        <div class="data-info">
            <strong>📊 Data Info:</strong> Analyzing {len(df_with_value)} players with valid market values 
            (filtered from {len(df)} total players)
        </div>
        ''', unsafe_allow_html=True)
        
        fig = go.Figure()
        
        # Create value tiers - FIXED
        try:
            df_with_value['value_tier'] = pd.cut(
                df_with_value['market_value'], 
                bins=5, 
                labels=['Budget', 'Affordable', 'Mid-Range', 'Premium', 'Elite'],
                duplicates='drop'  # Handle duplicate edges
            )
        except ValueError:
            # If cut fails, create manual tiers
            mv_values = df_with_value['market_value']
            q20, q40, q60, q80 = mv_values.quantile([0.2, 0.4, 0.6, 0.8])
            
            def assign_tier(value):
                if value <= q20:
                    return 'Budget'
                elif value <= q40:
                    return 'Affordable'
                elif value <= q60:
                    return 'Mid-Range'
                elif value <= q80:
                    return 'Premium'
                else:
                    return 'Elite'
            
            df_with_value['value_tier'] = df_with_value['market_value'].apply(assign_tier)
        
        tier_colors = {
            'Budget': '#6c757d',
            'Affordable': '#28a745', 
            'Mid-Range': '#ffc107',
            'Premium': '#fd7e14',
            'Elite': '#dc3545'
        }
        
        for tier in df_with_value['value_tier'].unique():
            tier_data = df_with_value[df_with_value['value_tier'] == tier]
            
            # FIXED: Proper size calculation
            mv_values = tier_data["market_value"].values
            size_values = 8 + (mv_values / df_with_value["market_value"].max()) * 20
            
            fig.add_trace(go.Scatter3d(
                x=tier_data[x_feature],
                y=tier_data[y_feature],
                z=tier_data[z_feature],
                mode='markers',
                marker=dict(
                    size=size_values,
                    color=tier_colors.get(tier, '#6c757d'),
                    opacity=0.8,
                    line=dict(width=1, color='rgba(255,255,255,0.4)')
                ),
                text=tier_data["Name"],
                name=f"{tier} (€{tier_data['market_value'].mean():.1f}M avg)",
                hovertemplate=
                "<b>%{text}</b><br>" +
                "Value: €%{customdata:.1f}M<br>" +
                f"{x_feature}: %{{x:.2f}}<br>" +
                f"{y_feature}: %{{y:.2f}}<br>" +
                f"{z_feature}: %{{z:.2f}}<br>" +
                "<extra></extra>",
                customdata=tier_data["market_value"]
            ))

    # Enhanced 3D layout
    fig.update_layout(
        scene=dict(
            xaxis_title=f"📊 {x_feature}",
            yaxis_title=f"📈 {y_feature}",
            zaxis_title=f"🎯 {z_feature}",
            bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                backgroundcolor="rgba(0,0,0,0)",
                gridcolor="rgba(255,255,255,0.2)",
                showbackground=True,
                zerolinecolor="rgba(255,255,255,0.3)",
                tickfont=dict(color="white")
            ),
            yaxis=dict(
                backgroundcolor="rgba(0,0,0,0)",
                gridcolor="rgba(255,255,255,0.2)",
                showbackground=True,
                zerolinecolor="rgba(255,255,255,0.3)",
                tickfont=dict(color="white")
            ),
            zaxis=dict(
                backgroundcolor="rgba(0,0,0,0)",
                gridcolor="rgba(255,255,255,0.2)",
                showbackground=True,
                zerolinecolor="rgba(255,255,255,0.3)",
                tickfont=dict(color="white")
            ),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        template="plotly_dark",
        height=700,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            font=dict(color="white"),
            bgcolor="rgba(0,0,0,0.5)"
        ),
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Statistical Insights Panel
    st.markdown("### 🔍 Statistical Insights")
    
    # Use appropriate dataset based on mode
    analysis_df = df_with_value if mode_value else df
    
    # Generate insights based on selected features
    col1, col2, col3 = st.columns(3)
    
    selected_features = [x_feature, y_feature, z_feature]
    
    for i, (feature, col) in enumerate(zip(selected_features, [col1, col2, col3])):
        feature_data = analysis_df[feature].dropna()
        
        with col:
            st.markdown(f"**📊 {feature} Analysis**")
            st.markdown(f"- **Mean**: {feature_data.mean():.3f}")
            st.markdown(f"- **Std Dev**: {feature_data.std():.2f}")
            st.markdown(f"- **Range**: {feature_data.min():.2f} to {feature_data.max():.2f}")
            
            # Find top performer
            if not feature_data.empty:
                top_player_idx = feature_data.idxmax()
                top_player = analysis_df.loc[top_player_idx, "Name"]
                top_value = feature_data.max()
                st.markdown(f"- **Top**: {top_player} ({top_value:.2f})")

    # Correlation Analysis
    st.markdown("### 🔗 Feature Correlation Analysis")
    
    corr_data = analysis_df[selected_features].corr()
    
    col1, col2, col3 = st.columns(3)
    
    correlations = [
        (f"{x_feature} ↔ {y_feature}", corr_data.loc[x_feature, y_feature]),
        (f"{x_feature} ↔ {z_feature}", corr_data.loc[x_feature, z_feature]),
        (f"{y_feature} ↔ {z_feature}", corr_data.loc[y_feature, z_feature])
    ]
    
    for (pair, corr_val), col in zip(correlations, [col1, col2, col3]):
        with col:
            # Determine correlation strength
            if abs(corr_val) > 0.7:
                strength = "Strong"
                color = "#2ed573" if corr_val > 0 else "#ff4757"
            elif abs(corr_val) > 0.3:
                strength = "Moderate"
                color = "#ffa502"
            else:
                strength = "Weak"
                color = "#6c757d"
            
            st.markdown(f"""
            <div style="background: {color}20; border: 1px solid {color}40; border-radius: 8px; padding: 1rem; text-align: center;">
                <div style="font-weight: 600; margin-bottom: 0.5rem;">{pair}</div>
                <div style="font-size: 1.2rem; color: {color};">{corr_val:.3f}</div>
                <div style="font-size: 0.8rem; color: var(--text-muted);">{strength}</div>
            </div>
            """, unsafe_allow_html=True)

    # Back button
    st.markdown("---")
    if st.button("🔙 Back to Dashboard", key="back_btn", use_container_width=True):
        st.session_state.current_page = "dashboard"

if __name__ == "__main__":
    main()
