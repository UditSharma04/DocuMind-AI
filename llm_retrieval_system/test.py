# test_pinecone.py
import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

def test_pinecone_connection():
    try:
        # Initialize Pinecone (Updated SDK v3.0+ syntax)
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        
        # List existing indexes (should be empty initially)
        indexes = pc.list_indexes()
        print("✅ Pinecone connection successful!")
        print(f"Current indexes: {indexes}")
        
        return True
    except Exception as e:
        print(f"❌ Pinecone connection failed: {e}")
        return False

if __name__ == "__main__":
    test_pinecone_connection()
