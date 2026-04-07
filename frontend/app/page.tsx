import { IngestPanel } from "@/components/ingest-panel";
import { ChatInterface } from "@/components/chat-interface";

export default function HomePage() {
  return (
    <div className="flex h-dvh overflow-hidden bg-rc-bg">
      {/* ── Sidebar ──────────────────────────────────────────── */}
      <aside
        className="flex w-[288px] shrink-0 flex-col overflow-hidden"
        style={{
          borderRight: "1px solid rgba(255,255,255,0.06)",
          background: "#0b0c0e",
        }}
      >
        {/* Logo / header */}
        <div
          className="flex shrink-0 items-center gap-2.5 px-4 py-3.5"
          style={{ borderBottom: "1px solid rgba(255,255,255,0.06)" }}
        >
          {/* Brand mark */}
          <div
            className="flex h-6 w-6 shrink-0 items-center justify-center rounded-btn"
            style={{
              background: "linear-gradient(135deg, #FF6363 0%, #cc4a4a 100%)",
              boxShadow:
                "rgba(255,99,99,0.4) 0px 2px 8px, rgba(255,255,255,0.1) 0px 1px 0px 0px inset",
            }}
          >
            <svg
              width="12"
              height="12"
              viewBox="0 0 12 12"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M2 10L6 2L10 10"
                stroke="white"
                strokeWidth="1.6"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M3.5 7.5H8.5"
                stroke="white"
                strokeWidth="1.6"
                strokeLinecap="round"
              />
            </svg>
          </div>

          <div>
            <p className="text-[13px] font-semibold leading-none tracking-tight text-rc-white">
              Agentic RAG
            </p>
            <p className="mt-0.5 text-[10px] tracking-rc-wide text-rc-dark">
              Knowledge Base
            </p>
          </div>
        </div>

        {/* Ingest panel (scrollable) */}
        <div className="flex-1 overflow-hidden">
          <IngestPanel />
        </div>
      </aside>

      {/* ── Main chat area ────────────────────────────────────── */}
      <main className="flex flex-1 flex-col overflow-hidden">
        <ChatInterface />
      </main>
    </div>
  );
}
