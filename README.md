# Football Forwards Scout Pro

An advanced football scouting dashboard powered by Streamlit, offering interactive analytics, AI-driven recommendations, and comprehensive visualizations to help scouts, analysts, and enthusiasts discover, compare, and evaluate forwards.

---

## 🚀 Live Demo

[https://football-forwards-scout-pro-joypynurnw6drb2rdpbu3h.streamlit.app/](https://football-forwards-scout-pro-joypynurnw6drb2rdpbu3h.streamlit.app/)

---

## 📦 Features

### 1. Dashboard Overview
- **Key Metrics**: Total forwards, leagues, teams, average market value  
- **Quick Access Cards**: Navigate to each scouting tool  

### 2. Forward Profile
- Individual player deep dive  
- Interactive radar chart, strengths & weaknesses  
- Performance badges and market value display  

### 3. Player Comparison
- Side-by-side comparison of two players  
- Tactical insights and comparison tables  

### 4. Player Similarity
- Cosine similarity on eight attributes (Pace, Shooting, Passing, Dribbling, Physical, Aerial, Mental, Overall)  
- Optional weighting by overall rating  
- Visual similarity scores and distribution  

### 5. Scouting Metrics
- Custom scatter plots with bubble sizing and color coding  
- Correlation analysis and distribution histograms  

### 6. Performance Trends
- League-based trend analysis (median, distribution, detailed stats)  
- Interactive charts grouped by league  

### 7. 3D Exploration
- Three-dimensional scatter plots for custom feature analysis  
- Modes: Performance clustering, league comparison, market value  

### 8. Scout Assistant
- AI-powered chat assistant using RAG + Llama LLM  
- Natural-language scouting queries and recommendations  

---

## 📁 Repository Structure

football-forwards-scout-pro/
├── app.py
├── requirements.txt
├── forwards_clean_with_market_values_updated.csv
├── setup_vectordb.py
├── backend/
│ ├── main.py
│ └── rag_system.py
└── pages/
├── compariso
.py ├── explorati
n_3d.py ├── forwar
_profile.py ├── perfo
mance_trends.py ├─
scout_assistant.py

---

## 🛠️ Installation & Setup

1. **Clone the repository**
git clone https://github.com/Mahdibenj22/football-forwards-scout-pro.git
cd football-forwards-scout-pro
2. **Create a virtual environment** (recommended)
python -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows
3. **Install dependencies**
pip install -r requirements.txt
4. **(Optional) Prepare vector database**
python setup_vectordb.py

---

## 🎯 Running Locally


Open your browser at `http://localhost:8501`.

---

## ☁️ Deploy to Streamlit Cloud

1. Push code to a **public** GitHub repo.  
2. Sign in at [share.streamlit.io](https://share.streamlit.io/).  
3. Click **New app**, select your repo, branch `main`, and entry `app.py`.  
4. Click **Deploy**—your app will be live in minutes!

---

## 🤝 Contributing

1. Fork this repo  
2. Create a branch: `git checkout -b feature/my-feature`  
3. Commit: `git commit -m "Add new feature"`  
4. Push: `git push origin feature/my-feature`  
5. Open a Pull Request  

---

## 📄 License

This project is licensed under the MIT License. 



