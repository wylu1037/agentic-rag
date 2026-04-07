"use client";

import { useState, useRef, useCallback } from "react";
import { cn } from "@/lib/utils";
import { ingestText, ingestFile, type IngestResponse } from "@/lib/api";
import {
  UploadSimple,
  FilePlus,
  FileText,
  CheckCircle,
  WarningCircle,
  X,
  CloudArrowUp,
} from "@phosphor-icons/react";

/* ── Types ─────────────────────────────────────────────────── */
interface IngestedDoc {
  id: string;
  title: string;
  chunk_count: number;
  addedAt: Date;
}

type TabKey = "file" | "text";

/* ── Sub-components ─────────────────────────────────────────── */
function Tab({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "flex-1 rounded-btn py-1.5 text-xs font-semibold tracking-rc-wide transition-all duration-150",
        active
          ? "bg-white/[0.08] text-rc-white"
          : "text-rc-dim hover:text-rc-mid",
      )}
    >
      {children}
    </button>
  );
}

function DocRow({ doc, onRemove }: { doc: IngestedDoc; onRemove: () => void }) {
  return (
    <div
      className={cn(
        "flex items-center gap-2 rounded-btn px-2 py-2",
        "group animate-fade-up transition-colors hover:bg-white/[0.04]",
      )}
    >
      <FileText size={13} className="shrink-0 text-rc-dim" />
      <span className="flex-1 truncate text-xs text-rc-lt">{doc.title}</span>
      <span
        className="shrink-0 rounded px-1.5 py-0.5 font-mono text-[10px]"
        style={{ background: "rgba(85,179,255,0.12)", color: "#55b3ff" }}
      >
        {doc.chunk_count}块
      </span>
      <button
        onClick={onRemove}
        className="shrink-0 text-rc-dark opacity-0 transition-all hover:text-rc-mid group-hover:opacity-100"
      >
        <X size={12} />
      </button>
    </div>
  );
}

