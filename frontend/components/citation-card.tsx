"use client";

import { cn, formatScore, scoreColor, truncate } from "@/lib/utils";
import type { CitationOut } from "@/lib/api";
import {
  FileText,
  LinkSimple,
  ArrowSquareOut,
} from "@phosphor-icons/react";
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
        "group relative rounded-btn overflow-hidden transition-all duration-200",
        "border border-white/[0.06] bg-rc-elevated hover:border-white/10",
      )}
      style={{ animationDelay: `${index * 60}ms` }}
    >
      {/* Score bar — left accent strip */}
      <div
        className="absolute left-0 top-0 bottom-0 w-[2px]"
        style={{ background: color }}
      />

      <div className="pl-4 pr-3 py-2.5">
        {/* Header row */}
        <div className="flex items-start gap-2">
          {/* Score badge */}
          <span
            className="mt-0.5 shrink-0 text-[10px] font-semibold rounded px-1.5 py-0.5"
            style={{
              color,
              background: `${color}1a`,
              letterSpacing: "0.2px",
              fontVariantNumeric: "tabular-nums",
            }}
          >
            {formatScore(citation.score)}
          </span>

          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold text-rc-white leading-snug truncate">
              {citation.document_title}
            </p>
            {citation.source_section && (
              <p className="text-[11px] text-rc-dim tracking-rc-wide mt-0.5 truncate">
                {citation.source_section}
              </p>
            )}
          </div>

          <button
            onClick={() => setExpanded((v) => !v)}
            className="shrink-0 text-rc-dark hover:text-rc-mid transition-colors mt-0.5"
            title={expanded ? "收起" : "展开"}
          >
            <ArrowSquareOut size={13} weight="bold" />
          </button>
        </div>

        {/* Source chip */}
        <div className="mt-1.5 flex items-center gap-1">
          <LinkSimple size={10} className="text-rc-dim" />
          <span className="text-[10px] text-rc-dim tracking-rc-wide font-mono truncate">
            {truncate(citation.source, 48)}
          </span>
        </div>

        {/* Score progress bar */}
        <div className="mt-2 h-[2px] rounded-full bg-white/[0.06] overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-500"
            style={{ width: `${pct}%`, background: color }}
          />
        </div>

        {/* Expanded snippet */}
        {expanded && (
          <div className="mt-2.5 pt-2.5 border-t border-white/[0.06]">
            <div className="flex items-center gap-1 mb-1.5">
              <FileText size={11} className="text-rc-dim" />
              <span className="text-[10px] text-rc-dim uppercase tracking-widest">
                内容片段
              </span>
            </div>
            <p className="text-[12px] text-rc-lt leading-relaxed">
              {citation.content_snippet}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
