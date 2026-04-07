"use client";

import { cn } from "@/lib/utils";
import type { CitationOut } from "@/lib/api";
import { CitationCard } from "./citation-card";
import { Quotes, Robot } from "@phosphor-icons/react";
import { useState } from "react";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  citations?: CitationOut[];
  isLoading?: boolean;
  error?: string;
}

interface MessageBubbleProps {
  message: Message;
}

/* ── Loading dots ────────────────────────────────────────────── */
function ThinkingDots() {
  return (
    <div className="flex items-center gap-1 py-1">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="h-1.5 w-1.5 rounded-full bg-rc-mid"
          style={{
            animation: "pulse-dot 1.4s ease-in-out infinite",
            animationDelay: `${i * 0.16}s`,
          }}
        />
      ))}
    </div>
  );
}

/* ── Citations section ───────────────────────────────────────── */
function Citations({ citations }: { citations: CitationOut[] }) {
  const [open, setOpen] = useState(false);

  if (!citations.length) return null;

  return (
    <div className="mt-3">
      <button
        onClick={() => setOpen((v) => !v)}
        className={cn(
          "flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-rc-wide",
          "transition-colors duration-150",
          open ? "text-rc-mid" : "text-rc-dark hover:text-rc-mid",
        )}
      >
        <Quotes size={12} weight="fill" />
        {citations.length} 条引用
        <span
          className={cn(
            "transition-transform duration-200",
            open ? "rotate-180" : "",
          )}
        >
          ▾
        </span>
      </button>

      {open && (
        <div className="mt-2 grid gap-1.5">
          {citations.map((c, i) => (
            <CitationCard key={`${c.source}-${i}`} citation={c} index={i} />
          ))}
        </div>
      )}
    </div>
  );
}

/* ── Message Bubble ──────────────────────────────────────────── */
export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  if (isUser) {
    return (
      <div className="flex animate-fade-up justify-end">
        <div
          className={cn(
            "max-w-[78%] rounded-card rounded-br-btn px-4 py-2.5",
            "border border-white/[0.08] bg-white/[0.06]",
            "text-[15px] leading-relaxed text-rc-white",
            "whitespace-pre-wrap break-words",
          )}
        >
          {message.content}
        </div>
      </div>
    );
  }

  /* Assistant */
  return (
    <div className="flex animate-fade-up gap-3">
      {/* Avatar */}
      <div
        className={cn(
          "mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-btn",
          "border border-white/[0.08] bg-rc-elevated",
          message.isLoading && "shimmer",
        )}
      >
        <Robot size={14} weight="fill" className="text-[#FF6363]" />
      </div>

      <div className="min-w-0 flex-1">
        {/* Error state */}
        {message.error && (
          <div
            className="rounded-btn px-3 py-2 text-sm"
            style={{
              background: "rgba(255,99,99,0.08)",
              border: "1px solid rgba(255,99,99,0.2)",
              color: "#FF6363",
            }}
          >
            {message.error}
          </div>
        )}

        {/* Loading state */}
        {message.isLoading && !message.error && (
          <div className="pt-1">
            <ThinkingDots />
          </div>
        )}

        {/* Answer text */}
        {!message.isLoading && !message.error && (
          <>
            <div
              className={cn(
                "whitespace-pre-wrap break-words text-[15px] leading-relaxed text-rc-lt",
              )}
            >
              {message.content}
            </div>

            {message.citations && <Citations citations={message.citations} />}
          </>
        )}
      </div>
    </div>
  );
}
