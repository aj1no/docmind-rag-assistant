# Search and Indexing

DocMind Cloud accelerates your workflows by offering lightning-fast, AI-driven semantic search. Unlike keyword-based engines, our ingestion relies on high-dimensional vectors to understand the *meaning* behind your questions and documents.

## The Indexing Process

1. **Extraction:** Text is parsed from your uploaded documents.
2. **Chunking:** The parsed text is intelligently split into chunks. We aim for 400-800 tokens per chunk to maintain optimal context window utilization for our LLMs.
3. **Embedding:** We pass these chunks through advanced sentence-transformers algorithms.
4. **Storage:** The resulting vectors are mapped into your workspace's dedicated localized FAISS index.

## Updating Documents

To update an existing document, you must upload the new version of the document referencing its original `doc_id`. 

```bash
curl -X PUT https://api.docmind.cloud/v1/documents/doc_11223344 \
  -H "Authorization: Bearer dm_live_..." \
  -F "file=@./local_guide_v2.md"
```

When a document is updated, DocMind Cloud automatically handles the invalidation of old chunks and seamlessly inserts the new representations into the vector store without downtime.

## Reindexing

Sometimes, DocMind releases global updates to our base embedding models. While we provide backwards compatibility, you may choose to trigger a manual workspace reindex to take advantage of improved accuracy.

**Trigger Reindex:**
```bash
curl -X POST https://api.docmind.cloud/v1/index/rebuild \
  -H "Authorization: Bearer dm_live_..."
```
*Note: Depending on your document volume, reindexing can take anywhere from a few seconds to a few hours. Your existing search endpoints will remain available and route to the old index until the new rebuild is fully complete.*
