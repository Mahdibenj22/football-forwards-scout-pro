import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import os

# Add pages directory to path
sys.path.append(str(Path(__file__).parent / "pages"))

# Configure page - START COLLAPSED
st.set_page_config(
    page_title="Football Scouting Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start collapsed
)

# Enhanced CSS with collapsible sidebar and navigation
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* AGGRESSIVE: Hide ALL Streamlit's built-in navigation elements */
.css-k1vhr4, .css-zt5igj, .css-1lcbmhc > div:first-child,
section[data-testid="stSidebar"] > div:first-child > div:first-child,
.css-1lcbmhc .css-1outpf7 > div:first-child,
div[data-testid="stSidebarNav"], 
div[data-testid="stSidebarNavItems"],
.css-1544g2n > div:first-child,
.css-17lntkn, .css-pkbazv,
[data-testid="stSidebarNav"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    width: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Hide the collapse button */
button[kind="header"] {
    display: none !important;
}

/* Hide any remaining navigation containers */
.css-1d391kg > div:first-child {
    display: none !important;
}

/* Ensure sidebar starts with our content */
.css-1d391kg {
    padding-top: 0 !important;
}

:root {
    --primary: #00c6ff;
    --secondary: #0072ff;
    --accent: #00e676;
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
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Premium Sidebar Styling */
.css-1d391kg {
    background: linear-gradient(180deg, #0a0a0b 0%, #1a1a2e 50%, #0a0a0b 100%) !important;
    border-right: 1px solid rgba(0,198,255,0.2) !important;
    padding-top: 0 !important;
}

.css-1544g2n { 
    padding: 0 !important; 
}

/* App Header in Sidebar */
.sidebar-header {
    text-align: center;
    padding: 2rem 1rem;
    background: linear-gradient(135deg, rgba(0,198,255,0.1), rgba(139,92,246,0.1));
    border-radius: 20px;
    margin: 1rem;
    border: 1px solid rgba(0,198,255,0.2);
}

.sidebar-title {
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #00c6ff, #8b5cf6, #00e676);
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
    margin: 0;
}

.sidebar-subtitle {
    font-size: 0.85rem;
    color: #a0a0a0;
    margin-top: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* Hero Section */
.hero-container {
    text-align: center;
    padding: 2rem 0 3rem 0;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.main-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #00c6ff 0%, #0072ff 50%, #00e676 100%);
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1.2;
    animation: titleGlow 3s ease-in-out infinite alternate;
}

.title-icon {
    font-size: 3.5rem;
    margin-right: 1rem;
    display: inline-block;
    animation: bounce 2s ease-in-out infinite;
}

.subtitle {
    font-size: 1.2rem;
    color: var(--text-muted);
    margin-top: 1rem;
    font-weight: 400;
}

@keyframes titleGlow {
    0% { filter: drop-shadow(0 0 10px rgba(0,198,255,0.5)); }
    100% { filter: drop-shadow(0 0 20px rgba(0,198,255,0.8)); }
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
}

/* Section Headers */
.section-header {
    font-size: 2rem;
    font-weight: 600;
    margin: 2.5rem 0 1.5rem 0;
    color: var(--text);
    text-align: center;
    position: relative;
}

.section-header::before {
    content: '';
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    bottom: -8px;
    width: 50px;
    height: 3px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    border-radius: 2px;
}

/* Metrics */
[data-testid="metric-container"] {
    background: var(--card) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    box-shadow: var(--shadow) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 15px 30px rgba(0,198,255,0.2) !important;
    border-color: var(--primary) !important;
}

[data-testid="stMetricValue"] {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: var(--primary) !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.85rem !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    font-weight: 500 !important;
}

/* Clickable Feature Cards */
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
    padding: 0;
}

.feature-card {
    background: var(--card);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
    text-align: center;
    box-shadow: var(--shadow);
    height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(0,198,255,0.1), rgba(0,114,255,0.1));
    opacity: 0;
    transition: opacity 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-8px) scale(1.02);
    border-color: var(--primary);
    box-shadow: 0 20px 40px rgba(0,198,255,0.25);
}

.feature-card:hover::before {
    opacity: 1;
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    display: block;
    position: relative;
    z-index: 2;
    transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon {
    transform: scale(1.1);
}

.feature-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text);
    position: relative;
    z-index: 2;
}

