import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { APIS, getApiBySlug } from "@/lib/apis";
import { API_BASE_URL } from "@/lib/config";
import { Badge } from "@/components/ui/badge";
import { StatusBadge } from "@/components/api/status-badge";
import { DocsSection } from "@/components/documentation/docs-section";
import { EndpointDocs } from "@/components/documentation/endpoint-docs";
import { ErrorTable } from "@/components/documentation/error-table";
import { LanguageExamples } from "@/components/code-examples/language-examples";
import { EndpointExplorer } from "@/components/api/endpoint-explorer";
import { Alert } from "@/components/ui/alert";

type PageProps = {
  params: Promise<{ slug: string }>;
};

export function generateStaticParams() {
  return APIS.map((api) => ({ slug: api.slug }));
}

export async function generateMetadata({
  params,
}: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const api = getApiBySlug(slug);
  if (!api) return { title: "API not found" };
  return {
    title: api.name,
    description: api.description,
  };
}

export default async function ApiDetailPage({ params }: PageProps) {
  const { slug } = await params;
  const api = getApiBySlug(slug);
  if (!api) notFound();

  return (
    <div className="container-page section-space">
      <div className="mb-6 text-sm text-muted-foreground">
        <Link href="/apis" className="hover:text-foreground">
          APIs
        </Link>
        <span className="mx-2">/</span>
        <span className="text-foreground">{api.shortName}</span>
      </div>

      <header className="mb-12 max-w-3xl space-y-4">
        <div className="flex flex-wrap items-center gap-2">
          <StatusBadge status={api.status} />
          <Badge tone="info">{api.category}</Badge>
          <Badge>{api.version}</Badge>
        </div>
        <h1 className="font-serif text-4xl tracking-tight text-foreground sm:text-5xl">
          {api.name}
        </h1>
        <p className="text-base leading-relaxed text-muted-foreground">
          {api.description}
        </p>
        <dl className="grid gap-4 rounded-2xl border border-border bg-card p-5 text-sm sm:grid-cols-3">
          <div>
            <dt className="text-muted-foreground">Auth</dt>
            <dd className="mt-1 font-medium text-foreground">{api.auth}</dd>
          </div>
          <div>
            <dt className="text-muted-foreground">Anonymous limit</dt>
            <dd className="mt-1 font-mono text-foreground">
              {api.rateLimitAnonymous}
            </dd>
          </div>
          <div>
            <dt className="text-muted-foreground">Base path</dt>
            <dd className="mt-1 font-mono text-foreground">
              {API_BASE_URL}
              {api.basePath}
            </dd>
          </div>
        </dl>
      </header>

      <div className="grid gap-14 lg:grid-cols-[220px_minmax(0,1fr)]">
        <aside className="hidden lg:block">
          <nav className="sticky top-24 space-y-2 text-sm">
            <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              On this page
            </p>
            {[
              ["overview", "Overview"],
              ["auth", "Authentication"],
              ["endpoints", "Endpoints"],
              ["examples", "Code examples"],
              ["try-it", "Try it"],
              ["errors", "Errors"],
              ["rate-limits", "Rate limits"],
            ].map(([id, label]) => (
              <a
                key={id}
                href={`#${id}`}
                className="block rounded-md px-2 py-1.5 text-muted-foreground hover:bg-surface hover:text-foreground"
              >
                {label}
              </a>
            ))}
          </nav>
        </aside>

        <div className="space-y-14">
          <DocsSection id="overview" title="Overview">
            <ul className="list-disc space-y-2 pl-5">
              {api.overview.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </DocsSection>

          <DocsSection id="auth" title="Authentication">
            <p>
              Most read endpoints allow anonymous access. To raise rate limits,
              send an API key in the{" "}
              <code className="font-mono text-foreground">X-API-Key</code>{" "}
              header — never as a query parameter.
            </p>
            <Alert tone="info" title="Do not expose secrets">
              The Try It explorer keeps optional keys in the request header only.
              Do not commit keys or paste them into shared URLs.
            </Alert>
          </DocsSection>

          <DocsSection id="endpoints" title="Endpoints">
            <div className="space-y-6">
              {api.endpoints.map((endpoint) => (
                <EndpointDocs key={endpoint.id} endpoint={endpoint} />
              ))}
            </div>
          </DocsSection>

          <DocsSection id="examples" title="Code examples">
            <LanguageExamples
              curl={api.exampleCurl}
              javascript={api.exampleJavascript}
              python={api.examplePython}
            />
          </DocsSection>

          <DocsSection id="try-it" title="Interactive explorer">
            <EndpointExplorer endpoints={api.endpoints} />
          </DocsSection>

          <DocsSection id="errors" title="Errors">
            <p>
              Errors use the same envelope with{" "}
              <code className="font-mono text-foreground">data: null</code> and a
              structured <code className="font-mono text-foreground">error</code>{" "}
              object. Include <code className="font-mono text-foreground">request_id</code>{" "}
              when asking for help.
            </p>
            <ErrorTable errors={api.errors} />
          </DocsSection>

          <DocsSection id="rate-limits" title="Rate limits">
            <ul className="list-disc space-y-2 pl-5">
              <li>
                Anonymous:{" "}
                <span className="font-mono text-foreground">
                  {api.rateLimitAnonymous}
                </span>
              </li>
              <li>
                With API key:{" "}
                <span className="font-mono text-foreground">
                  {api.rateLimitAuthenticated}
                </span>
              </li>
              <li>
                Response headers:{" "}
                <code className="font-mono text-foreground">
                  X-RateLimit-Limit
                </code>
                ,{" "}
                <code className="font-mono text-foreground">
                  X-RateLimit-Remaining
                </code>
                ,{" "}
                <code className="font-mono text-foreground">
                  X-RateLimit-Reset
                </code>
              </li>
            </ul>
          </DocsSection>
        </div>
      </div>
    </div>
  );
}
