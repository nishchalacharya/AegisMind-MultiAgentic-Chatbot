# rag/loader.py
"""
Document Loader - Load and parse PDF and DOCX files
Uses LangChain for easy document handling
"""

from typing import List
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config.settings import get_settings

class DocumentLoader:
    """
    Load documents and split them into chunks
    Supports: PDF, DOCX
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.settings.chunk_size,
            chunk_overlap=self.settings.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_document(self, file_path: str) -> List[Document]:
        """
        Load a single document and split into chunks
        
        Args:
            file_path: Path to PDF or DOCX file
        
        Returns:
            List of Document objects with text chunks
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Choose loader based on file extension
        if file_path.suffix.lower() == '.pdf':
            loader = PyPDFLoader(str(file_path))
        elif file_path.suffix.lower() in ['.docx', '.doc']:
            loader = Docx2txtLoader(str(file_path))
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        
        # Load document
        print(f"📄 Loading document: {file_path.name}")
        documents = loader.load()
        
        # Split into chunks
        print(f"✂️ Splitting into chunks (size={self.settings.chunk_size}, overlap={self.settings.chunk_overlap})")
        chunks = self.text_splitter.split_documents(documents)
        
        print(f"✅ Created {len(chunks)} chunks from {file_path.name}")
        
        # Add metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                "source": str(file_path),
                "chunk_id": i,
                "total_chunks": len(chunks)
            })
        
        return chunks
    
    def load_multiple_documents(self, file_paths: List[str]) -> List[Document]:
        """
        Load multiple documents
        
        Args:
            file_paths: List of file paths
        
        Returns:
            Combined list of all document chunks
        """
        all_chunks = []
        
        for file_path in file_paths:
            try:
                chunks = self.load_document(file_path)
                all_chunks.extend(chunks)
            except Exception as e:
                print(f"❌ Error loading {file_path}: {e}")
        
        print(f"\n📊 Total: {len(all_chunks)} chunks from {len(file_paths)} documents")
        return all_chunks


# Test the loader
if __name__ == "__main__":
    loader = DocumentLoader()
    print("✅ DocumentLoader initialized successfully!")