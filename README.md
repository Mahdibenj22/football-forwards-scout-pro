Football Forwards Scout Pro
An advanced football scouting dashboard powered by Streamlit, offering interactive analytics, AI-driven recommendations, and comprehensive visualizations to help scouts, analysts, and enthusiasts discover, compare, and evaluate forwards.

🚀 Live Demo
👉 https://football-forwards-scout-pro-joypynurnw6drb2rdpbu3h.streamlit.app/

📦 Features
Dashboard Overview
Displays key metrics (total forwards, leagues, teams, average market value) and quick access cards to all scouting tools.

Forward Profile
Deep-dive into individual player statistics with an interactive radar chart, strengths & weaknesses, and performance badges.

Player Comparison
Side-by-side comparison of two players across multiple attributes, including tactical insights and summary tables.

Player Similarity
Find look-alike forwards using cosine similarity on eight engineered features (Pace, Shooting, Passing, Dribbling, Physical, Aerial, Mental, Overall).

Scouting Metrics
Advanced scatter plots, distribution analyses, and correlation insights across any two metrics with optional bubble sizing and color coding.

Performance Trends
League-based trend analysis showing median performance, distributions, and detailed statistics with interactive tabs.

3D Exploration
Three-dimensional scatter plots for custom feature analyses, with modes for performance clustering, league comparison, and market value.

Scout Assistant
AI-powered chat assistant leveraging a RAG system and Llama LLM to answer scouting queries, suggest players, and compare talents.

📁 Repository Structure
text
football-forwards-scout-pro/
│
├── app.py                                # Main application entry point
├── requirements.txt                      # Python dependencies
├── forwards_clean_with_market_values_updated.csv
├── setup_vectordb.py                     # Backend vector DB setup
├── backend/                              # RAG system and embeddings
│   ├── main.py
│   └── rag_system.py
└── pages/                                # Streamlit page modules
    ├── comparison.py
    ├── exploration_3d.py
    ├── forward_profile.py
    ├── performance_trends.py
    ├── scout_assistant.py
    ├── scouting_metrics.py
    └── similarity.py
🛠️ Installation & Setup
Clone the repository

bash
git clone https://github.com/Mahdibenj22/football-forwards-scout-pro.git
cd football-forwards-scout-pro
Create a virtual environment (optional but recommended)

bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
Install dependencies

bash
pip install -r requirements.txt
Prepare vector database (for Scout Assistant)

bash
python setup_vectordb.py
Ensure chromadb and Ollama are running for full AI features.

🎯 Running Locally
bash
streamlit run app.py
The app will open at http://localhost:8501.

☁️ Deployment to Streamlit Cloud
Push your code to a public GitHub repo.

Sign up at share.streamlit.io and connect your GitHub account.

Click New app → select your repo, branch main, and app.py as the entrypoint.

Click Deploy. Your app will be live in a few minutes!

🔧 Usage Tips
Collapsible Sidebar: Click the “☰” icon top-left to expand/collapse navigation.

Feature Cards: Click any card on the dashboard for quick access.

AI Chat: Use Scout Assistant for natural-language scouting queries (requires RAG backend).

Similarity Thresholds: Scores >0.8 indicate very similar playing styles.

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/my-feature)

Commit your changes (git commit -m 'Add awesome feature')

Push to the branch (git push origin feature/my-feature)

Open a Pull Request

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.
