# pages/scout_assistant.py

import streamlit as st
import pandas as pd
import numpy as np
import time
import random
import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from rag_system import FootballRAGSystem
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    st.error("RAG system not available. Please check backend/rag_system.py")

@st.cache_data
def load_data():
    try:
        return pd.read_csv('forwards_clean_with_market_values_updated.csv')
    except FileNotFoundError:
        st.error("Data file not found.")
        return pd.DataFrame()

# Initialize RAG system
@st.cache_resource
def initialize_rag_system():
    """Initialize the RAG system once and cache it"""
    if not RAG_AVAILABLE:
        return None
    
    try:
        rag = FootballRAGSystem()
        # Run the async initialization in a sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(rag.initialize())
        loop.close()
        return rag
    except Exception as e:
        st.error(f"Failed to initialize RAG system: {e}")
        return None

async def get_rag_response(rag_system, query):
    """Get response from RAG system"""
    try:
        result = await rag_system.process_query(query)
        return result["answer"]
    except Exception as e:
        return f"❌ **Error processing query:** {str(e)}\n\nPlease check if Ollama is running and the vector database is set up correctly."

def generate_fallback_response(query, df):
    """Fallback response system when RAG is not available"""
    query_lower = query.lower()
    
    if not df.empty:
        # Most valuable forwards
        if any(word in query_lower for word in ['valuable', 'expensive', 'price', 'cost', 'market']):
            if 'market_value' in df.columns:
                top_valuable = df[df['market_value'].notna()].nlargest(5, 'market_value')
                if not top_valuable.empty:
                    response = "💰 **Most Valuable Forwards:**\n\n"
                    for i, (_, player) in enumerate(top_valuable.iterrows(), 1):
                        response += f"{i}. **{player['Name']}** - €{player['market_value']:.1f}M"
                        if 'Team' in player and pd.notna(player['Team']):
                            response += f" ({player['Team']})"
                        response += "\n"
                    return response
        
        # Premier League specific
        elif 'premier league' in query_lower or 'premier' in query_lower:
            if 'League' in df.columns:
                premier_players = df[df['League'].str.contains('Premier League', case=False, na=False)]
                if not premier_players.empty:
                    if 'fast' in query_lower and 'PACE' in premier_players.columns:
                        fastest = premier_players.nlargest(5, 'PACE')
                        response = "⚡ **Fastest Premier League Forwards:**\n\n"
                        for i, (_, player) in enumerate(fastest.iterrows(), 1):
                            response += f"{i}. **{player['Name']}** - {player['PACE']:.2f} PACE"
                            if 'Team' in player and pd.notna(player['Team']):
                                response += f" ({player['Team']})"
                            response += "\n"
                        return response
                    else:
                        top_pl = premier_players.nlargest(5, 'OVR') if 'OVR' in premier_players.columns else premier_players.head(5)
                        response = "🏆 **Top Premier League Forwards:**\n\n"
                        for i, (_, player) in enumerate(top_pl.iterrows(), 1):
                            ovr = f" - {player['OVR']:.2f} OVR" if 'OVR' in player and pd.notna(player['OVR']) else ""
                            response += f"{i}. **{player['Name']}**{ovr}"
                            if 'Team' in player and pd.notna(player['Team']):
                                response += f" ({player['Team']})"
                            response += "\n"
                        return response
    
    # Default helpful response
    return """🤖 **RAG System Unavailable - Using Basic Mode**

I can still help with basic queries! Try asking:
• "Most valuable forwards"
• "Who is the fastest player in Premier League?"
• "Best overall players"

For advanced analysis with natural language processing, please:
1. Start Ollama service
2. Set up the vector database
3. Ensure backend/rag_system.py is accessible
"""

