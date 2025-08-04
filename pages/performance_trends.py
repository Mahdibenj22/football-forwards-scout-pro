# pages/performance_trends.py

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
    # Enhanced CSS for Performance Trends page
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
        padding: 3rem 0;
        background: linear-gradient(135deg, rgba(255,107,53,0.1), rgba(139,92,246,0.1));
        border-radius: 25px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,107,53,0.2);
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
        background: radial-gradient(circle at 20% 30%, rgba(255,107,53,0.1), transparent 60%),
                    radial-gradient(circle at 80% 70%, rgba(139,92,246,0.1), transparent 60%);
        pointer-events: none;
        animation: backgroundShift 6s ease-in-out infinite alternate;
    }
    
    @keyframes backgroundShift {
        0% { transform: scale(1) rotate(0deg); }
        100% { transform: scale(1.1) rotate(2deg); }
    }
    
    .page-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--orange), var(--purple), var(--primary));
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        margin: 0;
        position: relative;
        z-index: 2;
        animation: titleGlow 4s ease-in-out infinite alternate;
    }
    
    .page-subtitle {
        font-size: 1.3rem;
        color: var(--text-muted);
        margin-top: 0.5rem;
        position: relative;
        z-index: 2;
        font-weight: 400;
    }
    
    @keyframes titleGlow {
        0% { filter: drop-shadow(0 0 10px rgba(255,107,53,0.5)); }
        100% { filter: drop-shadow(0 0 25px rgba(139,92,246,0.8)); }
    }
    
    .filter-label {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .league-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-card {
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
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, var(--primary)10, var(--purple)10);
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
    }
    
    .stat-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(255,107,53,0.2);
        border-color: var(--orange);
    }
    
    .stat-card:hover::before {
        opacity: 1;
    }
    
    .stat-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
        position: relative;
        z-index: 2;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--primary);
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        z-index: 2;
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
    }
    
    .chart-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.3);
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
        width: 80px;
        height: 3px;
        background: linear-gradient(90deg, var(--orange), var(--purple));
        border-radius: 2px;
    }
    
    .analysis-insights {
        background: linear-gradient(135deg, rgba(0,230,118,0.1), rgba(0,198,255,0.1));
        border: 1px solid rgba(0,230,118,0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .insight-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--accent);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .insight-card {
        background: var(--surface);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateY(-2px);
        border-color: var(--accent);
        box-shadow: 0 8px 16px rgba(0,230,118,0.1);
    }
    
    .insight-metric {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--accent);
        margin-bottom: 0.5rem;
    }
    
    .insight-desc {
        color: var(--text-muted);
        font-size: 0.95rem;
        line-height: 1.4;
    }
    
    .league-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .warning-panel {
        background: linear-gradient(135deg, rgba(255,107,53,0.1), rgba(255,215,0,0.1));
        border: 1px solid rgba(255,107,53,0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* CRITICAL: Hide all empty containers */
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
    
    /* Hide empty vertical blocks */
    div[data-testid="stVerticalBlock"]:empty {
        display: none !important;
    }
    
    div[data-testid="stVerticalBlock"] > div:empty {
        display: none !important;
    }
    
    /* Hide empty horizontal blocks */
    div[data-testid="stHorizontalBlock"]:empty {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Enhanced Page Header
    st.markdown('''
    <div class="page-header">
        <h1 class="page-title">📈 Performance Trends</h1>
        <p class="page-subtitle">League-based analysis and performance trends over time</p>
    </div>
    ''', unsafe_allow_html=True)
    
    df = load_data()
    if df.empty:
        return

    if "League" not in df.columns:
        st.error("League column missing from data.")
        return

    # FIXED: Direct filter section without containers
    st.markdown("### 🎯 Select Leagues for Analysis")
    
    # Show league overview
    league_counts = df["League"].value_counts()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        leagues = st.multiselect(
            "Choose leagues to compare:", 
            sorted(df["League"].unique()),
            help="Select 2-5 leagues for meaningful comparison"
        )
        analyze_button = st.button("🚀 Analyze Trends", use_container_width=True)
    
    with col2:
        st.markdown("**📊 League Overview**")
        top_leagues = league_counts.head(5)
        for league, count in top_leagues.items():
            st.markdown(f'<span class="league-badge">{league}: {count}</span>', unsafe_allow_html=True)
    
    if analyze_button:
        if not leagues:
            st.markdown('''
            <div class="warning-panel">
                <strong>⚠️ No leagues selected</strong><br>
                Please select at least one league to begin analysis
            </div>
            ''', unsafe_allow_html=True)
            return
        
        filtered = df[df["League"].isin(leagues)]
        if filtered.empty:
            st.warning("No data found for selected leagues.")
            return

        # Enhanced League Statistics
        st.markdown("### 📊 League Statistics")
        
        # League stats cards
        stats_data = []
        for league in leagues:
            league_data = filtered[filtered["League"] == league]
            stats_data.append({
                "League": league,
                "Players": len(league_data),
                "Avg_Age": league_data["Age"].mean() if "Age" in league_data.columns else 0,
                "Avg_OVR": league_data["OVR"].mean() if "OVR" in league_data.columns else 0,
                "Avg_Value": league_data["market_value"].mean() if "market_value" in league_data.columns else 0
            })
        
        # Display league cards
        cols = st.columns(len(leagues))
        for i, (col, league) in enumerate(zip(cols, leagues)):
            league_stats = stats_data[i]
            with col:
                st.markdown(f'''
                <div class="stat-card">
                    <div class="stat-icon">🏆</div>
                    <div class="stat-value">{league_stats["Players"]}</div>
                    <div class="stat-label">{league}</div>
                    <div style="margin-top: 1rem; font-size: 0.8rem; color: var(--text-muted);">
                        Avg Age: {league_stats["Avg_Age"]:.1f}<br>
                        Avg OVR: {league_stats["Avg_OVR"]:.2f}
                    </div>
                </div>
                ''', unsafe_allow_html=True)

        # Enhanced Analysis with Tabs
        tab1, tab2, tab3 = st.tabs(["📊 League Comparison", "📈 Distribution Analysis", "📋 Detailed Statistics"])
        
        with tab1:
            st.markdown("### 📈 Median Performance Trends")
            
            # Get numeric metrics
            metrics = [m for m in ["OVR","PACE","SHOOTING","PASSING","DRIBBLING","PHYSICAL","AERIAL","MENTAL","Age"] if m in filtered.columns]
            if not metrics:
                st.error("No numeric columns found for analysis.")
                return

            # Create trend data
            trend_data = []
            for lg in leagues:
                group = filtered[filtered["League"] == lg]
                for m in metrics[:6]:  # Limit to 6 metrics for clarity
                    trend_data.append({
                        "League": lg,
                        "Metric": m,
                        "Median": group[m].median(),
                        "Mean": group[m].mean(),
                        "Players": len(group)
                    })
            
            trend_df = pd.DataFrame(trend_data)
            
            # Enhanced line chart
            fig = px.line(
                trend_df, 
                x="Metric", 
                y="Median", 
                color="League", 
                markers=True,
                title="",
                hover_data=["Mean", "Players"]
            )
            
            fig.update_traces(
                line=dict(width=4),
                marker=dict(size=10)
            )
            
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=500,
                xaxis=dict(
                    tickfont=dict(size=14, color='white'),
                    title=dict(text="Performance Metrics", font=dict(size=16, color='white'))
                ),
                yaxis=dict(
                    tickfont=dict(size=14, color='white'),
                    title=dict(text="Median Score", font=dict(size=16, color='white'))
                ),
                legend=dict(
                    font=dict(size=12, color='white'),
                    bgcolor='rgba(0,0,0,0.5)',
                    bordercolor='rgba(255,255,255,0.2)',
                    borderwidth=1
                ),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.markdown("### 📊 Performance Distribution")
            
            metric = st.selectbox("Choose metric for distribution analysis:", metrics, key="dist_metric")
            
            # Enhanced box plot
            fig = px.box(
                filtered, 
                x="League", 
                y=metric, 
                color="League",
                title="",
                hover_data=["Name"] if "Name" in filtered.columns else None
            )
            
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=500,
                xaxis=dict(
                    tickfont=dict(size=14, color='white'),
                    title=dict(text="League", font=dict(size=16, color='white')),
                    tickangle=45
                ),
                yaxis=dict(
                    tickfont=dict(size=14, color='white'),
                    title=dict(text=f"{metric} Score", font=dict(size=16, color='white'))
                ),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.markdown("### 📋 Comprehensive League Statistics")
            
            # Create comprehensive statistics table
            detailed_stats = []
            for lg in leagues:
                grp = filtered[filtered["League"] == lg]
                row = {"League": lg, "Players": len(grp)}
                
                for m in metrics:
                    series = grp[m].dropna()
                    if not series.empty:
                        row[f"{m}_Mean"] = f"{series.mean():.2f}"
                        row[f"{m}_Median"] = f"{series.median():.2f}"
                        row[f"{m}_Std"] = f"{series.std():.2f}"
                        row[f"{m}_Max"] = f"{series.max():.2f}"
                        row[f"{m}_Min"] = f"{series.min():.2f}"
                
                detailed_stats.append(row)
            
            stats_df = pd.DataFrame(detailed_stats)
            
            # Display enhanced dataframe
            st.dataframe(
                stats_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "League": st.column_config.TextColumn("League", width="medium"),
                    "Players": st.column_config.NumberColumn("Players", format="%d")
                }
            )

        # Enhanced Insights Panel
        st.markdown("### 🔍 Key Insights")
        
        # Generate insights
        insights = []
        
        # Best performing league
        if "OVR" in filtered.columns:
            league_ovr = filtered.groupby("League")["OVR"].mean()
            best_league = league_ovr.idxmax()
            best_score = league_ovr.max()
            insights.append({
                "metric": f"{best_score:.2f}",
                "desc": f"Average OVR in {best_league} (highest among selected leagues)"
            })
        
        # Most players
        player_counts = filtered["League"].value_counts()
        biggest_league = player_counts.idxmax()
        biggest_count = player_counts.max()
        insights.append({
            "metric": f"{biggest_count}",
            "desc": f"Players in {biggest_league} (largest representation)"
        })
        
        # Age analysis
        if "Age" in filtered.columns:
            youngest_league = filtered.groupby("League")["Age"].mean().idxmin()
            youngest_age = filtered.groupby("League")["Age"].mean().min()
            insights.append({
                "metric": f"{youngest_age:.1f}",
                "desc": f"Average age in {youngest_league} (youngest league)"
            })
        
        # Market value analysis
        if "market_value" in filtered.columns:
            mv_data = filtered[filtered["market_value"].notna()]
            if not mv_data.empty:
                highest_value_league = mv_data.groupby("League")["market_value"].mean().idxmax()
                highest_value = mv_data.groupby("League")["market_value"].mean().max()
                insights.append({
                    "metric": f"€{highest_value:.1f}M",
                    "desc": f"Average market value in {highest_value_league}"
                })
        
        # Display insights
        cols = st.columns(len(insights))
        for col, insight in zip(cols, insights):
            with col:
                st.markdown(f'''
                <div class="insight-card">
                    <div class="insight-metric">{insight["metric"]}</div>
                    <div class="insight-desc">{insight["desc"]}</div>
                </div>
                ''', unsafe_allow_html=True)

    # Back button
    st.markdown("---")
    if st.button("🔙 Back to Dashboard", key="back_btn", use_container_width=True):
        st.session_state.current_page = "dashboard"

if __name__ == "__main__":
    main()
