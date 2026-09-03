import type { Metadata } from "next";
import Link from "next/link";
import { STATUS_SERVICES } from "@/lib/apis";
import { Badge } from "@/components/ui/badge";

export const metadata: Metadata = {
  title: "Status",
  description: "Operational status for Student API Platform services.",
};

export default function StatusPage() {
  return (
    <div className="container-page section-space">
      <div className="mb-10 max-w-2xl">
        <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-[color-mix(in_srgb,var(--success)_30%,white)] bg-[color-mix(in_srgb,var(--success)_10%,white)] px-3 py-1 text-xs font-medium text-success">
          <span className="h-1.5 w-1.5 rounded-full bg-success" />
          All systems operational
        </div>
        <h1 className="font-serif text-4xl tracking-tight text-foreground">
          API status
        </h1>
        <p className="mt-3 text-base leading-relaxed text-muted-foreground">
          Initial Phase 0 APIs are marked operational. This page will expand with
          live health checks as the platform matures.
        </p>
      </div>

      <div className="overflow-hidden rounded-2xl border border-border bg-card shadow-soft">
        <div className="grid grid-cols-[1fr_auto] gap-4 border-b border-border bg-surface px-5 py-3 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
          <span>Service</span>
          <span>Status</span>
        </div>
        <ul>
          {STATUS_SERVICES.map((service) => (
            <li
              key={service.slug}
              className="grid grid-cols-[1fr_auto] items-center gap-4 border-b border-border px-5 py-4 last:border-b-0"
            >
              <div>
                <Link
                  href={`/apis/${service.slug}`}
                  className="font-medium text-foreground hover:text-primary"
                >
                  {service.name}
                </Link>
                <p className="mt-0.5 text-xs text-muted-foreground">
                  {service.category}
                </p>
              </div>
              <Badge tone="success">Operational</Badge>
            </li>
          ))}
        </ul>
      </div>

      <p className="mt-6 text-sm text-muted-foreground">
        Backend probes:{" "}
        <code className="font-mono text-foreground">/health</code>,{" "}
        <code className="font-mono text-foreground">/health/live</code>,{" "}
        <code className="font-mono text-foreground">/health/ready</code>
      </p>
    </div>
  );
}
