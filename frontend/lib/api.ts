import axios from "axios";
import {
  chatChatPost,
  healthHealthGet,
  ingestDocumentIngestPost,
  ingestFileIngestFilePost,
} from "../gen/index";
import type { CitationOut, IngestResponse, ChatResponse } from "../gen/index";

export type { CitationOut, IngestResponse, ChatResponse };

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

// Configure default axios instance
axios.defaults.baseURL = BASE_URL;

export async function healthCheck(): Promise<boolean> {
  try {
    const res = await healthHealthGet({ baseURL: BASE_URL } as any); // config might only be partial
    return res.status === "ok";
  } catch {
    return false;
  }
}

export async function ingestText(
  content: string,
  filename: string,
  source?: string,
): Promise<IngestResponse> {
  return await ingestDocumentIngestPost(
    {
      content,
      filename,
      source: source || filename,
    },
    { baseURL: BASE_URL },
  );
}

export async function ingestFile(
  file: File,
  source?: string,
): Promise<IngestResponse> {
  return await ingestFileIngestFilePost(
    {
      file,
      source: source,
    },
    { baseURL: BASE_URL },
  );
}

/** @deprecated Use chatStream() for streaming responses */
export async function chat(query: string, top_k = 5): Promise<ChatResponse> {
  return await chatChatPost({ query, top_k }, { baseURL: BASE_URL });
}

/* ── SSE streaming chat ──────────────────────────────────────── */

export interface ChatStreamCallbacks {
  onToken: (token: string) => void;
  onCitations: (citations: CitationOut[]) => void;
  onDone: (conversationId: string) => void;
  onError: (error: string) => void;
}

/**
 * Stream chat via SSE (POST /chat/stream).
 * Returns an AbortController so the caller can cancel mid-stream.
 */
export function chatStream(
  query: string,
  top_k: number,
  callbacks: ChatStreamCallbacks,
): AbortController {
  const controller = new AbortController();

  (async () => {
    try {
      const res = await fetch(`${BASE_URL}/chat/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "text/event-stream" },
        body: JSON.stringify({ query, top_k }),
        signal: controller.signal,
      });

      if (!res.ok) {
        callbacks.onError(`服务端错误 (${res.status})`);
        return;
      }

      const reader = res.body?.getReader();
      if (!reader) {
        callbacks.onError("浏览器不支持流式读取");
        return;
      }

      const decoder = new TextDecoder();
      let buffer = "";
      let currentEvent = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        // SSE protocol: events separated by double newline
        const parts = buffer.split("\n\n");
        // Last element is either empty or an incomplete event
        buffer = parts.pop() ?? "";

        for (const part of parts) {
          const lines = part.split("\n");
          let data = "";

          for (const line of lines) {
            if (line.startsWith("event: ")) {
              currentEvent = line.slice(7).trim();
            } else if (line.startsWith("data: ")) {
              data = line.slice(6);
            }
          }

          if (!data) continue;

          try {
            const parsed = JSON.parse(data);

            switch (currentEvent) {
              case "chunk":
                callbacks.onToken(parsed.token ?? "");
                break;
              case "citations":
                callbacks.onCitations(parsed.citations ?? []);
                break;
              case "done":
                callbacks.onDone(parsed.conversation_id ?? "");
                break;
            }
          } catch {
            // Malformed JSON — skip
          }

          currentEvent = "";
        }
      }
    } catch (err: unknown) {
      if ((err as Error).name === "AbortError") return; // User cancelled
      callbacks.onError(
        err instanceof Error ? err.message : "流式请求失败，请稍后重试",
      );
    }
  })();

  return controller;
}
