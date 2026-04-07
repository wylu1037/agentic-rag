"use client";

import { cn, formatScore, scoreColor, truncate } from "@/lib/utils";
import type { CitationOut } from "@/lib/api";
import { FileText, LinkSimple, ArrowSquareOut } from "@phosphor-icons/react";
import { useState } from "react";

interface CitationCardProps {
  citation: CitationOut;
  index: number;
}

export function CitationCard({ citation, index }: CitationCardProps) {
  const [expanded, setExpanded] = useState(false);
  const color = scoreColor(citation.score);
  const pct = Math.round(citation.score * 100);

  return (
    <div
      className={cn(
        "group relative overflow-hidden rounded-btn transition-all duration-200",
        "border border-white/[0.06] bg-rc-elevated hover:border-white/10",
      )}
      style={{ animationDelay: `${index * 60}ms` }}
    >
      {/* Score bar — left accent strip */}
      <div
        className="absolute bottom-0 left-0 top-0 w-[2px]"
        style={{ background: color }}
      />

      <div className="py-2.5 pl-4 pr-3">
        {/* Header row */}
        <div className="flex items-start gap-2">
          {/* Score badge */}
          <span
            className="mt-0.5 shrink-0 rounded px-1.5 py-0.5 text-[10px] font-semibold"
            style={{
              color,
              background: `${color}1a`,
              letterSpacing: "0.2px",
              fontVariantNumeric: "tabular-nums",
            }}
          >
            {formatScore(citation.score)}
          </span>

          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-semibold leading-snug text-rc-white">
              {citation.document_title}
            </p>
            {citation.source_section && (
              <p className="mt-0.5 truncate text-[11px] tracking-rc-wide text-rc-dim">
                {citation.source_section}
              </p>
            )}
          </div>

          <button
            onClick={() => setExpanded((v) => !v)}
            className="mt-0.5 shrink-0 text-rc-dark transition-colors hover:text-rc-mid"
            title={expanded ? "收起" : "展开"}
          >
            <ArrowSquareOut size={13} weight="bold" />
          </button>
        </div>

        {/* Source chip */}
        <div className="mt-1.5 flex items-center gap-1">
          <LinkSimple size={10} className="text-rc-dim" />
          <span className="truncate font-mono text-[10px] tracking-rc-wide text-rc-dim">
            {truncate(citation.source, 48)}
          </span>
        </div>

        {/* Score progress bar */}
        <div className="mt-2 h-[2px] overflow-hidden rounded-full bg-white/[0.06]">
          <div
            className="h-full rounded-full transition-all duration-500"
            style={{ width: `${pct}%`, background: color }}
          />
        </div>

        {/* Expanded snippet */}
        {expanded && (
          <div className="mt-2.5 border-t border-white/[0.06] pt-2.5">
            <div className="mb-1.5 flex items-center gap-1">
              <FileText size={11} className="text-rc-dim" />
              <span className="text-[10px] uppercase tracking-widest text-rc-dim">
                内容片段
              </span>
            </div>
            <p className="text-[12px] leading-relaxed text-rc-lt">
              {citation.content_snippet}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
