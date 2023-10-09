# Textbook Embeddings

Use AI to smart-search your textbooks using Q/A!
![Example Usage](https://raw.githubusercontent.com/0xtimmy/textbook-embeddings/master/Screenshot.png) 

# Usage

To start, boot up the qdrant vector database. this where we'll store and query embeddings. 
```
docker run -p 6333:6333 qdrant/qdrant
``` 

Next, upload your textbook using the following script. This will run Unstructured on the pdf, create embeddings, and send them to the database. It might take a while.
```
python ./upload_corpus.py -f ./DeepLearning.pdf
```

You're done! It's that easy. You can now open up a search bar and submit queries:
```
python ./search_library.py
```

You can upload multiple textbooks to the same database. If you would like to make additional databases you can edit the `COLLECTION_NAME` variable at the tops of `search_library.py` and `upload_corpus.py`. 
To clean out unused collections, `clean_vdb.py` will delete all databases that don't match a certain pattern.

# Installation

Install submodules:
```
git submodule update --init --recursive
```

Install python packages:
```
pip install -r requirements.txt
```

# References
[Qdrant](https://github.com/qdrant/qdrant)

[Unstructured.io](https://github.com/Unstructured-IO/unstructured)

[SentenceTransformers](https://huggingface.co/sentence-transformers/multi-qa-MiniLM-L6-cos-v1)