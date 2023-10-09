from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

COLLECTION_NAME = "production-library-v1"

retriever = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
client = QdrantClient(host="localhost", port=6333)

query = input("> ")
while "exit" not in query: 
    encoded_search = retriever.encode(query)
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=encoded_search,
        limit=6
    )

    [print(f"\n-- {x.payload['source']}, page {x.payload['page']} -----\n {x.payload['text']}") for x in results]
    query = input("\n\n> ")