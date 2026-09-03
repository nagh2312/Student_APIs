import type { Metadata } from "next";
import { APIS, API_CATEGORIES } from "@/lib/apis";
import type { ApiCategory } from "@/types/api";
import { ApiCatalog } from "@/components/api/api-catalog";

export const metadata: Metadata = {
  title: "API Catalog",
  description:
    "Browse Student APIs — universities, countries, geography, weather, books, currency, and time.",
};

type PageProps = {
  searchParams: Promise<{ category?: string; q?: string }>;
};

export default async function ApisPage({ searchParams }: PageProps) {
  const params = await searchParams;
  const category =
    params.category &&
    (API_CATEGORIES as ApiCategory[]).includes(params.category as ApiCategory)
      ? params.category
      : "all";

  return (
    <div className="container-page section-space">
      <div className="mb-10 max-w-2xl">
        <h1 className="font-serif text-4xl tracking-tight text-foreground">
          API Catalog
        </h1>
        <p className="mt-3 text-base leading-relaxed text-muted-foreground">
          Search and filter the Phase 0 portfolio. Every API documents auth, rate
          limits, examples, and an interactive explorer.
        </p>
      </div>
      <ApiCatalog
        apis={APIS}
        initialCategory={category}
        initialQuery={params.q || ""}
      />
    </div>
  );
}
