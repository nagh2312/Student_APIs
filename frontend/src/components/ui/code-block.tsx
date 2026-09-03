"use client";

import { cn } from "@/lib/utils";
import { useState } from "react";

export function CodeBlock({
  code,
  language = "bash",
  className,
}: {
  code: string;
  language?: string;
  className?: string;
}) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    } catch {
      setCopied(false);
    }
  }

  return (
    <div
      className={cn(
        "group relative overflow-hidden rounded-xl border border-[#1e293b] bg-[#0f172a] shadow-soft",
        className,
      )}
    >
      <div className="flex items-center justify-between border-b border-white/10 px-4 py-2">
        <span className="font-mono text-xs uppercase tracking-wider text-slate-400">
          {language}
        </span>
        <button
          type="button"
          onClick={handleCopy}
          className="rounded-md px-2 py-1 text-xs text-slate-300 transition hover:bg-white/10 hover:text-white"
        >
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <pre className="overflow-x-auto p-4 text-sm leading-relaxed text-slate-100">
        <code className="font-mono">{code}</code>
      </pre>
    </div>
  );
}