/* ── Ingest Panel ───────────────────────────────────────────── */
export function IngestPanel() {
  const [tab, setTab] = useState<TabKey>("file");
  const [docs, setDocs] = useState<IngestedDoc[]>([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<{
    type: "success" | "error";
    msg: string;
  } | null>(null);

  // File tab
  const [dragOver, setDragOver] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  // Text tab
  const [textFilename, setTextFilename] = useState("");
  const [textContent, setTextContent] = useState("");

  /* helpers */
  const flashStatus = useCallback((type: "success" | "error", msg: string) => {
    setStatus({ type, msg });
    setTimeout(() => setStatus(null), 4000);
  }, []);

  const onIngested = useCallback(
    (res: IngestResponse) => {
      setDocs((prev) => [
        {
          id: res.document_id,
          title: res.title,
          chunk_count: res.chunk_count,
          addedAt: new Date(),
        },
        ...prev,
      ]);
      flashStatus("success", `已摄入 "${res.title}" — ${res.chunk_count} 块`);
    },
    [flashStatus],
  );

  /* File upload */
  async function handleFiles(files: FileList | null) {
    if (!files?.length) return;
    setLoading(true);
    try {
      for (const file of Array.from(files)) {
        const res = await ingestFile(file);
        onIngested(res);
      }
    } catch (e: unknown) {
      flashStatus("error", e instanceof Error ? e.message : "上传失败");
    } finally {
      setLoading(false);
    }
  }

  /* Text ingest */
  async function handleTextIngest() {
    if (!textFilename.trim() || !textContent.trim()) return;
    setLoading(true);
    try {
      const res = await ingestText(
        textContent,
        textFilename.endsWith(".md") ? textFilename : textFilename + ".md",
      );
      onIngested(res);
      setTextFilename("");
      setTextContent("");
    } catch (e: unknown) {
      flashStatus("error", e instanceof Error ? e.message : "摄入失败");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-full flex-col">
      {/* Section label */}
      <div className="px-4 pb-2 pt-4">
        <p className="text-[10px] font-semibold uppercase tracking-widest text-rc-dark">
          知识库
        </p>
      </div>

      {/* Tabs */}
      <div className="px-4 pb-3">
        <div className="flex gap-1 rounded-btn border border-white/[0.06] bg-white/[0.03] p-1">
          <Tab active={tab === "file"} onClick={() => setTab("file")}>
            <span className="flex items-center justify-center gap-1">
              <UploadSimple size={11} />
              上传文件
            </span>
          </Tab>
          <Tab active={tab === "text"} onClick={() => setTab("text")}>
            <span className="flex items-center justify-center gap-1">
              <FilePlus size={11} />
              粘贴文本
            </span>
          </Tab>
        </div>
      </div>

      {/* Panel body */}
      <div className="flex-shrink-0 px-4">
        {tab === "file" ? (
          /* ── File drop zone ─────────────────────────── */
          <div
            onClick={() => !loading && fileRef.current?.click()}
            onDragOver={(e) => {
              e.preventDefault();
              setDragOver(true);
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDragOver(false);
              handleFiles(e.dataTransfer.files);
            }}
            className={cn(
              "relative flex flex-col items-center justify-center gap-2",
              "cursor-pointer rounded-card border-2 border-dashed",
              "px-4 py-6 text-center transition-all duration-200",
              dragOver
                ? "border-[#55b3ff] bg-[rgba(85,179,255,0.06)]"
                : "border-white/[0.08] hover:border-white/[0.14] hover:bg-white/[0.02]",
              loading && "pointer-events-none opacity-50",
            )}
          >
            <CloudArrowUp
              size={28}
              weight="duotone"
              className={cn(
                "transition-colors",
                dragOver ? "text-[#55b3ff]" : "text-rc-dark",
              )}
            />
            <p className="text-xs text-rc-mid">
              拖拽或{" "}
              <span className="text-rc-white underline underline-offset-2">
                点击选择
              </span>
            </p>
            <p className="text-[10px] text-rc-dark">
              PDF · Markdown · DOCX · TXT
            </p>
            <input
              ref={fileRef}
              type="file"
              multiple
              accept=".pdf,.md,.txt,.docx"
              className="hidden"
              onChange={(e) => handleFiles(e.target.files)}
            />
          </div>
        ) : (
          /* ── Text paste ────────────────────────────── */
          <div className="flex flex-col gap-2">
            <input
              value={textFilename}
              onChange={(e) => setTextFilename(e.target.value)}
              placeholder="文件名 (e.g. guide.md)"
              className={cn(
                "rc-input w-full px-3 py-2 text-sm",
                "disabled:opacity-50",
              )}
              disabled={loading}
            />
            <textarea
              value={textContent}
              onChange={(e) => setTextContent(e.target.value)}
              placeholder="粘贴 Markdown 或纯文本内容..."
              rows={5}
              className={cn(
                "rc-input w-full resize-none px-3 py-2 font-mono text-sm",
                "disabled:opacity-50",
              )}
              disabled={loading}
            />
            <button
              onClick={handleTextIngest}
              disabled={loading || !textFilename.trim() || !textContent.trim()}
              className={cn(
                "w-full rounded-btn py-2 text-sm font-semibold transition-all duration-150",
                "bg-[#FF6363] tracking-rc-btn text-white",
                "hover:opacity-80 active:scale-[0.98]",
                "disabled:cursor-not-allowed disabled:opacity-30",
                loading && "shimmer",
              )}
            >
              {loading ? "处理中…" : "摄入文档"}
            </button>
          </div>
        )}

        {/* Status toast */}
        {status && (
          <div
            className={cn(
              "mt-2 flex items-center gap-2 rounded-btn px-3 py-2 text-xs",
              "animate-fade-up",
              status.type === "success"
                ? "border border-[rgba(95,201,146,0.2)] bg-[rgba(95,201,146,0.1)] text-[#5fc992]"
                : "border border-[rgba(255,99,99,0.2)] bg-[rgba(255,99,99,0.1)] text-[#FF6363]",
            )}
          >
            {status.type === "success" ? (
              <CheckCircle size={13} weight="fill" />
            ) : (
              <WarningCircle size={13} weight="fill" />
            )}
            <span className="flex-1 truncate">{status.msg}</span>
          </div>
        )}
      </div>

      {/* Divider */}
      <div className="mx-4 mb-2 mt-4 h-px bg-white/[0.06]" />

      {/* Documents list */}
      <div className="flex-1 overflow-y-auto px-2 pb-4">
        {docs.length === 0 ? (
          <div className="flex flex-col items-center gap-2 px-2 py-6 text-center">
            <FileText size={22} className="text-rc-dark" />
            <p className="text-xs text-rc-dark">还没有摄入文档</p>
            <p className="text-[10px] text-rc-dark opacity-60">
              上传文档后可开始问答
            </p>
          </div>
        ) : (
          <div className="flex flex-col gap-0.5">
            <p className="mb-1 px-2 text-[10px] uppercase tracking-widest text-rc-dark">
              已摄入 ({docs.length})
            </p>
            {docs.map((doc) => (
              <DocRow
                key={doc.id}
                doc={doc}
                onRemove={() =>
                  setDocs((prev) => prev.filter((d) => d.id !== doc.id))
                }
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
