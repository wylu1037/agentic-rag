"use client";

import {
  useState,
  useRef,
  useEffect,
  useCallback,
  type KeyboardEvent,
} from "react";
import { cn } from "@/lib/utils";
import { chat } from "@/lib/api";
import { MessageBubble, type Message } from "./message-bubble";
import {
  PaperPlaneTilt,
  ArrowsCounterClockwise,
  Sparkle,
  ShieldWarning,
  SlidersHorizontal,
} from "@phosphor-icons/react";

/* ── Empty state ─────────────────────────────────────────────── */
function EmptyState() {
  return (
    <div className="flex h-full select-none flex-col items-center justify-center gap-6 px-8">
      {/* Glow orb */}
      <div
        className="relative flex h-16 w-16 items-center justify-center rounded-full"
        style={{
          background:
            "radial-gradient(circle at 40% 35%, #FF636322 0%, #07080a 70%)",
          boxShadow:
            "rgb(27,28,30) 0px 0px 0px 1px, rgb(7,8,10) 0px 0px 0px 1px inset",
        }}
      >
        <Sparkle size={24} weight="duotone" className="text-[#FF6363]" />
      </div>

      <div className="text-center">
        <h2 className="mb-1 text-xl font-semibold tracking-tight text-rc-white">
          Agentic RAG
        </h2>
        <p className="max-w-[28ch] text-sm leading-relaxed text-rc-mid">
          先在左侧上传文档，再向知识库提问
        </p>
      </div>

      {/* Hint chips */}
      <div className="flex flex-wrap justify-center gap-2">
        {["RAG 是什么？", "总结这份文档的核心内容", "列出主要章节"].map(
          (hint) => (
            <span
              key={hint}
              className={cn(
                "rounded-pill px-3 py-1.5 text-xs text-rc-mid",
                "border border-white/[0.06] bg-white/[0.02]",
                "cursor-default",
              )}
            >
              {hint}
            </span>
          ),
        )}
      </div>
    </div>
  );
}

/* ── Settings popover ────────────────────────────────────────── */
function SettingsPopover({
  topK,
  setTopK,
  onClose,
}: {
  topK: number;
  setTopK: (v: number) => void;
  onClose: () => void;
}) {
  return (
    <div
      className="absolute bottom-full right-0 z-50 mb-2 w-56 rounded-card p-4"
      style={{ boxShadow: "var(--shadow-floating)", background: "#1b1c1e" }}
    >
      <div className="mb-3 flex items-center justify-between">
        <p className="text-xs font-semibold uppercase tracking-widest text-rc-mid">
          检索参数
        </p>
        <button onClick={onClose} className="text-rc-dark hover:text-rc-mid">
          ✕
        </button>
      </div>

      <div>
        <div className="mb-1 flex items-center justify-between">
          <label className="text-xs text-rc-mid">Top-K 召回数</label>
          <span className="font-mono text-xs text-rc-white">{topK}</span>
        </div>
        <input
          type="range"
          min={1}
          max={20}
          value={topK}
          onChange={(e) => setTopK(Number(e.target.value))}
          className="w-full accent-[#FF6363]"
        />
        <div className="mt-0.5 flex justify-between text-[10px] text-rc-dark">
          <span>1</span>
          <span>20</span>
        </div>
      </div>
    </div>
  );
}

