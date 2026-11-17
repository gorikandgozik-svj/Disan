# Security policy

Report issues privately to the project owner, not in a public issue containing secrets.

The remote MCP endpoint is **public and anonymous** and intentionally accepts only bounded, stateless requests. It has no disk write, shell execution, URL fetching, credentials, external billing or database integrations. The API checks Origin (when supplied), JSON-RPC shape, payload size, enumerated generation types, and title length. Hosting-level abuse protection and rate limiting are still needed for production.

The PWA's project settings are stored locally in the browser and are not sent to the cloud MCP by default. Browser storage can be cleared; projects may be lost. Generated HTML is escaped before interpolation. The preview iframe is sandboxed without access to same-origin data. Service workers cache only same-origin static GET responses, never API or MCP requests.

Do not ship API keys or private visual references inside publicly accessible files. Any expanded server functionality dealing with user files should require authenticated sessions, quotas and explicit permissions.
