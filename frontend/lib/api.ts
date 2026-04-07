const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

/* ── Types ─────────────────────────────────────────────────── */

export interface IngestResponse {
  document_id: string;
  title: string;
  chunk_count: number;
}

export interface CitationOut {
  document_title: string;
  source: string;
  source_section: string;
  content_snippet: string;
  score: number;
}

export interface ChatResponse {
  answer: string;
  citations: CitationOut[];
  conversation_id: string;
}

/* ── API calls ─────────────────────────────────────────────── */

export async function healthCheck(): Promise<boolean> {
  try {
    const res = await fetch(`${BASE_URL}/health`, { cache: "no-store" });
    return res.ok;
  } catch {
    return false;
  }
}

export async function ingestText(
  content: string,
  filename: string,
  source?: string,
): Promise<IngestResponse> {
  const res = await fetch(`${BASE_URL}/ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content, filename, source: source || filename }),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(detail || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function ingestFile(
  file: File,
  source?: string,
): Promise<IngestResponse> {
  const form = new FormData();
  form.append("file", file);
  if (source) form.append("source", source);

  const res = await fetch(`${BASE_URL}/ingest/file`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(detail || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function chat(
  query: string,
  top_k = 5,
): Promise<ChatResponse> {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, top_k }),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(detail || `HTTP ${res.status}`);
  }
  return res.json();
}
