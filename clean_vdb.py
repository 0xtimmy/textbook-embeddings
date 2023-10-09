import re
from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)
collections = client.get_collections()

for collection in [x.name for x in collections.collections]:
    if re.search(r"production-", collection) is None:
        client.delete_collection(collection_name=collection)
        print(f"deleting collection: {collection}")

