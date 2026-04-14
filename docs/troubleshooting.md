# Troubleshooting

Below is a guide to resolving the most common issues you might encounter while integrating with DocMind Cloud.

## 1. Authentication Errors (`401 Unauthorized`)
**Symptom:** Every API request returns a 401 error.
**Solution:**
- Verify you are passing the API key in the `Authorization: Bearer <key>` format.
- Ensure the API key has not been revoked in the dashboard.
- Check that you aren't accidentally using a `dm_test_` key in a production environment context that demands live keys.

## 2. Rate Limiting (`429 Too Many Requests`)
**Symptom:** You are abruptly blocked from uploading files or making queries.
**Solution:**
- DocMind enforces rate limits on a per-workspace basis. If you hit this limit, you should implement an exponential backoff strategy in your SDK/API client.
- Consider upgrading your plan if your application legitimately requires a higher throughput limit.

## 3. Hallucination or Inaccurate Answers
**Symptom:** The `/ask` endpoint returns information that doesn't exist in your documents.
**Solution:**
- Ensure you have executed the `/ingest` endpoint after uploading new files, otherwise the Vector store won't know they exist.
- Verify that your document format is cleanly structured. Messy PDF extractions can confuse the chunking mechanisms.
- If the issue persists, review the `sources` array in the response to verify what context the LLM is actually retrieving. Adjusting `top_k` to a higher value may capture the missing context.

## 4. File Upload Failures (`413 Payload Too Large`)
**Symptom:** Document uploads fail immediately.
**Solution:**
- Verify your file is under the 15 MB threshold.
- If you have extensive log files or images embedded in the markdown, strip them out before uploading to DocMind.
