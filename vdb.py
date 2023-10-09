import sklearn
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
import math
from datetime import datetime
from uuid import uuid4 as uuid

class VectorDatabaseAdapter:

    def __init__(self, top_k=1):
        self.TOP_K = top_k
        
        self.retriever = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
        self.client = QdrantClient(host="localhost", port=6333)
        self.transcript_collection_name = "production-transcript-v1"
        self.library_collection_name = "production-library-v1"
        collections = self.client.get_collections()

        #if self.collection_name not in [c.name for c in collections.collections]:
        collections = self.client.get_collections()
        if not self.transcript_collection_name in [x.name for x in collections.collections]:
            self.client.create_collection(
                collection_name=self.transcript_collection_name,
                vectors_config=models.VectorParams(
                    size=384,
                    distance=models.Distance.COSINE
                )
            )

        if not self.library_collection_name in [x.name for x in collections.collections]:
            self.client.create_collection(
                collection_name=self.library_collection_name,
                vectors_config=models.VectorParams(
                    size=384,
                    distance=models.Distance.COSINE
                )
            )

    def insert_transcript(self, fragment):
        #old_count = self.client.get_collection(collection_name=self.transcript_collection_name).vectors_count

        chunks = []
        num_chunks = math.ceil(len(fragment) / 2048)
        chunk_size = math.floor(len(fragment) / num_chunks)
        for i in range(num_chunks):
            start = chunk_size*i
            end = min(chunk_size*(i+1), len(fragment))
            chunks.append(fragment[start:end])

        timestamp = datetime.now()

        vectors = [
            models.PointStruct(
                id=uuid().hex,
                vector=self.retriever.encode(chunk).tolist(),
                payload={"text": chunk, "timestamp": timestamp}
            ) for chunk in chunks
        ]

        self.client.upsert(
            collection_name=self.transcript_collection_name,
            points=vectors
        )
        
        #new_count = self.client.get_collection(collection_name=self.transcript_collection_name).vectors_count
        #print(f"inserted {new_count - old_count} vectors")

    def query_transcript(self, prompt):
        prompt_enc = self.retriever.encode(prompt).tolist()
        return self.client.search(
            collection_name=self.transcript_collection_name,
            query_vector=prompt_enc,
            limit=4
        )

    def query_library(self, prompt):
        prompt_enc = self.retriever.encode(prompt).tolist()
        return self.client.search(
            collection_name=self.library_collection_name,
            query_vector=prompt_enc,
            limit=4
        )

if __name__ == "__main__":
    adapter = VectorDatabaseAdapter()
    adapter.insert_transcript("Hello my name is timmy, I'm building a friendly robot")
    print(
            adapter.query_transcript("What is timmy building?")
    )