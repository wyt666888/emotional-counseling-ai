"""
Embeddings module for generating vector representations of text.
Supports both documents and queries for semantic search.
"""

from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np


class EmbeddingModel:
    """Handles text embedding generation using sentence transformers"""
    
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Initialize the embedding model.
        
        Args:
            model_name: Name of the sentence-transformer model to use.
                       Default uses a multilingual model that supports both English and Chinese.
        """
        print(f"Loading embedding model: {model_name}...")
        try:
            self.model = SentenceTransformer(model_name)
            print("✅ Embedding model loaded successfully")
        except Exception as e:
            print(f"⚠️ Failed to load embedding model: {str(e)}")
            self.model = None
    
    def encode(self, texts: Union[str, List[str]], batch_size: int = 32) -> np.ndarray:
        """
        Generate embeddings for text(s).
        
        Args:
            texts: Single text string or list of texts to encode
            batch_size: Number of texts to process at once
            
        Returns:
            numpy array of embeddings
        """
        if self.model is None:
            raise RuntimeError("Embedding model not loaded")
        
        # Convert single string to list for consistent processing
        if isinstance(texts, str):
            texts = [texts]
        
        try:
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=False,
                convert_to_numpy=True
            )
            return embeddings
        except Exception as e:
            print(f"⚠️ Error encoding texts: {str(e)}")
            raise
    
    def encode_query(self, query: str) -> np.ndarray:
        """
        Generate embedding for a query.
        Wrapper around encode() for semantic clarity.
        
        Args:
            query: Query text to encode
            
        Returns:
            numpy array embedding of the query
        """
        return self.encode(query)[0]
    
    def encode_documents(self, documents: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of documents.
        Wrapper around encode() for semantic clarity.
        
        Args:
            documents: List of document texts to encode
            
        Returns:
            numpy array of document embeddings
        """
        return self.encode(documents)
    
    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score between -1 and 1
        """
        # Normalize vectors
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Calculate cosine similarity
        return np.dot(embedding1, embedding2) / (norm1 * norm2)
