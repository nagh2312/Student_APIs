"use client";

import { useMemo, useState } from "react";
import type { ApiDefinition } from "@/types/api";
import { API_CATEGORIES } from "@/lib/apis";
import { Input } from "@/components/ui/input";
import { ApiCard } from "@/components/api/api-card";
import { cn } from "@/lib/utils";

export function ApiCatalog({
  apis,
  initialCategory = "all",
  initialQuery = "",
}: {
  apis: ApiDefinition[];
  initialCategory?: string;
  initialQuery?: string;
}) {
  const [query, setQuery] = useState(initialQuery);
  const [category, setCategory] = useState<string>(initialCategory);
  const [status, setStatus] = useState<string>("all");

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return apis.filter((api) => {
      const matchesQuery =
        !q ||
        api.name.toLowerCase().includes(q) ||
        api.description.toLowerCase().includes(q) ||
        api.tags.some((tag) => tag.includes(q)) ||
        api.slug.includes(q);
      const matchesCategory = category === "all" || api.category === category;
      const matchesStatus = status === "all" || api.status === status;
      return matchesQuery && matchesCategory && matchesStatus;
    });
  }, [apis, query, category, status]);

  return (
    <div className="space-y-8">
      <div className="grid gap-4 rounded-2xl border border-border bg-card p-4 shadow-soft sm:p-5">
        <label className="block space-y-2">
          <span className="text-sm font-medium text-foreground">Search APIs</span>
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by name, tag, or description…"
            aria-label="Search APIs"
          />
        </label>

        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div className="space-y-2">
            <p className="text-sm font-medium text-foreground">Category</p>
            <div className="flex flex-wrap gap-2">
              <FilterChip
                active={category === "all"}
                onClick={() => setCategory("all")}
                label="All"
              />
              {API_CATEGORIES.map((cat) => (
                <FilterChip
                  key={cat}
                  active={category === cat}
                  onClick={() => setCategory(cat)}
                  label={cat}
                />
              ))}
            </div>
          </div>
          <div className="space-y-2">
            <p className="text-sm font-medium text-foreground">Status</p>
            <div className="flex flex-wrap gap-2">
              {["all", "stable", "beta"].map((s) => (
                <FilterChip
                  key={s}
                  active={status === s}
                  onClick={() => setStatus(s)}
                  label={s === "all" ? "All" : s}
                />
              ))}
            </div>
          </div>
        </div>
      </div>

      <p className="text-sm text-muted-foreground">
        Showing <span className="font-medium text-foreground">{filtered.length}</span>{" "}
        of {apis.length} APIs
      </p>

      {filtered.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-border bg-surface/50 px-6 py-16 text-center">
          <p className="font-serif text-xl text-foreground">No APIs match</p>
          <p className="mt-2 text-sm text-muted-foreground">
            Try a different search term or clear the filters.
          </p>
        </div>
      ) : (
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {filtered.map((api) => (
            <ApiCard key={api.slug} api={api} />
          ))}
        </div>
      )}
    </div>
  );
}

function FilterChip({
  label,
  active,
  onClick,
}: {
  label: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "rounded-full border px-3 py-1.5 text-xs font-medium capitalize transition",
        active
          ? "border-foreground bg-foreground text-background"
          : "border-border bg-card text-muted-foreground hover:border-foreground/30 hover:text-foreground",
      )}
    >
      {label}
    </button>
  );
}
