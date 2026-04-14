# Users and Roles

DocMind Cloud operates on a role-based access control (RBAC) model. This ensures that only authorized entities can perform actions like uploading documents, altering indexes, or administering billing details.

## Core Concepts

In DocMind Cloud, identities are separated into three different scopes:
- **Workspace Owner:** The root user who created the workspace. Has absolute privileges over billing, API keys, and member management.
- **Member:** An identity belonging to a workspace with an assigned Role.
- **Service Account (API):** Automated systems accessing the system via API keys. Service accounts inherit privileges based on how the API key was configured.

## Predefined Roles

DocMind provides predefined roles out of the box to simplify access management:

### 1. Admin
Has full access to all workspace settings except transferring ownership or deleting the workspace.
- **Capabilities:** Invite users, manage billing, create/delete API keys, manage document indexes.

### 2. Editor
Can manage documentation sets and view basic workspace metrics.
- **Capabilities:** Upload documents, delete documents, trigger reindexing, view search logs.
- **Restrictions:** Cannot view or edit billing, cannot manage API keys.

### 3. Viewer
Can only access the DocMind portal to search and read documents.
- **Capabilities:** Execute search queries, view documents.
- **Restrictions:** Cannot edit documents, cannot see workspace configuration.

## Managing Roles via API

You can invite new members and set their initial roles using the Users API.

**Example Request:**
```bash
curl -X POST https://api.docmind.cloud/v1/users/invite \
  -H "Authorization: Bearer dm_live_..." \
  -H "Content-Type: application/json" \
  -d '{
    "email": "developer@example.com",
    "role": "editor"
  }'
```

**Example Response:**
```json
{
  "id": "usr_987654321",
  "email": "developer@example.com",
  "role": "editor",
  "status": "pending_invite",
  "created_at": 1678886400
}
```

## Security Best Practices
- Practice the **Principle of Least Privilege**: grant users only the permissions necessary for their tasks.
- Periodically audit your workspace members and clean up stale Service Accounts.
