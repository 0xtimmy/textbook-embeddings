import argparse
import math
from unstructured.partition.auto import partition
from uuid import uuid4 as uuid
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from tqdm import tqdm

COLLECTION_NAME = "production-library-v1" 

#parser
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename")
args = parser.parse_args()

print("----- CONNECTING TO DATABASE -----")
# setup database
retriever = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
client = QdrantClient(host="localhost", port=6333)

# initialize collection
collections = client.get_collections()
if not COLLECTION_NAME in [x.name for x in collections.collections]:
    print("----- INITIALIZING COLLECTION -----")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=384,
            distance=models.Distance.COSINE
        )
    )
old_count = client.get_collection(collection_name=COLLECTION_NAME).vectors_count

print("----- PARSING CORPUS -----")
# partition text
elements = partition(args.filename)

print("----- BEGIN EMBEDDING -----")
# clean & embed
last_title = ""
cleaned = []
for i in tqdm(range(len(elements))):
    el = elements[i]
    meta = el.to_dict()
    if meta["type"] == "Title":
            last_title = meta["text"]

    if meta["type"] == "NarrativeText":

        fragment = last_title + ": " + meta["text"]
        page = meta["metadata"]["page_number"]

        chunks = []
        num_chunks = math.ceil(len(fragment) / 2048)
        chunk_size = math.floor(len(fragment) / num_chunks)
        for i in range(num_chunks):
            start = chunk_size*i
            end = min(chunk_size*(i+1), len(fragment))
            chunks.append(fragment[start:end])

        vectors = [
            models.PointStruct(
                id=uuid().hex,
                vector=retriever.encode(chunk).tolist(),
                payload={"text": chunk, "source": args.filename, "title": last_title, "page": page}
            ) for chunk in chunks
        ]

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=vectors
        )

with open("./uploaded.log", "a") as f:
    f.write(f"{args.filename}\name")
    f.close()

new_count = client.get_collection(collection_name=COLLECTION_NAME).vectors_count
print(f"===== EMBEDDING COMPLETE: inserted {new_count - old_count} vectors =====")