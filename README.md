# Textbook Embeddings

This repo uses AI to help you smart search your textbooks using question answer.

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