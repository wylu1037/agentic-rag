import { IngestPanel } from "@/components/ingest-panel";
import { ChatInterface } from "@/components/chat-interface";

export default function HomePage() {
  return (
    <div className="flex h-dvh overflow-hidden bg-rc-bg">
      {/* ── Sidebar ──────────────────────────────────────────── */}
      <aside
        className="w-[288px] shrink-0 flex flex-col overflow-hidden"
        style={{
          borderRight: "1px solid rgba(255,255,255,0.06)",
          background: "#0b0c0e",
        }}
      >
        {/* Logo / header */}
        <div
          className="shrink-0 flex items-center gap-2.5 px-4 py-3.5"
          style={{ borderBottom: "1px solid rgba(255,255,255,0.06)" }}
        >
          {/* Brand mark */}
          <div
            className="w-6 h-6 rounded-btn flex items-center justify-center shrink-0"
            style={{
              background:
                "linear-gradient(135deg, #FF6363 0%, #cc4a4a 100%)",
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
            <p className="text-[13px] font-semibold text-rc-white tracking-tight leading-none">
              Agentic RAG
            </p>
            <p className="text-[10px] text-rc-dark mt-0.5 tracking-rc-wide">
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
      <main className="flex-1 flex flex-col overflow-hidden">
        <ChatInterface />
      </main>
    </div>
  );
}
