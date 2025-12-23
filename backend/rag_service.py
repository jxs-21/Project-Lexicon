from haystack import Document as HaystackDocument
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
import os

class RAGService:
    def __init__(self):
        # Initialize Preprocessing
        self.cleaner = DocumentCleaner()
        self.splitter = DocumentSplitter(split_by="word", split_length=200, split_overlap=20)
        
        # Initialize Local Embeddings (HuggingFace)
        # using BAAI/bge-small-en-v1.5 which is very efficient and good for retrieval (384 dims)
        model_name = "BAAI/bge-small-en-v1.5"
        print(f"Loading local embedding model: {model_name}...")
        self.doc_embedder = SentenceTransformersDocumentEmbedder(model=model_name)
        self.doc_embedder.warm_up()
        
        self.text_embedder = SentenceTransformersTextEmbedder(model=model_name)
        self.text_embedder.warm_up()
        print("Local embedding model loaded.")

    def process_file(self, text: str, filename: str):
        # 1. Create Haystack Doc
        doc = HaystackDocument(content=text, meta={"filename": filename})
        
        # 2. Clean
        cleaned = self.cleaner.run(documents=[doc])
        
        # 3. Split
        split_docs = self.splitter.run(documents=cleaned["documents"])
        
        # 4. Embed (Locally)
        embedded = self.doc_embedder.run(documents=split_docs["documents"])
        return embedded["documents"]

    def embed_query(self, query: str):
        # Embed query locally
        result = self.text_embedder.run(text=query)
        return result["embedding"]
