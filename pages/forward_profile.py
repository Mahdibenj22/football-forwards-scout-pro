# pages/forward_profile.py

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
    # Enhanced CSS for Forward Profile page
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary: #00c6ff;
        --secondary: #0072ff;
        --accent: #00e676;
        --gold: #ffd700;
        --orange: #ff6b35;
        --purple: #8b5cf6;
        --bg: #0a0a0b;
        --surface: #1a1a1b;
        --card: rgba(255,255,255,0.08);
        --text: #ffffff;
        --text-muted: #a0a0a0;
        --border: rgba(255,255,255,0.1);
        --shadow: 0 8px 32px rgba(0,0,0,0.4);
        --glow: 0 0 20px rgba(0,198,255,0.3);
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--bg) 0%, #1a1a2e 50%, var(--bg) 100%) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .page-header {
        text-align: center;
        padding: 2.5rem 0;
        background: linear-gradient(135deg, rgba(0,198,255,0.1), rgba(139,92,246,0.1));
        border-radius: 25px;
        margin-bottom: 2rem;
        border: 1px solid rgba(0,198,255,0.2);
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
        background: radial-gradient(circle at 25% 25%, rgba(0,198,255,0.1), transparent 50%),
                    radial-gradient(circle at 75% 75%, rgba(139,92,246,0.1), transparent 50%);
        pointer-events: none;
    }
    
    .page-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary), var(--purple), var(--accent));
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        margin: 0;
        position: relative;
        z-index: 2;
        animation: titlePulse 3s ease-in-out infinite alternate;
    }
    
    .page-subtitle {
        font-size: 1.2rem;
        color: var(--text-muted);
        margin-top: 0.5rem;
        position: relative;
        z-index: 2;
    }
    
    @keyframes titlePulse {
        0% { filter: drop-shadow(0 0 10px rgba(0,198,255,0.5)); }
        100% { filter: drop-shadow(0 0 20px rgba(139,92,246,0.8)); }
    }
    
    .filter-panel {
        background: var(--card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
    }
    
    .player-hero {
        background: linear-gradient(145deg, var(--card), rgba(255,255,255,0.05));
        backdrop-filter: blur(20px);
        border: 1px solid var(--border);
        border-radius: 25px;
        padding: 3rem 2rem;
        margin: 2rem 0;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
    }
    
    .player-hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(0,198,255,0.05), rgba(139,92,246,0.05));
        pointer-events: none;
    }
    
    .player-name {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        margin: 0 0 1rem 0;
        text-align: center;
        position: relative;
        z-index: 2;
    }
    
    .player-info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
        position: relative;
        z-index: 2;
    }
    
    .info-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .info-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0,198,255,0.2);
        border-color: var(--primary);
    }
    
    .info-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .info-card:hover::before {
        opacity: 1;
    }
    
    .info-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .info-label {
        font-size: 0.9rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .info-value {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--text);
    }
    
    .radar-section {
        background: var(--card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: var(--shadow);
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 1.5rem;
        text-align: center;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--purple));
        border-radius: 2px;
    }
    
    .strengths-weaknesses {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .strength-card, .weakness-card {
        background: var(--surface);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }
    
    .strength-card {
        border-left: 4px solid var(--accent);
        background: linear-gradient(135deg, rgba(46,213,115,0.1), var(--surface));
    }
    
    .weakness-card {
        border-left: 4px solid var(--orange);
        background: linear-gradient(135deg, rgba(255,107,53,0.1), var(--surface));
    }
    
    .strength-card:hover, .weakness-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .strength-title {
        color: var(--accent);
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .weakness-title {
        color: var(--orange);
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .skill-list {
        font-size: 1.1rem;
        color: var(--text);
        font-weight: 500;
    }
    
    .performance-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .badge-excellent {
        background: linear-gradient(135deg, var(--accent), #2ed573);
        color: white;
    }
    
    .badge-good {
        background: linear-gradient(135deg, var(--gold), #ffa500);
        color: white;
    }
    
    .badge-average {
        background: linear-gradient(135deg, var(--orange), #ff6b35);
        color: white;
    }
    
    .market-value-display {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,107,53,0.1));
        border: 1px solid rgba(255,215,0,0.2);
        border-radius: 20px;
        margin: 2rem 0;
    }
    
    .market-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--gold), var(--orange));
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .market-label {
        font-size: 1rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Hide empty containers */
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
        <h1 class="page-title">👤 Forward Profile</h1>
        <p class="page-subtitle">Deep-dive analysis of individual players with comprehensive stats</p>
    </div>
    ''', unsafe_allow_html=True)
    
    df = load_data()
    if df.empty:
        return

    # Validate columns
    required = ["Position", "Name"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Missing columns: {missing}")
        return

    # Enhanced filter section
    st.markdown("### 🎯 Player Selection")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.form("fp_filters", clear_on_submit=False):
            pos = st.selectbox("Position (required)", sorted(df["Position"].unique()))
            styles = st.multiselect("Play Style (optional)", 
                                  sorted(df.get("play style", pd.Series()).fillna("N/A").unique()))
            submitted = st.form_submit_button("🔄 Apply Filters", use_container_width=True)
    
    with col2:
        # Filter info
        if submitted:
            df = df[df["Position"] == pos]
            if styles:
                df = df[df["play style"].fillna("N/A").isin(styles)]
        
        st.markdown(f"""
        <div style="background: rgba(0,198,255,0.1); border: 1px solid rgba(0,198,255,0.2); 
                    border-radius: 12px; padding: 1rem; margin-top: 1rem;">
            <strong>📊 Available Players:</strong> {len(df)}<br>
            <strong>🎯 Position:</strong> {pos if submitted else 'Not selected'}<br>
            <strong>🎨 Styles:</strong> {len(styles) if styles else 'Any'}
        </div>
        """, unsafe_allow_html=True)
    
    if df.empty:
        st.warning("No players found with the selected filters.")
        return

    # Player selection
    player = st.selectbox("Choose a player:", [""] + list(df["Name"].sort_values()))
    
    if player:
        p = df[df["Name"] == player].iloc[0]
        
        # Enhanced Player Hero Section
        st.markdown(f'''
        <div class="player-hero">
            <div class="player-name">{p['Name']}</div>
        ''', unsafe_allow_html=True)
        
        # Player Information Grid
        col1, col2, col3, col4 = st.columns(4)
        
        info_items = [
            ("🌍", "Nation", p.get('Nation', 'N/A')),
            ("🏆", "League", p.get('League', 'N/A')),
            ("👕", "Team", p.get('Team', 'N/A')),
            ("📅", "Age", f"{int(p['Age'])} yrs" if pd.notna(p.get('Age')) else 'N/A')
        ]
        
        for col, (icon, label, value) in zip([col1, col2, col3, col4], info_items):
            with col:
                st.markdown(f'''
                <div class="info-card">
                    <span class="info-icon">{icon}</span>
                    <div class="info-label">{label}</div>
                    <div class="info-value">{value}</div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Additional details
        col1, col2, col3 = st.columns(3)
        
        additional_items = [
            ("📏", "Height", p.get('Height', 'N/A')),
            ("⚖️", "Weight", p.get('Weight', 'N/A')),
            ("🎮", "Play Style", p.get('play style', 'N/A'))
        ]
        
        for col, (icon, label, value) in zip([col1, col2, col3], additional_items):
            with col:
                st.markdown(f'''
                <div class="info-card">
                    <span class="info-icon">{icon}</span>
                    <div class="info-label">{label}</div>
                    <div class="info-value">{value}</div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Key Performance Indicators
        col1, col2 = st.columns(2)
        
        with col1:
            if "OVR" in p.index:
                ovr_value = p["OVR"]
                # Determine performance level
                if ovr_value > 2.5:
                    badge_class = "badge-excellent"
                    level = "Excellent"
                elif ovr_value > 1.0:
                    badge_class = "badge-good" 
                    level = "Good"
                else:
                    badge_class = "badge-average"
                    level = "Average"
                
                st.markdown(f'''
                <div style="text-align: center; padding: 1.5rem; background: var(--card); 
                            border-radius: 16px; border: 1px solid var(--border);">
                    <div style="font-size: 2rem; font-weight: 800; color: var(--primary); 
                                margin-bottom: 0.5rem;">{ovr_value:.2f}</div>
                    <div style="color: var(--text-muted); margin-bottom: 1rem;">Overall Rating</div>
                    <span class="performance-badge {badge_class}">{level}</span>
                </div>
                ''', unsafe_allow_html=True)
        
        with col2:
            if "market_value" in p.index and pd.notna(p["market_value"]):
                mv_value = p["market_value"]
                st.markdown(f'''
                <div class="market-value-display">
                    <div class="market-value">€{mv_value:.1f}M</div>
                    <div class="market-label">Market Value</div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown('''
                <div style="text-align: center; padding: 2rem; background: var(--surface); 
                            border-radius: 16px; border: 1px solid var(--border);">
                    <div style="color: var(--text-muted);">Market Value</div>
                    <div style="font-size: 1.5rem; color: var(--text);">Not Available</div>
                </div>
                ''', unsafe_allow_html=True)

        # Enhanced Radar Chart - FIXED SCALING
        skills = [s for s in ["PACE","SHOOTING","PASSING","DRIBBLING","PHYSICAL","AERIAL","MENTAL"] if s in p.index]
        
        if skills:
            st.markdown('''
            <div class="radar-section">
                <div class="section-title">📊 Skill Radar</div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Get raw standardized values and scale for radar
            skill_values = [p[s] for s in skills]
            
            # Transform standardized values to 0-100 scale for radar visualization
            def scale_for_radar(val):
                # Map standardized values (roughly -3 to +3) to 0-100 scale
                clamped = max(-3.5, min(3.5, val))
                return ((clamped + 3.5) / 7.0) * 100
            
            radar_values = [scale_for_radar(val) for val in skill_values] + [scale_for_radar(skill_values[0])]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=radar_values,
                theta=skills + [skills[0]],
                fill='toself',
                name=player,
                line=dict(color='#00c6ff', width=4),
                fillcolor='rgba(0,198,255,0.4)',
                marker=dict(size=10, color='#00c6ff', symbol='circle')
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
                        dtick=20
                    ),
                    angularaxis=dict(
                        tickfont=dict(size=16, color='white', family='Inter'),
                        linecolor='rgba(255,255,255,0.4)',
                        gridcolor='rgba(255,255,255,0.3)'
                    ),
                    bgcolor='rgba(10,10,11,0.8)'
                ),
                template="plotly_dark",
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=500,
                margin=dict(t=20, b=20, l=20, r=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Enhanced Strengths & Weaknesses
            skill_data = pd.Series(skill_values, index=skills)
            top2 = list(skill_data.nlargest(2).index)
            bottom2 = list(skill_data.nsmallest(2).index)
            
            st.markdown('''
            <div class="strengths-weaknesses">
                <div class="strength-card">
                    <div class="strength-title">
                        <span>💪</span>
                        <span>Strengths</span>
                    </div>
                    <div class="skill-list">''' + ', '.join(top2) + '''</div>
                </div>
                <div class="weakness-card">
                    <div class="weakness-title">
                        <span>⚠️</span>
                        <span>Areas to Improve</span>
                    </div>
                    <div class="skill-list">''' + ', '.join(bottom2) + '''</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Raw values table
            st.markdown("### 📋 Detailed Skill Breakdown")
            
            skill_breakdown = []
            for skill in skills:
                raw_val = p[skill]
                radar_val = scale_for_radar(raw_val)
                
                # Determine grade
                if radar_val >= 80:
                    grade = "A"
                elif radar_val >= 65:
                    grade = "B"
                elif radar_val >= 50:
                    grade = "C"
                elif radar_val >= 35:
                    grade = "D"
                else:
                    grade = "F"
                
                skill_breakdown.append({
                    "Skill": skill,
                    "Raw Score": f"{raw_val:.3f}",
                    "Percentile": f"{radar_val:.1f}%",
                    "Grade": grade
                })
            
            breakdown_df = pd.DataFrame(skill_breakdown)
            st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
        
        else:
            st.info("No skill data available for radar chart.")

    # Back button
    st.markdown("---")
    if st.button("🔙 Back to Dashboard", key="back_btn", use_container_width=True):
        st.session_state.current_page = "dashboard"

if __name__ == "__main__":
    main()
