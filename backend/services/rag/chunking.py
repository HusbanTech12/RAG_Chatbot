import hashlib
from typing import List, Dict, Optional
import re


class DocumentChunker:
    """Splits documents into chunks with overlap for better context preservation."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document chunker.

        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(
        self,
        text: str,
        metadata: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Split text into overlapping chunks while preserving sentence boundaries.

        Args:
            text: Text to chunk
            metadata: Optional metadata to attach to each chunk

        Returns:
            List of chunks with metadata
        """
        if not text or not text.strip():
            return []

        # Split into sentences (simple approach)
        sentences = re.split(r'(?<=[.!?])\s+', text)

        chunks = []
        current_chunk = ""
        current_start = 0

        for sentence in sentences:
            # If adding this sentence exceeds chunk_size, save current chunk
            if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                chunk_data = self._create_chunk(
                    current_chunk.strip(),
                    current_start,
                    current_start + len(current_chunk),
                    metadata
                )
                chunks.append(chunk_data)

                # Start new chunk with overlap
                overlap_text = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else current_chunk
                current_chunk = overlap_text + " " + sentence
                current_start = current_start + len(current_chunk) - len(overlap_text) - len(sentence) - 1
            else:
                current_chunk += (" " if current_chunk else "") + sentence

        # Add the last chunk
        if current_chunk.strip():
            chunk_data = self._create_chunk(
                current_chunk.strip(),
                current_start,
                current_start + len(current_chunk),
                metadata
            )
            chunks.append(chunk_data)

        return chunks

    def _create_chunk(
        self,
        text: str,
        start_index: int,
        end_index: int,
        metadata: Optional[Dict]
    ) -> Dict:
        """Create a chunk dictionary with metadata."""
        chunk_id = hashlib.md5(text.encode()).hexdigest()

        chunk = {
            'text': text,
            'chunk_id': chunk_id,
            'start_index': start_index,
            'end_index': end_index,
            'metadata': metadata or {}
        }

        return chunk