.feature-desc {
    font-size: 0.85rem;
    color: var(--text-muted);
    line-height: 1.4;
    position: relative;
    z-index: 2;
    font-weight: 400;
}

/* CTA Section */
.cta-section {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, rgba(0,198,255,0.1), rgba(0,114,255,0.1));
    border-radius: 20px;
    margin: 2rem 0;
    border: 1px solid rgba(0,198,255,0.2);
    position: relative;
}

.cta-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--primary);
    margin-bottom: 0.5rem;
}

.cta-text {
    font-size: 1rem;
    color: var(--text-muted);
}

.pulse-dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    background: var(--accent);
    border-radius: 50%;
    margin-right: 0.5rem;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.2); }
    100% { opacity: 1; transform: scale(1); }
}

/* Data Preview */
.stCheckbox {
    margin-top: 1.5rem;
}

.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: var(--shadow);
}

/* Remove conflicting styles */
div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="element-container"] {
    margin-bottom: 0 !important;
}

/* Custom scrollbar for sidebar */
.css-1d391kg::-webkit-scrollbar { width: 4px; }
.css-1d391kg::-webkit-scrollbar-thumb {
    background: rgba(0,198,255,0.3);
    border-radius: 4px;
}
.css-1d391kg::-webkit-scrollbar-thumb:hover {
    background: rgba(0,198,255,0.5);
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"

# Render Premium Sidebar (when expanded)
def render_sidebar():
    with st.sidebar:
        # Sidebar Header
        st.markdown('''
        <div class="sidebar-header">
            <div class="sidebar-title">⚽ Scout Pro</div>
            <div class="sidebar-subtitle">Quick Navigation</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Navigation buttons
        pages = [
            ("Dashboard", "🏠", "dashboard"),
            ("Forward Profile", "👤", "forward_profile"),
            ("Comparison", "⚖️", "comparison"),
            ("Similarity", "🔍", "similarity"),
            ("Scouting Metrics", "📊", "scouting_metrics"),
            ("Performance Trends", "📈", "performance_trends"),
            ("3D Exploration", "🎯", "exploration_3d"),
            ("Scout Assistant", "🤖", "scout_assistant")
        ]
        
        for name, icon, page_key in pages:
            if st.button(f"{icon} {name}", key=f"sidebar_{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()

# Enhanced data loading
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('forwards_clean_with_market_values_updated.csv')
        return df
    except FileNotFoundError:
        st.error("⚠️ Data file not found. Please ensure 'forwards_clean_with_market_values_updated.csv' is in the project directory.")
        return pd.DataFrame()

# Main dashboard content
def show_dashboard():
    # Load data
    df = load_data()
    
    # Hero section
    st.markdown('''
    <div class="hero-container">
        <h1 class="main-title">
            <span class="title-icon">⚽</span>Forward Scouting Dashboard
        </h1>
        <p class="subtitle">Advanced Analytics & Intelligence for Football Scouts</p>
    </div>
    ''', unsafe_allow_html=True)
    
    if not df.empty:
        # Key Statistics
        st.markdown('<div class="section-header">📊 Key Statistics</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_forwards = len(df)
            st.metric("⚽ Total Forwards", f"{total_forwards:,}")
        
        with col2:
            leagues_count = df['League'].nunique() if 'League' in df.columns else 0
            st.metric("🏆 Leagues", leagues_count)
        
        with col3:
            teams_count = df['Team'].nunique() if 'Team' in df.columns else 0
            st.metric("👕 Teams", teams_count)
        
        with col4:
            if 'market_value' in df.columns:
                avg_market_value = df['market_value'].mean()
                st.metric("💰 Avg Market Value", f"€{avg_market_value:.1f}M")
            else:
                avg_overall = df['OVR'].mean() if 'OVR' in df.columns else 0
                st.metric("⭐ Avg Overall", f"{avg_overall:.1f}")
        
        # Clickable Scouting Tools
        st.markdown('<div class="section-header">🚀 Scouting Tools</div>', unsafe_allow_html=True)
        
        # Create clickable feature cards
        features = [
            {"icon": "👤", "title": "Forward Profile", "desc": "Individual player analysis", "page": "forward_profile"},
            {"icon": "⚖️", "title": "Player Comparison", "desc": "Side-by-side comparisons", "page": "comparison"},
            {"icon": "🔍", "title": "Similarity Finder", "desc": "AI-powered matching", "page": "similarity"},
            {"icon": "📊", "title": "Scouting Metrics", "desc": "Advanced statistics", "page": "scouting_metrics"},
            {"icon": "📈", "title": "Performance Trends", "desc": "League analysis", "page": "performance_trends"},
            {"icon": "🎯", "title": "3D Exploration", "desc": "Interactive visualization", "page": "exploration_3d"},
            {"icon": "🤖", "title": "Scout Assistant", "desc": "AI recommendations", "page": "scout_assistant"}
        ]
        
        # Create columns for feature cards
        cols = st.columns(3)
        for i, feature in enumerate(features):
            with cols[i % 3]:
                if st.button(
                    f"{feature['icon']}\n{feature['title']}\n{feature['desc']}", 
                    key=f"feature_{feature['page']}",
                    use_container_width=True,
                    help=f"Navigate to {feature['title']}"
                ):
                    st.session_state.current_page = feature["page"]
                    st.rerun()
        
        # CTA Section
        st.markdown('''
        <div class="cta-section">
            <h3 class="cta-title">🎯 Ready to Scout?</h3>
            <p class="cta-text">
                <span class="pulse-dot"></span>Click any tool above or use the sidebar (☰) for quick navigation
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Data preview
        if st.checkbox("📋 Preview Database", help="Show sample data"):
            st.markdown('<div class="section-header">📊 Data Sample</div>', unsafe_allow_html=True)
            
            preview_cols = ['Name', 'Team', 'League', 'Age', 'Position']
            if 'market_value' in df.columns:
                preview_cols.append('market_value')
            if 'OVR' in df.columns:
                preview_cols.append('OVR')
                
            existing_cols = [col for col in preview_cols if col in df.columns]
            preview_df = df[existing_cols].head(10)
            
            st.dataframe(
                preview_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "market_value": st.column_config.NumberColumn(
                        "Market Value (€M)",
                        format="€%.1fM"
                    ),
                    "Age": st.column_config.NumberColumn(
                        "Age", 
                        format="%d yrs"
                    )
                }
            )
    
    else:
        st.markdown('''
        <div style="text-align: center; padding: 3rem; background: var(--card); border-radius: 20px; margin: 2rem 0;">
            <h2 style="color: #ff6b6b; margin-bottom: 1rem;">⚠️ Database Unavailable</h2>
            <p style="color: var(--text-muted);">Unable to load player data.</p>
        </div>
        ''', unsafe_allow_html=True)

# Page routing
def main():
    render_sidebar()
    
    current_page = st.session_state.current_page
    
    try:
        if current_page == "dashboard":
            show_dashboard()
        else:
            # Import and run the specific page
            module = __import__(current_page)
            module.main()
    except ModuleNotFoundError as e:
        st.error(f"⚠️ Page '{current_page}' not found: {e}")
        st.info("Returning to dashboard...")
        st.session_state.current_page = "dashboard"
        show_dashboard()
    except Exception as e:
        st.error(f"⚠️ Error loading page: {e}")
        st.info("Returning to dashboard...")
        st.session_state.current_page = "dashboard"
        show_dashboard()

if __name__ == "__main__":
    main()
