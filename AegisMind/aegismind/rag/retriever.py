# rag/retriever.py
"""
Retriever - Store and search document embeddings using FAISS
FAISS = Facebook AI Similarity Search (free, fast, local)
"""

from typing import List,Tuple 
import faiss 
import numpy as np 
from pathlib import Path 
import pickle 
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader 
from rag.embedder import Embedder 
from config.settings import get_settings 


class VectorStore:
    """
    Store and retrieve document chunks using FAISS vector search
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.embedder = Embedder()
        self.dimension=self.embedder.model.get_sentence_embedding_dimension()
        
        # Initialize FAISS index
        # Using IndexFlatL2 (exact search, good for < 1M vectors)
        self.index=faiss.IndexFlatL2(self.dimension)
        
        # store original documents 
        self.documents : List[Document]=[]
        
        print(f" VectorStore initialized (dimension={self.dimension})")
        
    def add_documents(self,documents:List[Document]):
        """
            Add documents to the vector store
            
            Args:
                documents: List of Document objects with text
        """
        if not documents:
            print("No documents to add ")
            return 
        
        print(f"\n Adding {len(documents)} documents to vector store...")    

        # Extract text from documents 
        texts = [doc.page_content for doc in documents]
        
        # Generate embeddings 
        embeddings =self.embedder.embed_texts(texts)
        
        # Add to FAISS index 
        self.index.add(embeddings.astype('float32'))
        
        # store documents 
        self.documents.extend(documents)
        
        print(f" Added {len(documents)} documents")
        print(f"   Total documents in store: {len(self.documents)}")
        
        
    def search(self,query:str,k:int=None)-> List[Tuple[Document,float]]:
        """
            Search for similar documents
            
            Args:
                query: Search query text
                k: Number of results to return (default from settings)
            
            Returns:
                List of (document, similarity_score) tuples
        """
        if k is None:
            k=self.settings.retrieval_k
            
        if len(self.documents)==0:
            print("No documents in store to search")
            return []
        
        # Limit k to available documents
        k=min(k,len(self.documents))
        
        print(f" Searching for: '{query}' (top {k} results)")
        
        # Generate query embedding 
        query_embedding =self.embedder.embed_text(query)
        query_embedding= query_embedding.reshape(1,-1).astype('float32')
        
        # Search in  FAISS
        distances,indices =self.index.search(query_embedding,k)
        
        # Prepare results 
        results = []
        for i,(distance,idx) in enumerate(zip(distances[0],indices[0])):
            doc=self.documents[idx]
            # Convert L2 distance to similarity score (lower is better) 
            similarity = 1/(1+distance)  # simple conversion to (0,1] range
            results.append((doc,float(similarity)))
            
            print(f"   {i+1}. Score: {similarity:.3f} | Source: {doc.metadata.get('source', 'unknown')}")
            
            return results 
            
    def save(self,path:str):
        """
            Save vector store to disk
            
            Args:
                path: Directory path to save to
        """        
        save_path=Path(path)
        save_path.mkdir(parents=True,exist_ok=True)
        
        # Save FAISS index 
        index_path = save_path /"faiss.index"
        faiss.write_index(self.index,str(index_path))
        
        # save documents 
        docs_path =save_path/"documents.pkl"
        with open(docs_path,'wb') as f:
            pickle.dumb(self.documents,f)
        
        print(f"💾 Saved vector store to {save_path}")            
            
    
    def load(self,path:str):
        """
            Load vector store from disk
            
            Args:
                path: Directory path to load from
        """   
        load_path=Path(path)
        
        if not load_path.exists():
            raise FileNotFoundError(f"Vector store not found at {load_path}")
        
        #Load FAISS index 
        index_path =load_path /"faiss.index"
        self.index =faiss.read_index(str(index_path))
        
        # Load documents 
        docs_path = load_path/ "documents.pkl" 
        with open(docs_path,'rb') as f:
            self.documents =pickle.load(f)
        
        print(f" Loaded vector store from {load_path}")
        print(f" Total documents: {len(self.documents)}")   
        
    
    def clear(self):
        """Clear all documents from the store"""
        self.index.reset()
        self.documents =[]
        print(" Cleared vector store")    
        
        
        
# Test the retriever
if __name__ == "__main__":
    from rag.loader import DocumentLoader
    
    # Create sample documents
    loader = DocumentLoader()
    
    # Create test file
    from pathlib import Path
    test_file = Path("data/documents/test_retriever.txt")
    test_file.parent.mkdir(parents=True, exist_ok=True)
    
    test_file.write_text("""
    Artificial Intelligence is transforming the world.
    Machine learning models can learn from data.
    
    Neural networks are inspired by the human brain.
    Deep learning uses multiple layers of neurons.
    
    Natural language processing helps computers understand text.
    Computer vision enables machines to see and interpret images.
    """)
    
    # Load and chunk
    chunks = loader.load_document(str(test_file))
    
    # Create vector store
    vector_store = VectorStore()
    
    # Add documents
    vector_store.add_documents(chunks)
    
    # Test search
    print("\n" + "="*50)
    results = vector_store.search("What is deep learning?", k=2)
    
    print("\n📄 Top result:")
    print(results[0][0].page_content[:200])        
         
            
                
