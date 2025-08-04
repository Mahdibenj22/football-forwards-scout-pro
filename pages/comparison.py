# pages/comparison.py

import streamlit as st
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
    # Enhanced CSS for comparison page
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary: #00c6ff;
        --secondary: #0072ff;
        --accent: #00e676;
        --danger: #ff4757;
        --warning: #ffa502;
        --success: #2ed573;
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
        background: linear-gradient(135deg, rgba(0,198,255,0.1), rgba(0,114,255,0.1));
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(0,198,255,0.2);
    }
    
    .page-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        margin: 0;
    }
    
    .page-subtitle {
        font-size: 1.1rem;
        color: var(--text-muted);
        margin-top: 0.5rem;
    }
    
    .vs-indicator {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        color: var(--accent);
        margin: 1.5rem 0;
        text-shadow: 0 0 10px rgba(0,230,118,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .vs-text {
        background: linear-gradient(135deg, var(--primary), var(--accent));
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        font-weight: 800;
    }
    
    .player-card {
        background: linear-gradient(145deg, var(--card), rgba(255,255,255,0.05));
        backdrop-filter: blur(20px);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    
    .player-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0,198,255,0.2);
    }
    
    .player-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 1.5rem;
    }
    
    .player-stats {
        display: flex;
        justify-content: space-around;
        margin-top: 1rem;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text);
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.25rem;
    }
    
    .radar-info {
        background: rgba(0,198,255,0.1);
        border: 1px solid rgba(0,198,255,0.2);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
    }
    
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
    </style>
    """, unsafe_allow_html=True)
    
    # Page Header
    st.markdown('''
    <div class="page-header">
        <h1 class="page-title">⚖️ Player Comparison</h1>
        <p class="page-subtitle">Compare two players side-by-side with advanced analytics</p>
    </div>
    ''', unsafe_allow_html=True)
    
    df = load_data()
    if df.empty:
        return

    # Validate columns
    if "Position" not in df.columns or "Name" not in df.columns:
        st.error("Required columns (Position, Name) missing.")
        return

    # Enhanced filter section
    st.markdown("### 🎯 Select Position")
    with st.form("comp_filters", clear_on_submit=False):
        pos = st.selectbox("Position", sorted(df["Position"].unique()), label_visibility="collapsed")
        submitted = st.form_submit_button("🔄 Apply Filter", use_container_width=True)
    
    if submitted:
        df = df[df["Position"] == pos]
    if df.empty:
        st.warning("No players found for the selected position.")
        return

    # Player selection with FIXED VS indicator
    st.markdown("### 👥 Select Players to Compare")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    names = [""] + list(df["Name"].sort_values())
    
    with col1:
        p1 = st.selectbox("First Player", names, key="p1", label_visibility="collapsed")
    
    with col2:
        st.markdown('''
        <div class="vs-indicator">
            <span style="font-size: 1.5rem;">⚡</span>
            <span class="vs-text">VS</span>
            <span style="font-size: 1.5rem;">⚡</span>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        p2 = st.selectbox("Second Player", names, key="p2", label_visibility="collapsed")

    if p1 and p2:
        if p1 == p2:
            st.warning("⚠️ Please choose two different players for comparison.")
        else:
            a = df[df["Name"] == p1].iloc[0]
            b = df[df["Name"] == p2].iloc[0]
            
            # Enhanced Player Cards
            st.markdown("### 🏆 Player Overview")
            col1, col2 = st.columns(2)
            
            with col1:
                ovr_a = a.get('OVR', 0)
                mv_a = a.get('market_value', 0)
                age_a = a.get('Age', 'N/A')
                st.markdown(f'''
                <div class="player-card">
                    <div class="player-name">{p1}</div>
                    <div class="player-stats">
                        <div class="stat-item">
                            <div class="stat-value">{ovr_a:.2f}</div>
                            <div class="stat-label">Overall</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">€{mv_a:.1f}M</div>
                            <div class="stat-label">Value</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">{age_a}</div>
                            <div class="stat-label">Age</div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                    
            with col2:
                ovr_b = b.get('OVR', 0)
                mv_b = b.get('market_value', 0)
                age_b = b.get('Age', 'N/A')
                st.markdown(f'''
                <div class="player-card">
                    <div class="player-name">{p2}</div>
                    <div class="player-stats">
                        <div class="stat-item">
                            <div class="stat-value">{ovr_b:.2f}</div>
                            <div class="stat-label">Overall</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">€{mv_b:.1f}M</div>
                            <div class="stat-label">Value</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">{age_b}</div>
                            <div class="stat-label">Age</div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

            # CORRECTLY SCALED Radar Chart
            base_skills = ["PACE","SHOOTING","PASSING","DRIBBLING","PHYSICAL","AERIAL","MENTAL"]
            skills = [s for s in base_skills if s in df.columns]

            if skills:
                st.markdown("### 📊 Skills Comparison Radar")
                
                # Get raw standardized values (already scaled by StandardScaler)
                vals_a_raw = [a[s] for s in skills]
                vals_b_raw = [b[s] for s in skills]
                
                # Transform standardized values to 0-100 scale for better visualization
                # StandardScaler typically produces values roughly in [-3, +3] range
                # We'll map [-3, +3] to [0, 100] for better radar chart visualization
                def scale_standardized_to_radar(val):
                    # Clamp to reasonable range and scale to 0-100
                    clamped = max(-3.5, min(3.5, val))  # Clamp to [-3.5, 3.5]
                    return ((clamped + 3.5) / 7.0) * 100  # Map to [0, 100]
                
                vals_a_scaled = [scale_standardized_to_radar(val) for val in vals_a_raw] + [scale_standardized_to_radar(vals_a_raw[0])]
                vals_b_scaled = [scale_standardized_to_radar(val) for val in vals_b_raw] + [scale_standardized_to_radar(vals_b_raw[0])]
                
                fig = go.Figure()
                
                # Player 1 - Enhanced styling
                fig.add_trace(go.Scatterpolar(
                    r=vals_a_scaled,
                    theta=skills + [skills[0]],
                    fill='toself',
                    name=p1,
                    line=dict(color='#00c6ff', width=4),
                    fillcolor='rgba(0,198,255,0.4)',
                    marker=dict(size=8, color='#00c6ff', symbol='circle')
                ))
                
                # Player 2 - Enhanced styling
                fig.add_trace(go.Scatterpolar(
                    r=vals_b_scaled,
                    theta=skills + [skills[0]],
                    fill='toself',
                    name=p2,
                    line=dict(color='#ff4757', width=4),
                    fillcolor='rgba(255,71,87,0.4)',
                    marker=dict(size=8, color='#ff4757', symbol='circle')
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100],
                            tickfont=dict(size=14, color='white'),
                            gridcolor='rgba(255,255,255,0.3)',
                            linecolor='rgba(255,255,255,0.4)',
                            tickmode='linear',
                            tick0=0,
                            dtick=20,  # 0, 20, 40, 60, 80, 100
                            showticklabels=True
                        ),
                        angularaxis=dict(
                            tickfont=dict(size=16, color='white', family='Inter'),
                            linecolor='rgba(255,255,255,0.4)',
                            gridcolor='rgba(255,255,255,0.3)'
                        ),
                        bgcolor='rgba(10,10,11,0.8)'
                    ),
                    template="plotly_dark",
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.15,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=14, color='white', family='Inter'),
                        bgcolor='rgba(0,0,0,0.5)',
                        bordercolor='rgba(255,255,255,0.2)',
                        borderwidth=1
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=600,
                    margin=dict(t=50, b=100, l=50, r=50)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Explanation of scaling
                st.markdown('''
                <div class="radar-info">
                    <strong>📘 Radar Chart Scale:</strong> Values are StandardScaler normalized (mean=0, std=1) then mapped to 0-100 for visualization.
                    Center (50) = Average, Outer edge (100) = Excellent, Inner (0) = Below average
                </div>
                ''', unsafe_allow_html=True)
                
                # Show actual standardized values in a table
                st.markdown("**📋 Standardized Values (Z-scores):**")
                skills_data = {
                    "Skill": skills,
                    p1: [f"{val:.2f}" for val in vals_a_raw],
                    p2: [f"{val:.2f}" for val in vals_b_raw]
                }
                skills_df = pd.DataFrame(skills_data)
                st.dataframe(skills_df, use_container_width=True, hide_index=True)

            # Enhanced Comparison Table
            st.markdown("### 📋 Detailed Comparison")
            
            # Comparison attributes
            attrs = ["Age","Height","Weight","OVR","market_value"] + skills
            
            # Create comparison table using Streamlit's native dataframe
            comparison_data = []
            for attr in attrs:
                if attr in df.columns:
                    val_a = a.get(attr, 'N/A')
                    val_b = b.get(attr, 'N/A')
                    
                    # Format values
                    if attr == "market_value":
                        val_a_display = f"€{val_a:.1f}M" if isinstance(val_a, (int, float)) else str(val_a)
                        val_b_display = f"€{val_b:.1f}M" if isinstance(val_b, (int, float)) else str(val_b)
                    elif attr in ["Age", "Height", "Weight"]:
                        val_a_display = f"{val_a:.0f}" if isinstance(val_a, (int, float)) else str(val_a)
                        val_b_display = f"{val_b:.0f}" if isinstance(val_b, (int, float)) else str(val_b)
                    else:
                        val_a_display = f"{val_a:.2f}" if isinstance(val_a, (int, float)) else str(val_a)
                        val_b_display = f"{val_b:.2f}" if isinstance(val_b, (int, float)) else str(val_b)
                    
                    # Determine winner
                    winner = ""
                    if isinstance(val_a, (int, float)) and isinstance(val_b, (int, float)):
                        if val_a > val_b:
                            winner = f"{p1} 👑"
                        elif val_b > val_a:
                            winner = f"{p2} 👑"
                        else:
                            winner = "Tie"
                    
                    comparison_data.append({
                        "Attribute": attr,
                        p1: val_a_display,
                        p2: val_b_display,
                        "Winner": winner
                    })
            
            comparison_df = pd.DataFrame(comparison_data)
            
            st.dataframe(
                comparison_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Winner": st.column_config.TextColumn(
                        "Winner",
                        help="Player with better value"
                    )
                }
            )

    # Back button
    st.markdown("---")
    if st.button("🔙 Back to Dashboard", key="back_btn", use_container_width=True):
        st.session_state.current_page = "dashboard"

if __name__ == "__main__":
    main()
