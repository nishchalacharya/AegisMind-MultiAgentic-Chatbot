# project_setup.py
"""
AegisMind - Project Structure Generator
Run this to create the complete folder structure
"""

import os
from pathlib import Path

def create_project_structure():
    """Creates the complete AegisMind directory structure"""
    
    structure = {
        "aegismind": {
            "agents": [
                "__init__.py",
                "planner.py",
                "doc_qa.py", 
                "memory.py",
                "voice.py",
                "mcp_agent.py"
            ],
            "orchestration": [
                "__init__.py",
                "graph.py",
                "state.py"
            ],
            "rag": [
                "__init__.py",
                "loader.py",
                "embedder.py",
                "retriever.py"
            ],
            "memory": [
                "__init__.py",
                "short_term.py",
                "long_term.py"
            ],
            "services": [
                "__init__.py",
                "groq_client.py"
            ],
            "ui": [
                "__init__.py",
                "cli.py",
                "web.py"
            ],
            "data": [
                "documents/.gitkeep",
                "embeddings/.gitkeep"
            ],
            "config": [
                "__init__.py",
                "settings.py"
            ]
        }
    }
    
    # Create root directory
    root = Path("aegismind")
    root.mkdir(exist_ok=True)
    
    # Create all subdirectories and files
    for parent, items in structure.items():
        for key, value in items.items():
            dir_path = root / key
            dir_path.mkdir(exist_ok=True)
            
            for file in value:
                if "/" in file:
                    # Handle nested paths like "documents/.gitkeep"
                    file_path = dir_path / file
                    file_path.parent.mkdir(exist_ok=True)
                    file_path.touch()
                else:
                    (dir_path / file).touch()
    
    # Create root level files
    (root / "__init__.py").touch()
    (root / "main.py").touch()
    
    # Create project root files
    Path("requirements.txt").touch()
    # Path(".env.example").touch()
    # Path(".gitignore").touch()
    # Path("README.md").touch()
    
    print("✅ AegisMind project structure created successfully!")
    print("\nNext steps:")
    print("1. cd aegismind")
    print("2. Create virtual environment: python -m venv venv")
    print("3. Activate: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)")
    print("4. Install dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    create_project_structure()