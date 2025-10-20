import os, logging
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()
logger = logging.getLogger(__name__)

# Initialize Pinecone variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "hackathon-document-index")
DIM = int(os.getenv("EMBEDDING_DIMENSION", 1536))

# Initialize Pinecone client only if API key is available
pc = None
index = None

if PINECONE_API_KEY and PINECONE_API_KEY != "your_pinecone_api_key_here":
    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        
        # Create index if it doesn't exist (Updated SDK syntax)
        existing_indexes = [idx.name for idx in pc.list_indexes()]
        if INDEX_NAME not in existing_indexes:
            pc.create_index(
                name=INDEX_NAME,
                dimension=DIM,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-west-2"  # Best for India
                )
            )
            logger.info(f"Created Pinecone index: {INDEX_NAME}")
        
        index = pc.Index(INDEX_NAME)
        logger.info("Pinecone client initialized successfully")
    except Exception as e:
        logger.warning(f"Failed to initialize Pinecone: {e}")
        logger.info("Pinecone functionality will be disabled")
else:
    logger.info("Pinecone API key not configured - Pinecone functionality disabled")

def upsert_vectors(vectors):
    """vectors = [{'id': 'chunk-1', 'values': [...], 'metadata': {...}}, ...]"""
    if index is None:
        logger.warning("Pinecone not initialized - cannot upsert vectors")
        return False
    
    try:
        index.upsert(vectors)
        return True
    except Exception as e:
        logger.error(f"Failed to upsert vectors: {e}")
        return False

def query_vector(vector, top_k=10, metadata_filter=None):
    if index is None:
        logger.warning("Pinecone not initialized - cannot query vectors")
        return {"matches": []}
    
    try:
        return index.query(vector=vector, top_k=top_k, filter=metadata_filter or {}, include_metadata=True)
    except Exception as e:
        logger.error(f"Failed to query vectors: {e}")
        return {"matches": []}
