import sys
import requests
import json
from pathlib import Path

# Add project to path
sys.path.append(str(Path(__file__).parent.parent))

def test_document_upload():
    """Test document upload functionality"""
    base_url = "http://localhost:8000"
    
    # Create a test text file
    test_file_content = """
    This is a test document for the LLM Query Retrieval System.
    
    The system should be able to process this document, extract its text,
    and split it into appropriate chunks for embedding and semantic search.
    
    This paragraph contains information about artificial intelligence and
    natural language processing capabilities that should be searchable.
    
    The final paragraph tests the chunking algorithm's ability to handle
    longer text passages and maintain context across chunk boundaries.
    """
    
    test_file_path = Path("test_document.txt")
    with open(test_file_path, "w") as f:
        f.write(test_file_content)
    
    try:
        # Test file upload
        with open(test_file_path, "rb") as f:
            files = {"file": ("test_document.txt", f, "text/plain")}
            response = requests.post(f"{base_url}/api/v1/documents/upload", files=files)
        
        print("Upload Response:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            document_id = response.json()["document_id"]
            
            # Test document retrieval
            response = requests.get(f"{base_url}/api/v1/documents/{document_id}")
            print("\nDocument Details:")
            print(json.dumps(response.json(), indent=2))
            
            # Test document list
            response = requests.get(f"{base_url}/api/v1/documents/")
            print("\nAll Documents:")
            print(json.dumps(response.json(), indent=2))
        
    finally:
        # Clean up test file
        if test_file_path.exists():
            test_file_path.unlink()

if __name__ == "__main__":
    test_document_upload()
