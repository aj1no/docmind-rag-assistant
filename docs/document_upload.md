# Document Upload

The DocMind Document API enables you to programmatically upload and manage your technical documentation. Once uploaded, documents are automatically scheduled for processing and vector indexing.

## Supported Formats

Currently, DocMind Cloud optimally parses and natively supports the following file formats:
- **Markdown (.md)** - *Recommended for structural clarity (headings, code blocks).*
- **Plain Text (.txt)**
- **PDF (.pdf)** - *Text extraction only. Optical Character Recognition (OCR) is billed separately.*

## File Limitations

To ensure system stability and fast processing times for all tenants, DocMind strictly enforces the following limits:
- **Maximum File Size:** 15 MB per file.
- **Concurrent Uploads:** Up to 50 concurrent file uploads per minute.
- **Maximum Chunks:** A single document will be truncated if it produces more than 10,000 embedded chunks.

## Uploading a Document

You can upload a document as a standard multipart form-data payload.

**Example Request:**
```bash
curl -X POST https://api.docmind.cloud/v1/documents/upload \
  -H "Authorization: Bearer dm_live_..." \
  -F "file=@./local_guide.md" \
  -F "collection=engineering" \
  -F "metadata={\"author\":\"John Doe\"}"
```

**Example Response:**
```json
{
  "id": "doc_11223344",
  "filename": "local_guide.md",
  "status": "processing",
  "uploaded_at": 1678888000
}
```

## Processing Lifecycle

When an upload is acknowledged, its status initially displays as `processing`. During this phase, DocMind Cloud:
1. Cleans the incoming text and extracts structural metadata.
2. Divides the text into overlapping tokens (chunking).
3. Evaluates semantic embeddings using our high-performance models.
4. Updates your workspace's local vector index.

Once complete, the document status transitions to `indexed`, at which point the contents are immediately available for semantic search or RAG generation.
