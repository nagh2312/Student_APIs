"use client";

import { cn } from "@/lib/utils";
import { useState, type ReactNode } from "react";

export interface TabItem {
  id: string;
  label: string;
  content: ReactNode;
}

export function Tabs({
  items,
  defaultTab,
  className,
}: {
  items: TabItem[];
  defaultTab?: string;
  className?: string;
}) {
  const [active, setActive] = useState(defaultTab || items[0]?.id);

  return (
    <div className={cn("space-y-4", className)}>
      <div
        role="tablist"
        className="flex flex-wrap gap-1 rounded-xl border border-border bg-surface p-1"
      >
        {items.map((item) => (
          <button
            key={item.id}
            role="tab"
            type="button"
            aria-selected={active === item.id}
            onClick={() => setActive(item.id)}
            className={cn(
              "rounded-lg px-3 py-2 text-sm font-medium transition",
              active === item.id
                ? "bg-card text-foreground shadow-sm"
                : "text-muted-foreground hover:text-foreground",
            )}
          >
            {item.label}
          </button>
        ))}
      </div>
      <div role="tabpanel">
        {items.find((item) => item.id === active)?.content}
      </div>
    </div>
  );
}
