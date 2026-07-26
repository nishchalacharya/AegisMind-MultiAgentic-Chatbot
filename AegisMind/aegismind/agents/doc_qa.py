# agents/doc_qa.py
"""
Document Q&A Agent - Answer questions using RAG
Retrieval-Augmented Generation
"""

import traceback
from typing import List 
from pathlib import Path
from urllib import response
from orchestration import state
from urllib import response 
from rag.loader import DocumentLoader
from rag.embedder import Embedder
from rag.retriever import VectorStore
from config.settings import get_settings
from services.groq_client import GroqClient
from orchestration.state import AgentState

class DocQAAgent:
    """
        Document Q&A agent using RAG pipeline:
        1. Load documents
        2. Store in vector database
        3. Retrieve relevant chunks
        4. Generate answer with context
    """
    def __init__(self):
        self.settings=get_settings()
        self.loader=DocumentLoader()
        self.vector_store=VectorStore()
        self.llm = GroqClient()
        
        #try to load existing vector store
        self._load_or_create_vector_store()
        
        
    def _load_or_create_vector_store(self):
        """Load existing vector store or create new one"""
        store_path = self.settings.embeddings_dir / "vector_store"
        try:
            if store_path.exists():
                self.vector_store.load(str(store_path))
                print(f"Loaded existing vector store from {store_path}...")
            else:
                print(f" No existing vector store, will create on first document upload")
        except Exception as e:
            print(f"Could not load vector store: {e}")  
    
    def upload_documents(self,file_paths:List[str]):
        """
            Upload and process documents
            
            Args:
                file_paths: List of document file paths
        """
        print(f"\n Uploading {len(file_paths)} documents...")
        
        # Load and chunk  documents 
        chunks=self.loader.load_multiple_documents(file_paths)
        
        if not chunks:
            print("No chunks created from documents")
            return 
        
        # Add to vector store
        self.vector_store.add_documents(chunks)
        
        # Save vector store 
        store_path =self.settings.embeddings_dir / "vector_store"
        self.vector_store.save(str(store_path))
        
        print(f" Documents uploaded and indexed successfully")
        
        
    def execute(self,state: AgentState) -> AgentState :
        """
        Answer question using RAG
        
        Args:
            state: Current agent state with user question
        
        Returns:
            Updated state with answer
        """ 
        query=state["user_message"]
        
        print(f"\n Document Q&A Agent")
        print(f"User query:{query}")
        
        # check if we have documents 
        if len(self.vector_store.documents)==0:
            state["final_response"]=(
                "No documents uploaded yet."
                "Please upload documents first using the upload command."
                
            )
            return state 
        
        # Retrieve relevant chunks 
        results=self.vector_store.search(query,k=self.settings.retrieval_k)
        
        if not results:
            state["final_response"]=(
                " I couldn't find any relevant information in the documents."
                "Try rephrasing the question or uploading more documents."
            )
            return state 
        
        # Build context from retrieved chunks 
        context= "\n\n".join([f"[Source:{doc.metadata.get('source','unknown')}]\n {doc.page_content}" for doc,score in results])
        
        # Generate answer using LLM with context 
        system_prompt="""
        
        You are helpful assistant that answers questions based on provided document context.
        
        Instructions:
        - Answer the questions using only the information from the provided context.
        - If the context doesn't contain enough information ,say so clearly.
        - Be consise but complete.
        - Cite which source you are referencing when possible.
        - If you are not sure, say you are not sure rather than making up an answer.
        
        Context from documents:
        {context}
        
        """
        messages =[
            {
                "role":"user",
             "content":query}
        ]
        
        # After building the context, add debug:
        print(f"\n📝 Context length: {len(context)} characters")
        print(f"📝 Context preview: {context[:200]}...")

        # Before the LLM call:
        print(f"\n🤖 Calling Groq LLM...")
                
        try:
            response = self.llm.generate(
                messages=messages,
                system_prompt=system_prompt.format(context=context),
                temperature =0.3,
                max_tokens=500
                
            )
            print(f"✅ Got response from LLM")
            print(f"📝 Response preview: {response[:100]}...")
        
        except Exception as e:
                print(f"❌ Error calling LLM: {e}")
                import traceback
                traceback.print_exc()
                response = f"Error generating answer: {e}"
            
        # Store retrieved documents in state
        state["retrieved_documents"]=[
            {
                "content":doc.page_content,
                "metadata":doc.metadata,
                "score":score 
                
            }for doc,score in results
        ]
        state["final_response"]= response
        
        return state 
    
    
    

# Test the agent
if __name__ == "__main__":
    agent = DocQAAgent()
    
    # Create test document
    test_file = Path("data/documents/test_doc_qa.txt")
    test_file.parent.mkdir(parents=True, exist_ok=True)
    
    test_file.write_text("""
    Project AegisMind Documentation
    
    AegisMind is a multi-agent AI system built with LangGraph.
    It uses Groq for fast LLM inference and FAISS for vector search.
    
    The system has several agents:
    - Planner Agent: Routes user requests to appropriate agents
    - Document Q&A Agent: Answers questions about uploaded documents
    - Memory Agent: Stores and retrieves user information
    - General Agent: Handles general conversation
    
    The RAG pipeline uses:
    1. Document loading with LangChain
    2. Text chunking for better retrieval
    3. Sentence Transformers for embeddings
    4. FAISS for fast similarity search
    5. Groq LLM for answer generation
    
    All components are free and run locally where possible.
    """)
    
    # Upload document
    agent.upload_documents([str(test_file)])
    
    # Create test state
    test_state = {
        "user_message": "What agents does AegisMind have?",
        "user_id": "test",
        "messages": [],
        "short_term_memory": [],
        "intent": None,
        "next_agent": None,
        "current_response": "",
        "final_response": "",
        "retrieved_documents": [],
        "memory_updates": [],
        "tool_calls": [],
        "tool_results": [],
        "iteration_count": 0,
        "error": None
    }
    
    # After the execute line, add:
result = agent.execute(test_state)

print("\n" + "="*50)
print("📄 ANSWER:")
print("="*50)
print(result["final_response"])

# Add debug info
print("\n" + "="*50)
print("🔍 DEBUG INFO:")
print("="*50)
print(f"Retrieved {len(result['retrieved_documents'])} documents")
if result['retrieved_documents']:
    print(f"First chunk preview: {result['retrieved_documents'][0]['content'][:100]}...")
            
        
        
                          
                        