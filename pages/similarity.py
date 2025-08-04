# pages/similarity.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

@st.cache_data
def load_data():
    try:
        return pd.read_csv('forwards_clean_with_market_values_updated.csv')
    except FileNotFoundError:
        st.error("Data file not found.")
        return pd.DataFrame()

@st.cache_data
def prepare_similarity_data(df):
    """Prepare data for similarity analysis"""
    # Keep only the scaled feature columns
    feature_cols = ['PACE','SHOOTING','PASSING','DRIBBLING',
                    'PHYSICAL','AERIAL','MENTAL','OVR']
    
    # Check if all required columns exist
    missing_cols = [col for col in feature_cols if col not in df.columns]
    if missing_cols:
        st.error(f"Missing required columns: {missing_cols}")
        return None, None, None
    
    # Create forwards_scaled (assuming the data is already scaled)
    forwards_scaled = df.copy()
    
    # Extract feature matrix
    X_fw = forwards_scaled[feature_cols].values
    
    # Create name to index mapping
    name_to_idx = {name: idx for idx, name in enumerate(forwards_scaled['Name'])}
    
    return forwards_scaled, X_fw, name_to_idx

def get_top_similar_forwards(player_name, forwards_scaled, X_fw, name_to_idx, 
                           top_n=10, include_ovr_weight=False, ovr_weight=0.15):
    """
    Return top-N similar forwards (name, similarity score).
    Cosine similarity on scaled engineered features.
    """
    if player_name not in name_to_idx:
        raise ValueError(f"{player_name} not found in forward list.")

    idx = name_to_idx[player_name]
    target_vec = X_fw[idx].reshape(1, -1)

    # Compute cosine similarity to all others
    sims = cosine_similarity(target_vec, X_fw)[0]

    # Optionally penalize large OVR gaps
    if include_ovr_weight:
        ovr_gap = abs(forwards_scaled['OVR'].values - forwards_scaled.iloc[idx]['OVR'])
        if ovr_gap.max() > 0:  # Avoid division by zero
            sims = sims * (1 - ovr_weight * (ovr_gap / ovr_gap.max()))

    # Build result dataframe
    results = pd.DataFrame({
        'Name': forwards_scaled['Name'],
        'Club': forwards_scaled.get('Team', 'Unknown'),
        'League': forwards_scaled.get('League', 'Unknown'),
        'Similarity': sims,
        'OVR': forwards_scaled.get('OVR', 0),
        'Age': forwards_scaled.get('Age', 0),
        'market_value': forwards_scaled.get('market_value', 0)
    })

    # Exclude the player himself and sort
    results = results[results['Name'] != player_name] \
                 .sort_values('Similarity', ascending=False) \
                 .head(top_n) \
                 .reset_index(drop=True)

    return results

