# backend/rag_system.py - PRODUCTION-GRADE RAG+LLM FOOTBALL SCOUTING SYSTEM
import chromadb
import requests
import json
from sentence_transformers import SentenceTransformer
import pandas as pd
import os
import re

class FootballRAGSystem:
    def __init__(self):
        self.client = None
        self.collection = None
        self.embedder = None
        self.df = None
        
    async def initialize(self):
        """Initialize all components"""
        print("🔄 Initializing RAG system...")
        
        # Load data
        csv_path = "../forwards_clean_with_market_values_updated.csv"
        if not os.path.exists(csv_path):
            csv_path = "forwards_clean_with_market_values_updated.csv"
        
        self.df = pd.read_csv(csv_path)
        print(f"📊 Loaded {len(self.df)} players")
        
        # Enhanced data cleaning and validation
        self.df = self.clean_and_validate_data()
        
        # Initialize ChromaDB
        db_path = "../football_vectordb"
        if not os.path.exists(db_path):
            db_path = "./football_vectordb"
            
        self.client = chromadb.PersistentClient(path=db_path)
        
        try:
            self.collection = self.client.get_collection("football_players")
            print("📚 Connected to existing vector database")
        except:
            raise Exception("Vector database not found. Please run setup_vectordb.py first!")
        
        # Initialize embedding model
        print("🤖 Loading embedding model...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Test Ollama connection
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code != 200:
                raise Exception(f"Ollama returned status {response.status_code}")
            print("🦙 Ollama connection verified")
        except Exception as e:
            raise Exception(f"Ollama is not running or not accessible: {e}")
        
        print("✅ RAG system initialized successfully!")
    
    def clean_and_validate_data(self):
        """Enhanced data cleaning and validation"""
        df = self.df.copy()
        
        # Basic cleaning
        df = df.dropna(subset=['Name'])
        df['market_value'] = pd.to_numeric(df['market_value'], errors='coerce').fillna(0)
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce').fillna(25)
        
        # Fix Overall Rating scale (convert normalized values to 0-100 scale if needed)
        if 'OVR' in df.columns:
            df['OVR'] = pd.to_numeric(df['OVR'], errors='coerce').fillna(75)
            # If ratings are in normalized scale (-3 to +3), convert to 0-100
            if df['OVR'].max() <= 5 and df['OVR'].min() >= -5:
                print("🔧 Converting normalized ratings to 0-100 scale")
                # Convert -3 to +3 scale to 50-95 scale (more realistic for football ratings)
                df['OVR'] = ((df['OVR'] + 3) / 6) * 45 + 50  # Maps -3→50, +3→95
        
        # Ensure reasonable ranges
        df = df[df['Age'].between(16, 45)]
        df = df[df['market_value'] >= 0]
        
        print(f"🧹 Data cleaned and validated: {len(df)} players")
        return df
    
    def detect_query_type(self, query):
        """Advanced query type detection"""
        query_lower = query.lower()
        
        # Comparison detection (enhanced)
        comparison_patterns = [
            r'\bwho is better\b',           # "who is better X or Y"
            r'\bbetter\b.*\bor\b',          # "better X or Y"
            r'\bvs\b',                      # "X vs Y"
            r'\bversus\b',                  # "X versus Y"
            r'\bcompare\b',                 # "compare X and Y"
            r'\b\w+\s+or\s+\w+\b'          # "mbappe or salah"
        ]
        
        for pattern in comparison_patterns:
            if re.search(pattern, query_lower):
                return "comparison"
        
        # Plural detection (enhanced)
        plural_indicators = [
            r'\bwho are\b',                 # "who are the fastest"
            r'\bshow me\b',                 # "show me the fastest"
            r'\blist\b',                    # "list the fastest"
            r'\bfind\b',                    # "find the fastest"
            r'\bwingers\b',                 # "fastest wingers"
            r'\bstrikers\b',                # "strongest strikers"
            r'\bforwards\b',                # "best forwards"
            r'\bplayers\b',                 # "fastest players"
            r'\btalents\b',                 # "young talents"
            r'\bfinishers\b',               # "best finishers"
            r'\btop \d+\b',                 # "top 5"
            r'\bbest \d+\b',                # "best 10"
            r'\bcheapest \w+s\b',           # "cheapest forwards"
            r'\bfastest \w+s\b',            # "fastest wingers"
            r'\bstrongest \w+s\b'           # "strongest strikers"
        ]
        
        for pattern in plural_indicators:
            if re.search(pattern, query_lower):
                return "plural"
        
        # Singular detection (enhanced)
        singular_indicators = [
            r'\bwho is the\b',              # "who is the fastest"
            r'\bwhat is the\b',             # "what is the best"
            r'\bwhich is the\b',            # "which is the strongest"
            r'\btell me about\b',           # "tell me about X"
            r'\bthe best\b(?!\s+\d+)',      # "the best" but not "the best 5"
            r'\bthe fastest\b(?!\s+\w+s\b)', # "the fastest" but not "the fastest wingers"
            r'\bthe strongest\b(?!\s+\w+s\b)'
        ]
        
        for pattern in singular_indicators:
            if re.search(pattern, query_lower):
                return "singular"
        
        # Default to plural for safety
        return "plural"
    
    def extract_nationality_filter(self, query):
        """Extract nationality filters with better matching"""
        query_lower = query.lower()
        
        nationality_map = {
            'french': ['france', 'fra'],
            'france': ['france', 'fra'],
            'brazilian': ['brazil', 'bra'],
            'brazil': ['brazil', 'bra'],
            'argentinian': ['argentina', 'arg'],
            'argentina': ['argentina', 'arg'],
            'spanish': ['spain', 'esp'],
            'spain': ['spain', 'esp'],
            'english': ['england', 'eng'],
            'england': ['england', 'eng'],
            'german': ['germany', 'ger'],
            'germany': ['germany', 'ger'],
            'italian': ['italy', 'ita'],
            'italy': ['italy', 'ita'],
            'portuguese': ['portugal', 'por'],
            'portugal': ['portugal', 'por'],
            'dutch': ['netherlands', 'ned'],
            'netherlands': ['netherlands', 'ned']
        }
        
        for keyword, country_codes in nationality_map.items():
            if keyword in query_lower:
                return country_codes
        
        return None
    
    def extract_price_threshold(self, query):
        """Extract price thresholds from query"""
        query_lower = query.lower()
        
        patterns = [
            r'under\s*€?(\d+(?:\.\d+)?)',      # "under €10", "under 10"
            r'below\s*€?(\d+(?:\.\d+)?)',      # "below €10"
            r'less than\s*€?(\d+(?:\.\d+)?)',  # "less than €10"
            r'up to\s*€?(\d+(?:\.\d+)?)',      # "up to €10"
            r'maximum\s*€?(\d+(?:\.\d+)?)',    # "maximum €10"
            r'max\s*€?(\d+(?:\.\d+)?)'         # "max €10"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query_lower)
            if match:
                threshold = float(match.group(1))
                print(f"💰 Detected price threshold: €{threshold}M")
                return threshold
        
        return None
    
    def extract_age_threshold(self, query):
        """Extract age thresholds from query"""
        query_lower = query.lower()
        
        patterns = [
            r'under\s*(\d+)',              # "under 25"
            r'below\s*(\d+)',              # "below 23" 
            r'young.*under\s*(\d+)',       # "young players under 23"
            r'(\d+)\s*and under',          # "23 and under"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query_lower)
            if match:
                threshold = int(match.group(1))
                if 18 <= threshold <= 35:
                    print(f"👶 Detected age threshold: under {threshold}")
                    return threshold
        
        # Special keywords
        if 'young' in query_lower and 'talent' in query_lower:
            print(f"👶 Detected 'young talent' keyword: under 25")
            return 25
        
        return None
    
    def extract_players_for_comparison(self, query):
        """Enhanced player name extraction for comparisons"""
        query_lower = query.lower()
        
        # Extended player database with common variations
        player_variations = {
            'mbappe': ['mbappe', 'mbappé', 'kylian'],
            'salah': ['salah', 'mohamed salah', 'mo salah'],
            'haaland': ['haaland', 'erling', 'erling haaland'],
            'messi': ['messi', 'lionel', 'lionel messi'],
            'ronaldo': ['ronaldo', 'cristiano'],
            'neymar': ['neymar', 'neymar jr'],
            'benzema': ['benzema', 'karim'],
            'kane': ['kane', 'harry kane'],
            'lewandowski': ['lewandowski', 'robert'],
            'mbeumo': ['mbeumo', 'bryan mbeumo', 'meumo'],  # Common misspelling
            'luis diaz': ['luis diaz', 'diaz', 'luis díaz'],
            'son': ['son', 'heung-min', 'son heung-min'],
            'sterling': ['sterling', 'raheem'],
            'saka': ['saka', 'bukayo'],
            'foden': ['foden', 'phil'],
            'isak': ['isak', 'alexander isak']
        }
        
        found_players = []
        for main_name, variations in player_variations.items():
            for variation in variations:
                if variation in query_lower:
                    found_players.append(main_name)
                    break  # Don't add duplicates
        
        return found_players
    
    def apply_comprehensive_filtering(self, query):
        """Enhanced filtering with better fallback handling"""
        query_lower = query.lower()
        df = self.df.copy()
        
        print(f"🔍 Query: {query}")
        print(f"📊 Starting with {len(df)} players")
        
        # Handle comparison queries first
        if 'better' in query_lower or 'vs' in query_lower or 'compare' in query_lower:
            comparison_players = self.extract_players_for_comparison(query)
            if comparison_players:
                # Create pattern for all comparison players
                patterns = []
                for player in comparison_players:
                    if player == 'luis diaz':
                        patterns.append(r'luis.*d[ií]az')
                    elif player == 'mbeumo':
                        patterns.append(r'mb[eu]umo')
                    else:
                        patterns.append(player.replace(' ', '.*'))
                
                combined_pattern = '|'.join(patterns)
                matched_df = df[df['Name'].str.lower().str.contains(combined_pattern, case=False, na=False)]
                print(f"🔍 After comparison filter ({comparison_players}): {len(matched_df)} players")
                
                if matched_df.empty:
                    print("⚠️ No exact matches found for comparison players")
                    return pd.DataFrame(), pd.DataFrame()
                
                return matched_df.head(10), pd.DataFrame()  # No suggestions for comparisons
        
        # Extract filters
        nationality_codes = self.extract_nationality_filter(query)
        price_threshold = self.extract_price_threshold(query)
        age_threshold = self.extract_age_threshold(query)
        
        # Store original dataframe for fallback
        original_df = df.copy()
        
        # Apply nationality filtering FIRST (most restrictive)
        if nationality_codes:
            nationality_pattern = '|'.join(nationality_codes)
            df = df[df['Nation'].str.lower().str.contains(nationality_pattern, case=False, na=False)]
            print(f"🌍 After nationality filter ({nationality_codes}): {len(df)} players")
        
        # Store after nationality filter for fallback
        after_nationality_df = df.copy()
        
        # Apply age filtering
        if age_threshold:
            df = df[df['Age'] < age_threshold]
            print(f"👶 After age filter (<{age_threshold}): {len(df)} players")
        
        # Apply league filtering
        league_filters = {
            'premier league': 'Premier League',
            'premier': 'Premier League',
            'la liga': 'La Liga',
            'laliga': 'La Liga',
            'serie a': 'Serie A',
            'bundesliga': 'Bundesliga',
            'ligue 1': 'Ligue 1'
        }
        
        for keyword, league_name in league_filters.items():
            if keyword in query_lower:
                df = df[df['League'].str.contains(league_name, case=False, na=False)]
                print(f"🏆 After {league_name} filter: {len(df)} players")
                break
        
        # Apply position filtering
        if 'winger' in query_lower:
            df = df[df['Position'].str.contains('LW|RW', case=False, na=False)]
            print(f"🏃 After winger filter: {len(df)} players")
        elif 'striker' in query_lower:
            df = df[df['Position'].str.contains('ST|CF', case=False, na=False)]
            print(f"🏃 After striker filter: {len(df)} players")
        elif 'forward' in query_lower:
            df = df[df['Position'].str.contains('ST|CF|LW|RW', case=False, na=False)]
            print(f"🏃 After forward filter: {len(df)} players")
        elif 'finisher' in query_lower:
            # Finishers are typically strikers and attacking wingers
            df = df[df['Position'].str.contains('ST|CF|LW|RW', case=False, na=False)]
            print(f"🎯 After finisher position filter: {len(df)} players")
        
        # ENHANCED FALLBACK LOGIC
        main_results = df.copy()
        suggestions = pd.DataFrame()
        
        # If we have strict criteria but no results, create fallback suggestions
        if main_results.empty:
            print("⚠️ No players found with strict criteria, creating fallback suggestions...")
            
            if nationality_codes:
                # Fallback 1: Same nationality, relax other criteria
                fallback_df = after_nationality_df.copy()
                if age_threshold:
                    # Extend age range by 3 years
                    fallback_df = fallback_df[fallback_df['Age'] < age_threshold + 3]
                
                if not fallback_df.empty:
                    suggestions = fallback_df.head(3)
                    print(f"💡 Fallback suggestions (same nationality, relaxed criteria): {len(suggestions)} players")
                
                # Fallback 2: If still empty, remove nationality filter but keep other criteria
                if suggestions.empty:
                    fallback_df = original_df.copy()
                    if age_threshold:
                        fallback_df = fallback_df[fallback_df['Age'] < age_threshold + 2]
                    # Apply position filter if it was specified
                    if 'finisher' in query_lower:
                        fallback_df = fallback_df[fallback_df['Position'].str.contains('ST|CF|LW|RW', case=False, na=False)]
                    
                    suggestions = fallback_df.head(3)
                    print(f"💡 Broad fallback suggestions: {len(suggestions)} players")
        
        # Apply price filtering with suggestions
        if price_threshold:
            if not main_results.empty:
                # Main results: strictly under threshold
                strict_results = main_results[main_results['market_value'] <= price_threshold]
                
                # Suggestions: slightly over threshold (up to 1.5x)
                suggestion_threshold = price_threshold * 1.5
                over_budget = main_results[
                    (main_results['market_value'] > price_threshold) & 
                    (main_results['market_value'] <= suggestion_threshold)
                ].head(2)
                
                main_results = strict_results
                if not over_budget.empty:
                    suggestions = pd.concat([suggestions, over_budget]).drop_duplicates().head(3)
                
                print(f"💰 After price filter: Main={len(main_results)}, Suggestions={len(suggestions)}")
        
        # Apply sorting based on query intent
        if 'fastest' in query_lower and 'lowest' in query_lower and 'market value' in query_lower:
            # Special case: fast and cheap
            if 'PACE' in main_results.columns and not main_results.empty:
                pace_threshold = main_results['PACE'].quantile(0.6)  # Top 40% by pace
                fast_players = main_results[main_results['PACE'] >= pace_threshold]
                main_results = fast_players.nsmallest(15, 'market_value')
                print(f"⚡💰 Fast + cheap filter: {len(main_results)} players")
        elif 'fastest' in query_lower:
            main_results = self.sort_with_fallback(main_results, 'PACE', ascending=False)
            suggestions = self.sort_with_fallback(suggestions, 'PACE', ascending=False)
        elif 'strongest' in query_lower:
            main_results = self.sort_with_fallback(main_results, 'PHYSICAL', ascending=False)
            suggestions = self.sort_with_fallback(suggestions, 'PHYSICAL', ascending=False)
        elif 'finisher' in query_lower or 'finishing' in query_lower:
            main_results = self.sort_with_fallback(main_results, 'SHOOTING', ascending=False)
            suggestions = self.sort_with_fallback(suggestions, 'SHOOTING', ascending=False)
        elif 'cheapest' in query_lower:
            main_results = main_results.nsmallest(15, 'market_value')
            suggestions = suggestions.nsmallest(3, 'market_value')
        elif 'talent' in query_lower or 'potential' in query_lower:
            main_results = self.sort_with_fallback(main_results, 'OVR', ascending=False)
            suggestions = self.sort_with_fallback(suggestions, 'OVR', ascending=False)
        else:
            # Default sort by overall rating
            main_results = self.sort_with_fallback(main_results, 'OVR', ascending=False)
            suggestions = self.sort_with_fallback(suggestions, 'OVR', ascending=False)
        
        return main_results.head(15), suggestions.head(3)
    
    def sort_with_fallback(self, df, column, ascending=False):
        """Sort with fallback to OVR if column doesn't exist"""
        if df.empty:
            return df
        
        if column in df.columns:
            return df.nlargest(15, column) if not ascending else df.nsmallest(15, column)
        else:
            print(f"⚠️ Column {column} not found, falling back to OVR")
            return df.nlargest(15, 'OVR')
    
    def convert_stats_to_text(self, player):
        """Enhanced stat conversion with better descriptions"""
        descriptions = {}
        
        stat_columns = ['PACE', 'SHOOTING', 'PASSING', 'DRIBBLING', 'PHYSICAL']
        
        for stat in stat_columns:
            if stat in player.index:
                try:
                    val = float(player[stat])
                    
                    # Enhanced descriptions based on stat type
                    if stat == 'PACE':
                        if val >= 2.0: descriptions['pace'] = "lightning fast pace that terrorizes defenders"
                        elif val >= 1.0: descriptions['pace'] = "very fast with explosive acceleration"
                        elif val >= 0.0: descriptions['pace'] = "good pace and mobility"
                        else: descriptions['pace'] = "average pace"
                    elif stat == 'SHOOTING':
                        if val >= 2.0: descriptions['shooting'] = "world-class finishing ability"
                        elif val >= 1.0: descriptions['shooting'] = "excellent shooting and clinical finishing"
                        elif val >= 0.0: descriptions['shooting'] = "good finishing skills"
                        else: descriptions['shooting'] = "average shooting"
                    elif stat == 'PHYSICAL':
                        if val >= 2.0: descriptions['physical'] = "exceptional physical presence and strength"
                        elif val >= 1.0: descriptions['physical'] = "very strong and robust"
                        elif val >= 0.0: descriptions['physical'] = "good physicality"
                        else: descriptions['physical'] = "average strength"
                    elif stat == 'PASSING':
                        if val >= 2.0: descriptions['passing'] = "exceptional vision and passing range"
                        elif val >= 1.0: descriptions['passing'] = "excellent passing and distribution"
                        elif val >= 0.0: descriptions['passing'] = "good passing ability"
                        else: descriptions['passing'] = "average passing"
                    elif stat == 'DRIBBLING':
                        if val >= 2.0: descriptions['dribbling'] = "exceptional dribbling and ball control"
                        elif val >= 1.0: descriptions['dribbling'] = "excellent dribbling skills"
                        elif val >= 0.0: descriptions['dribbling'] = "good ball control"
                        else: descriptions['dribbling'] = "average dribbling"
                except:
                    descriptions[stat.lower()] = "unknown"
        
        return descriptions
    
    def create_comparison_table(self, players_df):
        """Create a formatted comparison table for multiple players"""
        if players_df.empty:
            return "No players to compare."
        
        comparison = "\n**COMPARISON TABLE:**\n"
        comparison += "| Player | Age | Value | Pace | Shooting | Physical | Overall |\n"
        comparison += "|--------|-----|-------|------|----------|----------|---------|\n"
        
        for _, player in players_df.iterrows():
            stats = self.convert_stats_to_text(player)
            
            pace_desc = stats.get('pace', 'unknown')[:12] + "..." if len(stats.get('pace', '')) > 12 else stats.get('pace', 'unknown')
            shooting_desc = stats.get('shooting', 'unknown')[:12] + "..." if len(stats.get('shooting', '')) > 12 else stats.get('shooting', 'unknown')
            physical_desc = stats.get('physical', 'unknown')[:12] + "..." if len(stats.get('physical', '')) > 12 else stats.get('physical', 'unknown')
            
            comparison += f"| {player['Name'][:15]} | {int(player.get('Age', 25))} | €{player.get('market_value', 0):.1f}M | {pace_desc} | {shooting_desc} | {physical_desc} | {player.get('OVR', 0):.1f}/100 |\n"
        
        return comparison
    
    async def call_enhanced_llm(self, context, suggestions_context, comparison_table, query, query_type, has_price_threshold, has_nationality_filter):
        """Enhanced LLM call with advanced prompting"""
        
        if query_type == "singular":
            prompt = f"""You are a professional football scout. Based on the data below, identify and analyze THE SINGLE BEST player that matches the user's query.

CRITICAL RULES:
- Focus on ONE player only (the top player in the main results)
- Use the qualitative descriptions provided (never show raw numbers for pace/shooting/physical/passing/dribbling)
- Show exact numbers ONLY for: Age, Market Value (€M), Overall Rating (/100)
- Be detailed and professional like a real scout report
- If suggestions are provided, mention them at the end

Main Results:
{context}

{suggestions_context if suggestions_context else ""}

Question: {query}

Professional Scout Analysis:"""

        elif query_type == "comparison":
            prompt = f"""You are a professional football scout. Compare ALL the players provided in the data below.

CRITICAL RULES:
- Compare each player's strengths and weaknesses point by point
- Use the qualitative descriptions provided (never show raw numbers for pace/shooting/physical/passing/dribbling)
- Show exact numbers ONLY for: Age, Market Value (€M), Overall Rating (/100)
- Use the comparison table provided to structure your analysis
- Give a clear final recommendation with reasoning

{comparison_table}

Detailed Player Data:
{context}

Question: {query}

Professional Comparison Analysis:"""

        else:  # plural
            no_matches_context = ""
            if has_nationality_filter and "No players found with strict criteria" in suggestions_context:
                no_matches_context = f"""
IMPORTANT: No players were found matching the exact nationality criteria. The suggestions below are alternative options that might interest the user.
"""
            
            prompt = f"""You are a professional football scout. Analyze the TOP players from the data below that match the user's query.

CRITICAL RULES:
- Present MULTIPLE players in ranked order (start with #1, #2, #3, etc.)
- Use the qualitative descriptions provided (never show raw numbers for pace/shooting/physical/passing/dribbling)
- Show exact numbers ONLY for: Age, Market Value (€M), Overall Rating (/100)
- Be detailed for each player with tactical insights
- If no exact matches were found, clearly explain this and present alternatives
{f"- Include suggestions section at the end labeled 'ALTERNATIVE OPTIONS'" if suggestions_context else ""}

{no_matches_context}

Main Results:
{context}

{suggestions_context if suggestions_context else ""}

Question: {query}

Professional Scout Analysis:"""

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5:7b",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,  # Lower for more consistent responses
                        "top_p": 0.85,
                        "top_k": 35,
                        "num_predict": 900,  # Increased for comprehensive responses
                        "stop": []
                    }
                },
                timeout=75
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response generated").strip()
            else:
                return f"Error: LLM returned status {response.status_code}"
                
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
    
    async def process_query(self, query: str) -> dict:
        """Enhanced query processing with production-grade features"""
        print(f"🔍 Processing: {query}")
        
        # Detect query type
        query_type = self.detect_query_type(query)
        print(f"📝 Type: {query_type}")
        
        # Apply comprehensive filtering
        main_results, suggestions = self.apply_comprehensive_filtering(query)
        
        # Enhanced fallback handling
        if main_results.empty:
            print("❌ No players found in main results")
            
            if not suggestions.empty:
                print("💡 Using suggestions as main results")
                main_results = suggestions
                suggestions = pd.DataFrame()
            else:
                # Create helpful fallback message
                nationality_codes = self.extract_nationality_filter(query)
                age_threshold = self.extract_age_threshold(query)
                
                fallback_msg = "I couldn't find any players matching your specific criteria. "
                if nationality_codes:
                    fallback_msg += f"There might not be any players from {nationality_codes[0]} "
                if age_threshold:
                    fallback_msg += f"under {age_threshold} years old "
                fallback_msg += "in our database. Try broadening your search criteria."
                
                return {
                    "answer": fallback_msg,
                    "sources": []
                }
        
        print(f"✅ Found {len(main_results)} main results, {len(suggestions)} suggestions")
        
        # Create rich context
        context = ""
        sources = []
        
        max_players = 1 if query_type == "singular" else min(8, len(main_results))
        
        for idx, (_, player) in enumerate(main_results.head(max_players).iterrows()):
            stats = self.convert_stats_to_text(player)
            
            context += f"Player {idx + 1}: {player['Name']}\n"
            context += f"- Team: {player.get('Team', 'Unknown')} ({player.get('League', 'Unknown')})\n"
            context += f"- Age: {int(player.get('Age', 25))} years\n"
            context += f"- Position: {player.get('Position', 'Unknown')}\n"
            context += f"- Nation: {player.get('Nation', 'Unknown')}\n"
            context += f"- Market Value: €{player.get('market_value', 0):.1f}M\n"
            context += f"- Overall Rating: {player.get('OVR', 75):.1f}/100\n"
            
            for stat_name, description in stats.items():
                context += f"- {stat_name.title()}: {description}\n"
            
            if 'play style' in player.index and pd.notna(player['play style']):
                context += f"- Play Style: {player['play style']}\n"
            
            context += f"\n"
            sources.append(player['Name'])
        
        # Create suggestions context
        suggestions_context = ""
        if not suggestions.empty:
            has_price_threshold = self.extract_price_threshold(query) is not None
            has_nationality_filter = self.extract_nationality_filter(query) is not None
            
            if has_price_threshold:
                suggestions_context += "\n\nSLIGHTLY OVER BUDGET OPTIONS:\n"
            elif has_nationality_filter:
                suggestions_context += "\n\nALTERNATIVE OPTIONS (different criteria):\n"
            else:
                suggestions_context += "\n\nADDITIONAL SUGGESTIONS:\n"
            
            for idx, (_, player) in enumerate(suggestions.iterrows()):
                stats = self.convert_stats_to_text(player)
                
                suggestions_context += f"Option {idx + 1}: {player['Name']}\n"
                suggestions_context += f"- Team: {player.get('Team', 'Unknown')} ({player.get('League', 'Unknown')})\n"
                suggestions_context += f"- Age: {int(player.get('Age', 25))} years\n"
                suggestions_context += f"- Position: {player.get('Position', 'Unknown')}\n"
                suggestions_context += f"- Nation: {player.get('Nation', 'Unknown')}\n"
                suggestions_context += f"- Market Value: €{player.get('market_value', 0):.1f}M\n"
                suggestions_context += f"- Overall Rating: {player.get('OVR', 75):.1f}/100\n"
                
                for stat_name, description in stats.items():
                    suggestions_context += f"- {stat_name.title()}: {description}\n"
                
                suggestions_context += f"\n"
        
        # Create comparison table for comparison queries
        comparison_table = ""
        if query_type == "comparison":
            comparison_table = self.create_comparison_table(main_results)
        
        # Call enhanced LLM
        response = await self.call_enhanced_llm(
            context, 
            suggestions_context, 
            comparison_table,
            query, 
            query_type, 
            self.extract_price_threshold(query) is not None,
            self.extract_nationality_filter(query) is not None
        )
        
        return {
            "answer": response,
            "sources": sources[:5]
        }
