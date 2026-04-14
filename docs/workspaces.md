# Workspaces

DocMind Cloud operates fundamentally on a multi-tenant architecture. The core boundary for multi-tenancy in our platform is the **Workspace**. 

## What is a Workspace?

A Workspace represents an isolated environment for your documentation schemas, uploaded files, vector indexes, and usage analytics. 

- Data separation is strictly enforced at the Workspace level. 
- API Keys are scoped exactly to one Workspace.
- A user account can be a member of multiple Workspaces.

## Data Organization

Within a workspace, data is organized logically as follows:

1. **Workspace:** The root entity containing everything.
2. **Collections:** Logical folders or tags that group related documents (e.g., "Engineering Docs", "HR Handbook").
3. **Documents:** The actual files (Markdown, PDF, TXT) that have been imported.
4. **Chunks:** Vector representations of smaller segments derived from your Documents for semantic retrieval.

## Creating a Workspace

New workspaces can be created via the DocMind Dashboard or dynamically via the API if your current plan supports programmatic provisioning.

**Example: Switch Workspace Context (API)**
When making API requests, the target workspace is inferred from the API Key provided in the `Authorization` header. You do not need to explicitly specify a `workspace_id` in most endpoints, as it is derived from your credentials.

## Cross-Workspace Access

Currently, DocMind Cloud **does not** support cross-workspace queries. If you need to search across two different documentation sets simultaneously, they must either reside in the same Workspace (potentially organized into different Collections), or you must perform two separate API queries on the client side using the respective API keys.