/* ── Chat Interface ──────────────────────────────────────────── */
export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [topK, setTopK] = useState(5);
  const [showSettings, setShowSettings] = useState(false);

  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  /* Auto-scroll */
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  /* Auto-resize textarea */
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 160)}px`;
  }, [input]);

  const sendMessage = useCallback(async () => {
    const query = input.trim();
    if (!query || loading) return;

    const userMsg: Message = {
      id: `u-${Date.now()}`,
      role: "user",
      content: query,
    };
    const assistantId = `a-${Date.now()}`;
    const loadingMsg: Message = {
      id: assistantId,
      role: "assistant",
      content: "",
      isLoading: true,
    };

    setMessages((prev) => [...prev, userMsg, loadingMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await chat(query, topK);
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantId
            ? {
                ...m,
                content: res.answer,
                citations: res.citations,
                isLoading: false,
              }
            : m,
        ),
      );
    } catch (e: unknown) {
      const errMsg = e instanceof Error ? e.message : "请求失败，请稍后重试";
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantId
            ? { ...m, content: "", isLoading: false, error: errMsg }
            : m,
        ),
      );
    } finally {
      setLoading(false);
    }
  }, [input, loading, topK]);

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  function clearChat() {
    setMessages([]);
  }

  return (
    <div className="flex h-full flex-col">
      {/* ── Top bar ──────────────────────────────────────── */}
      <div
        className={cn(
          "flex shrink-0 items-center justify-between px-5 py-3",
          "border-b border-white/[0.06]",
        )}
      >
        <div className="flex items-center gap-2">
          <div
            className="h-1.5 w-1.5 rounded-full"
            style={{ background: "#5fc992", boxShadow: "0 0 6px #5fc99266" }}
          />
          <span className="text-xs tracking-rc-wide text-rc-mid">
            与知识库对话
          </span>
        </div>

        <div className="flex items-center gap-2">
          {messages.length > 0 && (
            <button
              onClick={clearChat}
              className="flex items-center gap-1.5 rounded-btn border border-transparent px-2.5 py-1 text-xs text-rc-dark transition-colors hover:border-white/[0.06] hover:text-rc-mid"
            >
              <ArrowsCounterClockwise size={12} />
              清空
            </button>
          )}
        </div>
      </div>

      {/* ── Messages ─────────────────────────────────────── */}
      <div className="flex-1 overflow-y-auto px-5 py-5">
        {messages.length === 0 ? (
          <EmptyState />
        ) : (
          <div className="mx-auto flex max-w-3xl flex-col gap-5">
            {messages.map((m) => (
              <MessageBubble key={m.id} message={m} />
            ))}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      {/* ── Backend error notice ──────────────────────────── */}
      {/* ── Input area ───────────────────────────────────── */}
      <div className="shrink-0 px-5 pb-5 pt-3">
        <div className="mx-auto max-w-3xl">
          <div
            className={cn(
              "relative flex items-end gap-2 rounded-card p-1 pl-3",
              "border border-white/[0.08] bg-rc-surface",
              "transition-colors duration-200 focus-within:border-white/[0.16]",
              "shadow-card",
            )}
          >
            <textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="向知识库提问… (Enter 发送，Shift+Enter 换行)"
              rows={1}
              disabled={loading}
              className={cn(
                "flex-1 resize-none bg-transparent py-2 text-sm text-rc-white",
                "outline-none placeholder:text-rc-dim",
                "font-sans font-medium leading-relaxed",
                "disabled:opacity-50",
              )}
              style={{ maxHeight: 160 }}
            />

            <div className="flex items-center gap-1 pb-1.5 pr-1">
              {/* Settings trigger */}
              <div className="relative">
                <button
                  onClick={() => setShowSettings((v) => !v)}
                  className={cn(
                    "rounded-btn p-1.5 transition-all duration-150",
                    showSettings
                      ? "bg-[rgba(85,179,255,0.1)] text-[#55b3ff]"
                      : "text-rc-dark hover:text-rc-mid",
                  )}
                  title="检索设置"
                >
                  <SlidersHorizontal size={15} />
                </button>
                {showSettings && (
                  <SettingsPopover
                    topK={topK}
                    setTopK={setTopK}
                    onClose={() => setShowSettings(false)}
                  />
                )}
              </div>

              {/* Send button */}
              <button
                onClick={sendMessage}
                disabled={!input.trim() || loading}
                className={cn(
                  "flex h-8 w-8 items-center justify-center rounded-btn",
                  "transition-all duration-150",
                  input.trim() && !loading
                    ? "bg-[#FF6363] text-white hover:opacity-80 active:scale-95"
                    : "cursor-not-allowed bg-white/[0.04] text-rc-dark",
                )}
              >
                {loading ? (
                  <span
                    className="h-3 w-3 animate-spin rounded-full border-2 border-white/20 border-t-white/60"
                    style={{ animation: "spin 0.7s linear infinite" }}
                  />
                ) : (
                  <PaperPlaneTilt size={15} weight="fill" />
                )}
              </button>
            </div>
          </div>

          {/* Keyboard hint */}
          <div className="mt-2 flex items-center gap-1.5 px-1">
            <ShieldWarning size={11} className="text-rc-dark" />
            <span className="text-[10px] text-rc-dark">
              仅根据已摄入文档回答 · Top-K={topK}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
