## Section 3: Request and Response Structure (Non-Streaming)

### 1. Why does the request use a client-generated id rather than a server-generated one? What problem does this solve in distributed systems?
Using a client-generated `id` lets the caller assign a stable correlation key before sending the request. In distributed systems, retries, load balancers, queues, and asynchronous processing can cause duplicate submissions or out-of-order responses. If the same task is resent with the same `id`, the server can detect duplicates (idempotency), and the client can reliably match any response to the original logical task. This avoids ambiguity when multiple requests are in flight and helps with traceability across services.

### 2. The status.state can be 'working'. Under what circumstances would a server return this state in a non-streaming call, and how should a client react?
A server may return `working` when the task is accepted but not finished within the request timeout window, or when execution is intentionally deferred to a background worker (for long-running tasks like large document analysis or external tool orchestration). In a non-streaming pattern, the client should treat `working` as in-progress: keep the task `id`, then poll a status/result endpoint (or follow protocol-specific continuation instructions) with backoff until the state becomes `completed`, `failed`, or `canceled`.

### 3. What is the purpose of the sessionId field? Give a concrete example of two related tasks that should share a session.
`sessionId` groups related tasks into one conversational or workflow context so the server can preserve shared state (history, cached intermediate results, user intent, tool outputs). Example: Task A asks, "Summarize this PDF and list key risks." Task B then asks, "Now draft a response email for risk #2." Both should use the same `sessionId` so Task B can reference Task A's extracted context without re-uploading or re-explaining the PDF.

### 4. The parts array supports types text, file, and data. Describe a realistic multi-agent workflow where all three part types appear in a single conversation.
A realistic workflow is contract review automation:

1. User sends a request with:
	- `text`: "Review this supplier contract and flag legal and financial risks."
	- `file`: URL to the contract PDF (`mimeType: application/pdf`).
	- `data`: structured constraints like `{ "jurisdiction": "TW", "riskThreshold": "medium", "deadline": "2026-05-01" }`.
2. A document-ingestion agent reads the file and extracts clauses.
3. A legal-analysis agent uses the text goal plus extracted clauses.
4. A finance-risk agent uses the same clauses plus structured `data` constraints.
5. A coordinator agent merges outputs and returns an artifact with a textual executive summary and optional links to generated annotated files.

This uses all three part types together: natural-language intent (`text`), binary/document input (`file`), and machine-readable parameters (`data`).
