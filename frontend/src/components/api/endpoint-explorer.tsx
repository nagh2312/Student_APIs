"use client";

import { useState } from "react";
import type { ApiEndpoint } from "@/types/api";
import { TryItExplorer } from "@/components/api/try-it-explorer";
import { cn } from "@/lib/utils";

export function EndpointExplorer({ endpoints }: { endpoints: ApiEndpoint[] }) {
  const [activeId, setActiveId] = useState(endpoints[0]?.id);
  const active = endpoints.find((e) => e.id === activeId) || endpoints[0];

  if (!active) return null;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2">
        {endpoints.map((endpoint) => (
          <button
            key={endpoint.id}
            type="button"
            onClick={() => setActiveId(endpoint.id)}
            className={cn(
              "rounded-lg border px-3 py-2 text-left text-xs transition",
              activeId === endpoint.id
                ? "border-foreground bg-foreground text-background"
                : "border-border bg-card text-muted-foreground hover:text-foreground",
            )}
          >
            <span className="font-mono font-semibold">{endpoint.method}</span>{" "}
            <span className="font-mono">{endpoint.path}</span>
          </button>
        ))}
      </div>
      <TryItExplorer key={active.id} endpoint={active} />
    </div>
  );
}
