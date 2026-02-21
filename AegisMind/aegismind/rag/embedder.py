# rag/embedder.py
"""
Embedder - Generate embeddings for text chunks
Uses Sentence Transformers (free, local, CPU-friendly)
"""
from typing import List
from sentence_transformers import SentenceTransformer 
from config.settings import get_settings
import numpy as np 


class Embedder:
    """
        Generate embeddings using Sentence Transformers
        Runs locally on CPU (no API calls needed)
    """
    def __init__(self):
        self.settings=get_settings()
        self.model_name=self.settings.embedding_model
        
        print(f" Loading embedding model: {self.model_name}")
        
        # Load model (cached after first download)
        self.model=SentenceTransformer(self.model_name)
        
        print(f" Embedding model loaded")
        print(f" Dimension: {self.model.get_sentence_embedding_dimension()}")
        
    
    def embed_text(self,text:str) -> np.ndarray:
        """
            Generate embedding for a single text
            
            Args:
                text: Input text
            
            Returns:
                Embedding vector as numpy array
       
        """   
        embedding =self.model.encode(text,convert_to_numpy=True)
        return embedding 
    
    
    def embed_texts(self,texts:List[str])->np.ndarray:
        """
            Generate embeddings for multiple texts (batch processing)
            
            Args:
                texts: List of input texts
            
            Returns:
                Array of embeddings (shape: [num_texts, embedding_dim])
        """
        print(f" Generating embeddings for {len(texts)} texts...")
        
        embeddings =self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
            batch_size=32
        )
        
        print(f"Generated {len(embeddings)} embeddings")
        return embeddings
  
    def get_embedding_dimension(self)-> int:
        
        """Get the dimension of the embedding vectors """
        return self.model.get_sentence_embedding_dimension()
        
        

# Test the embedder
if __name__ == "__main__":
    embedder = Embedder()
    
    # Test single embedding
    text = "This is a sample text for embedding"
    embedding = embedder.embed_text(text)
    print(f"\n📊 Single embedding shape: {embedding.shape}")
    print(f"   First 5 values: {embedding[:5]}")
    
    # Test batch embeddings
    texts = [
        "First document about AI",
        "Second document about machine learning",
        "Third document about neural networks"
    ]
    embeddings = embedder.embed_texts(texts)
    print(f"\n📊 Batch embeddings shape: {embeddings.shape}")