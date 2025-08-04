import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
import os

def setup_football_vectordb():
    print("🏗️ Setting up Football Vector Database...")
    
    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path="./football_vectordb")
    
    # Delete existing collection if it exists
    try:
        client.delete_collection("football_players")
        print("🗑️ Deleted existing collection")
    except:
        pass
    
    # Create collection
    collection = client.create_collection(
        name="football_players",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Load data
    df = pd.read_csv("forwards_clean_with_market_values_updated.csv")
    print(f"📊 Loaded {len(df)} players")
    
    # Initialize embedding model
    print("🤖 Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Create documents for each player
    documents = []
    metadatas = []
    ids = []
    
    for idx, player in df.iterrows():
        # Create rich text description for each player
        doc = f"""
        Name: {player['Name']}
        Age: {player['Age']} years old
        Position: {player['Position']}
        Nation: {player['Nation']}
        League: {player['League']}
        Team: {player['Team']}
        Market Value: €{player['market_value']}M
        Overall Rating: {player['OVR']}
        Pace: {player['PACE']}
        Shooting: {player['SHOOTING']}
        Passing: {player['PASSING']}
        Dribbling: {player['DRIBBLING']}
        Physical: {player['PHYSICAL']}
        Aerial: {player['AERIAL']}
        Mental: {player['MENTAL']}
        Play Style: {player['play style']}
        Preferred Foot: {player['Preferred foot']}
        Height: {player['Height']}cm
        Weight: {player['Weight']}kg
        """
        
        documents.append(doc)
        metadatas.append({
            "name": str(player['Name']),
            "league": str(player['League']),
            "nation": str(player['Nation']),
            "position": str(player['Position']),
            "market_value": float(player['market_value']),
            "overall": float(player['OVR']),
            "age": int(player['Age']),
            "team": str(player['Team'])
        })
        ids.append(f"player_{idx}")
    
    # Generate embeddings and add to collection in batches
    print("🔄 Generating embeddings...")
    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i:i+batch_size]
        batch_metas = metadatas[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]
        
        embeddings = model.encode(batch_docs)
        
        collection.add(
            documents=batch_docs,
            metadatas=batch_metas,
            embeddings=embeddings,
            ids=batch_ids
        )
        print(f"✅ Processed batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")
    
    print(f"🎯 Vector database setup complete! {len(documents)} players indexed.")

if __name__ == "__main__":
    setup_football_vectordb()