def main():
    # Enhanced CSS (same as before but with RAG status indicators)
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
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--bg) 0%, #1a1a2e 50%, var(--bg) 100%) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .page-header {
        text-align: center;
        padding: 2.5rem 0;
        background: linear-gradient(135deg, rgba(0,230,118,0.1), rgba(0,198,255,0.1));
        border-radius: 25px;
        margin-bottom: 2rem;
        border: 1px solid rgba(0,230,118,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .page-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--accent), var(--primary), var(--purple));
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        margin: 0;
        animation: titleGlow 4s ease-in-out infinite alternate;
    }
    
    .page-subtitle {
        font-size: 1.2rem;
        color: var(--text-muted);
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    @keyframes titleGlow {
        0% { filter: drop-shadow(0 0 15px rgba(0,230,118,0.6)); }
        100% { filter: drop-shadow(0 0 30px rgba(0,198,255,0.8)); }
    }
    
    .rag-status {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .rag-enabled {
        background: linear-gradient(135deg, var(--accent), #2ed573);
        color: white;
    }
    
    .rag-disabled {
        background: linear-gradient(135deg, var(--orange), #ff6b35);
        color: white;
    }
    
    .chat-container {
        background: var(--card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border);
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: var(--shadow);
        overflow: hidden;
        position: relative;
    }
    
    .chat-header {
        background: linear-gradient(135deg, var(--surface), rgba(255,255,255,0.05));
        padding: 1.5rem;
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .ai-avatar {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, var(--accent), var(--primary));
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        animation: avatarPulse 3s ease-in-out infinite;
    }
    
    @keyframes avatarPulse {
        0%, 100% { transform: scale(1); box-shadow: 0 0 20px rgba(0,230,118,0.3); }
        50% { transform: scale(1.05); box-shadow: 0 0 30px rgba(0,198,255,0.5); }
    }
    
    .chat-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--text);
    }
    
    .chat-status {
        font-size: 0.9rem;
        color: var(--accent);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background: var(--accent);
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    .chat-messages {
        padding: 1.5rem;
        max-height: 400px;
        overflow-y: auto;
        min-height: 100px;
    }
    
    .message {
        padding: 1rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        max-width: 85%;
        word-wrap: break-word;
        animation: messageSlide 0.3s ease-out;
    }
    
    @keyframes messageSlide {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .message.assistant {
        background: linear-gradient(135deg, var(--surface), rgba(0,230,118,0.1));
        border: 1px solid rgba(0,230,118,0.2);
        border-left: 4px solid var(--accent);
    }
    
    .message.user {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        margin-left: auto;
        text-align: right;
    }
    
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--text-muted);
        font-style: italic;
        margin: 1rem 0;
    }
    
    .typing-dots {
        display: flex;
        gap: 0.25rem;
    }
    
    .typing-dot {
        width: 6px;
        height: 6px;
        background: var(--accent);
        border-radius: 50%;
        animation: typingDot 1.4s ease-in-out infinite;
    }
    
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typingDot {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }
    
    .stat-card {
        background: var(--card);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        border-color: var(--primary);
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
    
    # Initialize RAG system
    rag_system = initialize_rag_system()
    
    # Page Header with RAG status
    rag_status_text = "🦙 RAG + LLM Enabled" if rag_system else "⚠️ Basic Mode"
    rag_status_class = "rag-enabled" if rag_system else "rag-disabled"
    
    st.markdown(f'''
    <div class="page-header">
        <h1 class="page-title">🤖 Scout Assistant</h1>
        <p class="page-subtitle">AI-powered scouting with intelligent data analysis</p>
        <span class="rag-status {rag_status_class}">{rag_status_text}</span>
    </div>
    ''', unsafe_allow_html=True)
    
    df = load_data()
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        if rag_system:
            welcome_msg = "👋 **Hello! I'm your AI football scout powered by Llama LLM.**\n\nI can provide detailed analysis about forwards using natural language. Ask me anything like:\n• \"Who is the fastest player in Premier League?\"\n• \"Compare Mbappe vs Haaland\"\n• \"Find young French talents under €20M\""
        else:
            welcome_msg = "👋 **Hello! I'm running in basic mode.**\n\nRAG system is not available. I can still help with simple queries about forwards in the database."
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    
    # Enhanced Chat Interface
    status_text = "RAG + LLM Ready" if rag_system else "Basic Mode Active"
    
    st.markdown(f'''
    <div class="chat-container">
        <div class="chat-header">
            <div class="ai-avatar">🤖</div>
            <div>
                <div class="chat-title">Scout Assistant</div>
                <div class="chat-status">
                    <div class="status-dot"></div>
                    <span>{status_text}</span>
                </div>
            </div>
        </div>
        <div class="chat-messages">
    ''', unsafe_allow_html=True)
    
    # Display messages
    for message in st.session_state.messages:
        role_class = "assistant" if message["role"] == "assistant" else "user"
        clean_content = message["content"].replace("</div>", "").replace("<div>", "")
        st.markdown(f'''
        <div class="message {role_class}">
            {clean_content}
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Enhanced suggestion buttons based on RAG availability
    st.markdown("### 💡 Quick Suggestions")
    
    if rag_system:
        suggestions = [
            "Who is the fastest player in Premier League?",
            "Compare Mbappe vs Haaland", 
            "Find young French talents under €20M",
            "Best finishers in Serie A",
            "Strongest physical players in Bundesliga",
            "Most valuable La Liga forwards",
            "Young prospects under 23",
            "Cheapest talents with potential"
        ]
    else:
        suggestions = [
            "Most valuable forwards",
            "Who is the fastest player in Premier League?", 
            "Best overall players",
            "Top young prospects",
            "Premier League forwards",
            "La Liga talents",
            "Fastest players overall",
            "Most expensive forwards"
        ]
    
    cols = st.columns(4)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 4]:
            if st.button(f"💫 {suggestion}", key=f"sug_{i}", use_container_width=True):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": suggestion})
                
                # Generate response
                if rag_system:
                    # Show typing indicator
                    typing_placeholder = st.empty()
                    typing_placeholder.markdown('''
                    <div class="typing-indicator">
                        🤖 Analyzing with RAG + LLM...
                        <div class="typing-dots">
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Get RAG response
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    response = loop.run_until_complete(get_rag_response(rag_system, suggestion))
                    loop.close()
                    
                    typing_placeholder.empty()
                else:
                    with st.spinner("🔍 Processing..."):
                        time.sleep(1)
                        response = generate_fallback_response(suggestion, df)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
    
    # Text Input
    st.markdown("### 💬 Ask Your Question")
    
    with st.form("chat_form", clear_on_submit=True):
        if rag_system:
            placeholder_text = "e.g., Compare Salah and Son, or find young talents under €15M"
        else:
            placeholder_text = "e.g., Who are the fastest Premier League forwards?"
            
        user_input = st.text_input(
            "Type your question...", 
            placeholder=placeholder_text,
            label_visibility="collapsed"
        )
        col1, col2, col3 = st.columns([1, 1, 2])
        with col2:
            submitted = st.form_submit_button("🚀 Send", use_container_width=True)
    
    if submitted and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        if rag_system:
            # Show enhanced processing message
            with st.spinner("🦙 Processing with Llama LLM..."):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(get_rag_response(rag_system, user_input))
                loop.close()
        else:
            with st.spinner("🤖 Processing..."):
                time.sleep(1)
                response = generate_fallback_response(user_input, df)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    # Database stats
    if not df.empty:
        st.markdown("### 📊 Database Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
            <div class="stat-card">
                <div style="font-size: 2rem; color: var(--primary); font-weight: 700;">{len(df)}</div>
                <div style="color: var(--text-muted); font-size: 0.9rem;">Total Forwards</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            leagues = df['League'].nunique() if 'League' in df.columns else 0
            st.markdown(f'''
            <div class="stat-card">
                <div style="font-size: 2rem; color: var(--accent); font-weight: 700;">{leagues}</div>
                <div style="color: var(--text-muted); font-size: 0.9rem;">Leagues</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            teams = df['Team'].nunique() if 'Team' in df.columns else 0
            st.markdown(f'''
            <div class="stat-card">
                <div style="font-size: 2rem; color: var(--purple); font-weight: 700;">{teams}</div>
                <div style="color: var(--text-muted); font-size: 0.9rem;">Teams</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            if 'market_value' in df.columns:
                avg_value = df['market_value'].mean()
                st.markdown(f'''
                <div class="stat-card">
                    <div style="font-size: 2rem; color: var(--gold); font-weight: 700;">€{avg_value:.1f}M</div>
                    <div style="color: var(--text-muted); font-size: 0.9rem;">Avg Value</div>
                </div>
                ''', unsafe_allow_html=True)
    
    # System Status and Controls
    st.markdown("### 🔧 System Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if rag_system:
            st.success("✅ **RAG System Active**\n- 🦙 Llama LLM connected\n- 📚 Vector database loaded\n- 🤖 Advanced analysis available")
        else:
            st.warning("⚠️ **Basic Mode Active**\n- RAG system unavailable\n- Limited query processing\n- Start Ollama & setup vector DB for full features")
    
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            if rag_system:
                welcome_msg = "👋 **Hello! I'm your AI football scout powered by Llama LLM.**\n\nI can provide detailed analysis about forwards using natural language. Ask me anything!"
            else:
                welcome_msg = "👋 **Hello! I'm running in basic mode.**\n\nRAG system is not available. I can still help with simple queries about forwards in the database."
            st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
            st.rerun()
    
    # Back button
    st.markdown("---")
    if st.button("🔙 Back to Dashboard", use_container_width=True):
        st.session_state.current_page = "dashboard"

if __name__ == "__main__":
    main()
