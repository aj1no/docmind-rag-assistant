# Billing and Plans

DocMind Cloud provides flexible, usage-based billing suitable for startups scaling up to heavy-duty enterprise operations.

## Subscription Plans

DocMind offers three core tiers:

1. **Developer (Free)**
   - Ideal for testing and side projects.
   - Limit: 50 documents / 10MB total storage.
   - Rate limit: 60 API requests/minute.
   - Standard semantic search model only.

2. **Pro (Starting at $49/mo)**
   - Perfect for growing SaaS teams and internal wikis.
   - Limit: 5,000 documents / 5GB total storage.
   - Rate limit: 600 API requests/minute.
   - Access to advanced OpenAI-powered Generation endpoints.

3. **Enterprise (Custom)**
   - For massive data sets and dedicated infrastructure.
   - Custom limits and SLA guarantees.
   - Dedicated local instances (SOC2/HIPAA compliant).

## Usage Components

If your usage exceeds the quotas included in your plan, you are billed on a pay-as-you-go model:
- **Storage:** Billed incrementally per GB of vector index size over the limit.
- **Generation Compute:** Generating answers via the RAG API consumes compute credits. This is billed per 1,000 tokens generated.
- **Data Ingestion:** Uploading and converting text to embeddings is billed per 100,000 tokens ingested.

## Managing Subscriptions

You can upgrade, downgrade, or cancel your subscription at any time via the **Billing** tab in the DocMind Dashboard. Any changes to plans are prorated automatically.

*Note: If you downgrade from Pro to Developer and your workspace already exceeds the 50 document limit, your API access will be restricted to read-only until you delete excess data.*
