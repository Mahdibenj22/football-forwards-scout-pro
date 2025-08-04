import pandas as pd
import numpy as np
import re
import streamlit as st

@st.cache_data
def load_data():
    """
    Load and preprocess the forwards dataset.
    Returns a DataFrame with numeric columns coerced and an OVR_size for marker sizing.
    """
    df = pd.read_csv("forwards_clean_with_market_values_updated.csv")
    # Ensure numeric columns
    cols = ["PACE","SHOOTING","PASSING","DRIBBLING","PHYSICAL","AERIAL",
            "MENTAL","OVR","Age","Height","Weight","market_value"]
    df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")
    # Size for scatter marker
    df["OVR_size"] = ((df["OVR"] - df["OVR"].min()) /
                      (df["OVR"].max() - df["OVR"].min())) * 30 + 5
    return df

def smart_query_processor(query: str, df):
    """
    Process a natural language query into filtered results or comparisons.
    Returns formatted markdown string.
    """
    q = query.lower().strip()
    # Nations mapping
    nations = {
        'brazil': ['brazil', 'brazilian'],
        'argentina': ['argentina','argentinian','argentine'],
        'france': ['france','french'],
        'spain': ['spain','spanish'],
        'england': ['england','english'],
        'germany': ['germany','german'],
        'italy': ['italy','italian'],
        'portugal': ['portugal','portuguese'],
        'netherlands': ['netherlands','dutch'],
        'belgium': ['belgium','belgian']
    }
    # Identify nation
    found_nation = next((n for n, keys in nations.items() if any(k in q for k in keys)), None)
    # Price filter
    price_limit = None
    if any(w in q for w in ['under','below','less than','cheaper']) and ('€' in q or 'million' in q or 'm' in q):
        m = re.findall(r'(\d+)', q)
        if m:
            price_limit = float(m[-1])
    # Age filter
    age_limit = None
    if any(w in q for w in ['under','below','younger']) and any(w in q for w in ['age','years','young']):
        m = re.findall(r'under (\d+)', q)
        age_limit = int(m[0]) if m else (23 if 'young' in q else None)
    # Position filter
    position_filter = None
    if 'winger' in q:
        position_filter = 'LW|RW|LM|RM'
    elif 'striker' in q or 'forward' in q:
        position_filter = 'ST|CF'
    # Attribute sort
    attr_map = {
        'PACE': ['fast','fastest','speed','pace'],
        'PHYSICAL': ['strong','strongest','physical','power'],
        'SHOOTING': ['finish','finisher','goalscorer','shooting'],
        'DRIBBLING': ['dribble','dribbler','skill','tricks'],
        'PASSING': ['pass','passing','playmaker','creative'],
        'AERIAL': ['aerial','header'],
        'MENTAL': ['mental','composure']
    }
    attribute_sort = next((a for a, keys in attr_map.items() if any(k in q for k in keys)), None)

    # Apply filters
    df_f = df.copy()
    title_parts = []
    if found_nation:
        df_f = df_f[df_f['Nation'].str.lower().str.contains(found_nation)]
        title_parts.append(found_nation.title())
    if position_filter:
        df_f = df_f[df_f['Position'].str.contains(position_filter, case=False, na=False)]
        title_parts.append("Wingers" if 'winger' in q else "Forwards")
    if price_limit:
        df_f = df_f[df_f['market_value'] < price_limit]
        title_parts.append(f"Under €{price_limit}M")
    if age_limit:
        df_f = df_f[df_f['Age'] < age_limit]
        title_parts.append(f"Under {age_limit}")
    # Sort & slice
    if attribute_sort:
        df_r = df_f.nlargest(10, attribute_sort)
        title_parts.insert(0, {
            'PACE': "Fastest",
            'PHYSICAL': "Strongest",
            'SHOOTING': "Best Finishing",
            'DRIBBLING': "Best Dribbling",
            'PASSING': "Best Passing"
        }.get(attribute_sort, attribute_sort))
    else:
        df_r = df_f.nlargest(10, 'OVR')
        if not title_parts:
            title_parts.append("Top Players")
    title = " ".join(title_parts) if title_parts else "Players"
    # Comparison or player info
    if ' vs ' in q or 'compare' in q:
        from pages.comparison import handle_query_comparison
        return handle_query_comparison(q, df)
    for nm in df['Name']:
        if len(nm) > 3 and nm.lower() in q:
            from pages.forward_profile import format_player_info
            return format_player_info(nm, df)
    # Format results
    return format_results(df_r, title)

def format_results(df, title: str) -> str:
    if df.empty:
        return f"No players found for {title}."
    md = f"## {title}\n\n"
    for i, (_, p) in enumerate(df.head(10).iterrows(), 1):
        md += (f"**{i}. {p['Name']}** ({p['Team']})  \n"
               f"• League: {p['League']} | Age: {int(p['Age'])}  \n"
               f"• OVR: {p['OVR']:.1f} | Value: €{p['market_value']:.1f}M  \n"
               f"• Pace: {p['PACE']:.0f}, Shoot: {p['SHOOTING']:.0f}, Pass: {p['PASSING']:.0f}\n\n")
    return md
