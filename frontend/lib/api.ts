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

export async function chat(query: string, top_k = 5): Promise<ChatResponse> {
  return await chatChatPost({ query, top_k }, { baseURL: BASE_URL });
}
