# test_loader.py
"""Test document loader"""

from rag.loader import DocumentLoader

# Test initialization
loader = DocumentLoader()
print(" DocumentLoader initialized")

# Test with a sample text file (create this first)
# Create data/documents/sample.txt with some text
sample_text = """
This is a sample document for testing.
It has multiple paragraphs to demonstrate chunking.

The document loader will split this into smaller pieces.
Each piece will be stored and searchable later.
"""

# Save sample file
from pathlib import Path
Path("data/documents").mkdir(parents=True, exist_ok=True)
with open("data/documents/sample.txt", "w") as f:
    f.write(sample_text * 10)  # Make it longer

print(" Sample document created")