def main():
    # Enhanced CSS with CRITICAL empty container fixes
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
        --teal: #20b2aa;
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
        background: linear-gradient(135deg, rgba(32,178,170,0.1), rgba(139,92,246,0.1));
        border-radius: 25px;
        margin-bottom: 2rem;
        border: 1px solid rgba(32,178,170,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .page-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--teal), var(--purple), var(--primary));
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        margin: 0;
        animation: titleFlow 6s ease-in-out infinite alternate;
    }
    
    .page-subtitle {
        font-size: 1.3rem;
        color: var(--text-muted);
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    @keyframes titleFlow {
        0% { filter: drop-shadow(0 0 20px rgba(32,178,170,0.6)); }
        100% { filter: drop-shadow(0 0 35px rgba(139,92,246,0.8)); }
    }
    
    .player-card {
        background: linear-gradient(145deg, var(--surface), rgba(255,255,255,0.05));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .player-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 16px 32px rgba(32,178,170,0.2);
        border-color: var(--teal);
    }
    
    .similarity-score {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: linear-gradient(135deg, var(--teal), var(--primary));
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
    }
    
    .player-info {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .info-item {
        text-align: center;
    }
    
    .info-value {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text);
    }
    
    .info-label {
        font-size: 0.8rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.25rem;
    }
    
    .target-player {
        background: linear-gradient(145deg, rgba(32,178,170,0.2), rgba(139,92,246,0.1));
        border: 2px solid var(--teal);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .target-name {
        font-size: 2rem;
        font-weight: 800;
        color: var(--teal);
        margin-bottom: 1rem;
    }
    
    .similarity-bar {
        background: var(--surface);
        border-radius: 10px;
        height: 8px;
        margin: 0.5rem 0;
        overflow: hidden;
        position: relative;
    }
    
    .similarity-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--teal), var(--primary));
        border-radius: 10px;
        transition: width 0.6s ease;
    }
    
    .controls-panel {
        background: rgba(32,178,170,0.1);
        border: 1px solid rgba(32,178,170,0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .stat-box {
        background: var(--card);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }
    
    .stat-box:hover {
        transform: translateY(-2px);
        border-color: var(--teal);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: var(--text-muted);
        font-size: 0.9rem;
    }
    
    /* CRITICAL: Hide ALL empty containers */
    .element-container:empty {
        display: none !important;
    }
    
    .stContainer > div:empty {
        display: none !important;
    }
    
    div[data-testid="stVerticalBlock"]:empty {
        display: none !important;
    }
    
    div[data-testid="stHorizontalBlock"]:empty {
        display: none !important;
    }
    
    /* Hide empty columns and containers */
    div[data-testid="column"]:empty {
        display: none !important;
    }
    
    .stMarkdown:empty {
        display: none !important;
    }
    
    /* Hide plotly loading containers */
    .js-plotly-plot .plotly .modebar {
        background: transparent !important;
    }
    
    /* Hide streamlit specific empty elements */
    .stPlotlyChart > div:empty {
        display: none !important;
    }
    
    .stSelectbox > div:empty {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Page Header
    st.markdown('''
    <div class="page-header">
        <h1 class="page-title">🔍 Player Similarity</h1>
        <p class="page-subtitle">Advanced cosine similarity analysis to find player lookalikes</p>
    </div>
    ''', unsafe_allow_html=True)
    
    df = load_data()
    if df.empty:
        return

    # Prepare similarity data
    result = prepare_similarity_data(df)
    if result[0] is None:
        return
    
    forwards_scaled, X_fw, name_to_idx = result
    
    # FIXED: Direct components without unnecessary containers
    st.markdown("### 🎯 Find Similar Players")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Player selection
        players = sorted(forwards_scaled['Name'].tolist())
        selected_player = st.selectbox(
            "Choose a player to find similar players:",
            [""] + players,
            help="Select a player to analyze their playing style and find similar forwards"
        )
        
        if selected_player:
            # Advanced controls in a styled container
            st.markdown('''
            <div class="controls-panel">
                <h4 style="color: var(--teal); margin-bottom: 1rem;">⚙️ Analysis Settings</h4>
            </div>
            ''', unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                top_n = st.slider("🔢 Number of similar players", 5, 20, 10)
                
            with col_b:
                include_ovr = st.checkbox("📊 Weight by overall rating", value=False,
                                        help="Boost similarity for players with similar overall ratings")
            
            if include_ovr:
                ovr_weight = st.slider("⚖️ OVR weight influence", 0.0, 0.5, 0.15, 0.05)
            else:
                ovr_weight = 0.15
    
    with col2:
        if selected_player:
            # Target player info
            target_info = forwards_scaled[forwards_scaled['Name'] == selected_player].iloc[0]
            
            st.markdown(f'''
            <div class="target-player">
                <div class="target-name">{selected_player}</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 0.9rem;">
                    <div><strong>Team:</strong> {target_info.get('Team', 'Unknown')}</div>
                    <div><strong>League:</strong> {target_info.get('League', 'Unknown')}</div>
                    <div><strong>Age:</strong> {int(target_info.get('Age', 0))} years</div>
                    <div><strong>OVR:</strong> {target_info.get('OVR', 0):.2f}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Generate similarity results
    if selected_player:
        try:
            with st.spinner("🔍 Finding similar players using cosine similarity..."):
                similar_players = get_top_similar_forwards(
                    selected_player, 
                    forwards_scaled, 
                    X_fw, 
                    name_to_idx,
                    top_n=top_n,
                    include_ovr_weight=include_ovr,
                    ovr_weight=ovr_weight
                )
            
            if not similar_players.empty:
                # Results Display
                st.markdown(f"### 🎯 Top {top_n} Similar Players")
                
                # Similarity visualization
                st.markdown("### 📊 Similarity Scores")
                
                # Create similarity bar chart
                fig_bar = go.Figure()
                
                fig_bar.add_trace(go.Bar(
                    x=similar_players['Similarity'],
                    y=similar_players['Name'],
                    orientation='h',
                    marker=dict(
                        color=similar_players['Similarity'],
                        colorscale='Teal',
                        colorbar=dict(title="Similarity Score")
                    ),
                    text=[f"{score:.3f}" for score in similar_players['Similarity']],
                    textposition='inside',
                    hovertemplate=
                    "<b>%{y}</b><br>" +
                    "Similarity: %{x:.3f}<br>" +
                    "<extra></extra>"
                ))
                
                fig_bar.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    xaxis=dict(
                        title="Similarity Score",
                        tickfont=dict(color='white'),
                        range=[0, 1]
                    ),
                    yaxis=dict(
                        title="",
                        tickfont=dict(color='white'),
                        categoryorder='total ascending'
                    ),
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                
                st.plotly_chart(fig_bar, use_container_width=True)
                
                # Player cards with enhanced styling
                for idx, (_, player) in enumerate(similar_players.iterrows()):
                    similarity_score = player['Similarity']
                    
                    # Color coding based on similarity
                    if similarity_score >= 0.9:
                        score_color = "#00e676"  # Green for very high similarity
                    elif similarity_score >= 0.8:
                        score_color = "#00c6ff"  # Blue for high similarity
                    elif similarity_score >= 0.7:
                        score_color = "#ffd700"  # Gold for good similarity
                    else:
                        score_color = "#ff6b35"  # Orange for moderate similarity
                    
                    st.markdown(f'''
                    <div class="player-card">
                        <div class="similarity-score" style="background: {score_color};">
                            #{idx + 1} • {similarity_score:.3f}
                        </div>
                        <h3 style="color: var(--teal); margin: 0 0 1rem 0; font-size: 1.3rem;">
                            {player['Name']}
                        </h3>
                        <div class="player-info">
                            <div class="info-item">
                                <div class="info-value">{player.get('Club', 'Unknown')}</div>
                                <div class="info-label">Team</div>
                            </div>
                            <div class="info-item">
                                <div class="info-value">{player.get('League', 'Unknown')}</div>
                                <div class="info-label">League</div>
                            </div>
                            <div class="info-item">
                                <div class="info-value">{int(player.get('Age', 0))} yrs</div>
                                <div class="info-label">Age</div>
                            </div>
                        </div>
                        <div class="similarity-bar">
                            <div class="similarity-fill" style="width: {similarity_score * 100}%;"></div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Advanced Analytics
                st.markdown("### 📈 Similarity Analysis")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_similarity = similar_players['Similarity'].mean()
                    st.markdown(f'''
                    <div class="stat-box">
                        <div class="stat-value" style="color: var(--teal);">{avg_similarity:.3f}</div>
                        <div class="stat-label">Average Similarity</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col2:
                    max_similarity = similar_players['Similarity'].max()
                    best_match = similar_players.iloc[0]['Name']
                    st.markdown(f'''
                    <div class="stat-box">
                        <div class="stat-value" style="color: var(--accent);">{max_similarity:.3f}</div>
                        <div class="stat-label">Best Match: {best_match}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col3:
                    # Count high similarity players (>0.8)
                    high_sim_count = len(similar_players[similar_players['Similarity'] > 0.8])
                    st.markdown(f'''
                    <div class="stat-box">
                        <div class="stat-value" style="color: var(--primary);">{high_sim_count}</div>
                        <div class="stat-label">High Similarity (>0.8)</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Export results
                st.markdown("### 💾 Export Results")
                
                # Create downloadable CSV
                export_df = similar_players.copy()
                export_df['Target_Player'] = selected_player
                export_df = export_df[['Target_Player', 'Name', 'Club', 'League', 'Similarity', 'OVR', 'Age', 'market_value']]
                
                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="📊 Download Similarity Report (CSV)",
                    data=csv,
                    file_name=f"{selected_player.replace(' ', '_')}_similarity_report.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            else:
                st.warning("No similar players found. Try adjusting the parameters.")
                
        except Exception as e:
            st.error(f"Error finding similar players: {str(e)}")
    
    else:
        # Help section when no player is selected
        st.markdown("### 🤖 How Player Similarity Works")
        
        st.markdown("""
**🔍 Cosine Similarity Algorithm**

Our similarity engine uses advanced machine learning to find players with similar playing styles:

- **📊 Feature Analysis:** Compares eight key attributes: Pace, Shooting, Passing, Dribbling, Physical, Aerial, Mental, and Overall.
- **📐 Cosine Similarity:** Measures the angle between player vectors in multi-dimensional space.
- **⚖️ OVR Weighting:** Optionally boosts similarity scores when players have similar overall ratings.
- **📈 Normalized Scores:** Results range from 0 (completely different) to 1 (identical).

> 💡 **Tip:** Scores above 0.8 indicate very similar playing styles, while scores above 0.9 suggest near-identical player profiles.
""")

    # Back button
    st.markdown("---")
    if st.button("🔙 Back to Dashboard", key="back_btn", use_container_width=True):
        st.session_state.current_page = "dashboard"

if __name__ == "__main__":
    main()
