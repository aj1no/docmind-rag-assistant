# Authentication

Welcome to the **DocMind Cloud** API authentication guide. Our API uses API keys to authenticate requests. You can view and manage your API keys in the DocMind Cloud Dashboard under the **Developers** section.

## Obtaining an API Key

To get started, you will need a secret API key. 

1. Log in to your [DocMind Cloud Dashboard](https://dashboard.docmind.cloud).
2. Navigate to **Developers** > **API Keys**.
3. Generate a new "Secret Key".

> **Warning:** Keep your secret key safe! Never expose it in client-side code, public repositories, or share it in support chats.

## Authenticating Requests

All API requests must be made over HTTPS. Calls made over plain HTTP will fail. API requests without authentication will also fail.

You authenticate to the DocMind API by providing your secret key in the request header.

### Bearer Token

Provide your API key as a Bearer token in the `Authorization` header.

**Example Request:**
```bash
curl https://api.docmind.cloud/v1/workspaces \
  -H "Authorization: Bearer dm_test_1234567890abcdef"
```

## Scopes and Best Practices

DocMind Cloud offers different API key modes:
- **Test Mode Keys** (prefix: `dm_test_`): Use these keys to build and test your integration without processing real data or consuming billing credits.
- **Live Mode Keys** (prefix: `dm_live_`): Use these keys for production. Actions taken with live keys will affect your actual billing and data.

### Key Rotation

For maximum security, we recommend rotating your keys periodically. You can generate a new key in the dashboard, update your application servers with the new key, and then safely delete the old key.

## Error Handling

If an API key is missing, malformed, or invalid, you will receive a `401 Unauthorized` response:
```json
{
  "error": {
    "type": "authentication_error",
    "message": "Invalid API Key provided: dm_test_***"
  }
}
```
