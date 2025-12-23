from haystack import Document as HaystackDocument
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.embedders import OpenAITextEmbedder, OpenAIDocumentEmbedder
# If user wants Anthropic, we might need a different embedder or use a bridge, 
# typically Anthropic is for generation (LLM), not embeddings (OpenAI/Voyage/Cohere used there).
# For now stick to OpenAI for embeddings as it's standard.

import os

class RAGService:
    def __init__(self):
        self.cleaner = DocumentCleaner()
        self.splitter = DocumentSplitter(split_by="word", split_length=200, split_overlap=20)
        # Using OpenAI for now, requiring OPENAI_API_KEY
        self.doc_embedder = OpenAIDocumentEmbedder()
        self.text_embedder = OpenAITextEmbedder()

    def process_file(self, text: str, filename: str):
        # 1. Create Haystack Doc
        doc = HaystackDocument(content=text, meta={"filename": filename})
        
        # 2. Clean
        cleaned = self.cleaner.run(documents=[doc])
        
        # 3. Split
        split_docs = self.splitter.run(documents=cleaned["documents"])
        
        # 4. Embed
        # This requires API key check or mock
        if os.getenv("OPENAI_API_KEY"):
            embedded = self.doc_embedder.run(documents=split_docs["documents"])
            return embedded["documents"]
        else:
            # Fallback or mock if no key (for testing structure)
            print("WARNING: No Open AI Key, skipping embedding")
            return split_docs["documents"]

    def embed_query(self, query: str):
        if os.getenv("OPENAI_API_KEY"):
            result = self.text_embedder.run(text=query)
            return result["embedding"]
        else:
            return [0.1] * 1536 # Mock
