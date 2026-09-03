import Link from "next/link";
import { API_CATEGORIES, APIS, getPopularApis } from "@/lib/apis";
import { API_BASE_URL, GITHUB_URL } from "@/lib/config";
import { ApiCard } from "@/components/api/api-card";
import { Button } from "@/components/ui/button";
import { CodeBlock } from "@/components/ui/code-block";
import { Badge } from "@/components/ui/badge";

const steps = [
  {
    title: "Pick an API",
    body: "Browse the catalog and open the docs for the resource you need.",
  },
  {
    title: "Call /v1",
    body: "Hit the backend with fetch, curl, or your language of choice.",
  },
  {
    title: "Ship your project",
    body: "Use the envelope response and optional API keys for higher limits.",
  },
];

export default function HomePage() {
  const popular = getPopularApis().slice(0, 6);

  return (
    <>
      <section className="relative overflow-hidden border-b border-border">
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 bg-hero-fade"
        />
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 bg-hero-grid bg-[size:48px_48px] opacity-70 [mask-image:linear-gradient(to_bottom,black,transparent_85%)]"
        />
        <div className="container-page relative section-space">
          <div className="mx-auto max-w-3xl text-center animate-fade-up">
            <p className="mb-5 inline-flex items-center gap-2 rounded-full border border-border bg-card/80 px-3 py-1 text-xs font-medium text-muted-foreground shadow-sm backdrop-blur">
              <span className="h-1.5 w-1.5 rounded-full bg-success" />
              Open source · CAMARA-inspired · MIT
            </p>
            <h1 className="font-serif text-4xl tracking-tight text-foreground sm:text-5xl md:text-6xl text-balance">
              Open-source APIs for student developers.
            </h1>
            <p className="mx-auto mt-5 max-w-2xl text-base leading-relaxed text-muted-foreground sm:text-lg">
              Build your project instead of rebuilding the infrastructure.
            </p>
            <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
              <Link href="/apis">
                <Button size="lg">Explore APIs</Button>
              </Link>
              <Link href="/getting-started">
                <Button size="lg" variant="outline">
                  Get Started
                </Button>
              </Link>
              <a href={GITHUB_URL} target="_blank" rel="noopener noreferrer">
                <Button size="lg" variant="ghost">
                  View on GitHub
                </Button>
              </a>
            </div>
          </div>
        </div>
      </section>

      <section className="container-page section-space">
        <div className="mb-8 flex items-end justify-between gap-4">
          <div>
            <h2 className="font-serif text-3xl tracking-tight text-foreground">
              Categories
            </h2>
            <p className="mt-2 text-sm text-muted-foreground">
              Seven Phase 0 APIs across education, geography, weather, and more.
            </p>
          </div>
          <Link
            href="/apis"
            className="hidden text-sm font-medium text-primary hover:underline sm:inline"
          >
            View catalog
          </Link>
        </div>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {API_CATEGORIES.map((category, index) => {
            const count = APIS.filter((api) => api.category === category).length;
            return (
              <Link
                key={category}
                href={`/apis?category=${encodeURIComponent(category)}`}
                className="rounded-2xl border border-border bg-card p-5 shadow-soft transition hover:-translate-y-0.5 hover:shadow-lift"
                style={{ animationDelay: `${index * 60}ms` }}
              >
                <p className="font-serif text-xl text-foreground">{category}</p>
                <p className="mt-1 text-sm text-muted-foreground">
                  {count} API{count === 1 ? "" : "s"}
                </p>
              </Link>
            );
          })}
        </div>
      </section>

      <section className="border-y border-border bg-card/50">
        <div className="container-page section-space">
          <div className="mb-8">
            <h2 className="font-serif text-3xl tracking-tight text-foreground">
              Popular APIs
            </h2>
            <p className="mt-2 text-sm text-muted-foreground">
              Start with the highest-demand endpoints from the Phase 0 portfolio.
            </p>
          </div>
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {popular.map((api) => (
              <ApiCard key={api.slug} api={api} />
            ))}
          </div>
        </div>
      </section>

      <section className="container-page section-space">
        <div className="mb-10 max-w-2xl">
          <h2 className="font-serif text-3xl tracking-tight text-foreground">
            How it works
          </h2>
          <p className="mt-2 text-sm text-muted-foreground">
            One consistent envelope, optional keys, and provider-abstracted data.
          </p>
        </div>
        <ol className="grid gap-5 md:grid-cols-3">
          {steps.map((step, index) => (
            <li
              key={step.title}
              className="rounded-2xl border border-border bg-card p-6 shadow-soft"
            >
              <p className="font-mono text-xs text-muted-foreground">
                Step {String(index + 1).padStart(2, "0")}
              </p>
              <h3 className="mt-3 font-serif text-xl text-foreground">
                {step.title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                {step.body}
              </p>
            </li>
          ))}
        </ol>
      </section>

      <section className="border-y border-border bg-surface/40">
        <div className="container-page section-space grid gap-8 lg:grid-cols-2 lg:items-center">
          <div>
            <Badge tone="accent" className="mb-4">
              Example request
            </Badge>
            <h2 className="font-serif text-3xl tracking-tight text-foreground">
              A clean response on every call
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
              All public endpoints live under{" "}
              <code className="font-mono text-foreground">/v1</code> and return{" "}
              <code className="font-mono text-foreground">
                {"{ data, meta, error }"}
              </code>
              . Point your client at{" "}
              <code className="font-mono text-foreground">{API_BASE_URL}</code>.
            </p>
            <div className="mt-6">
              <Link href="/apis/universities">
                <Button variant="outline">Open Universities docs</Button>
              </Link>
            </div>
          </div>
          <CodeBlock
            language="bash"
            code={`curl -s "${API_BASE_URL}/v1/universities?q=Carnegie&country=US&limit=3" \\
  -H "Accept: application/json"`}
          />
        </div>
      </section>

      <section className="container-page section-space">
        <div className="rounded-3xl border border-border bg-foreground px-6 py-12 text-background sm:px-10">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="font-serif text-3xl tracking-tight sm:text-4xl">
              Contribute an API or a fix
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-white/70 sm:text-base">
              Specs, providers, docs, and portal improvements are welcome. Open an
              issue or PR on GitHub and help the next student ship faster.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              <a href={GITHUB_URL} target="_blank" rel="noopener noreferrer">
                <Button
                  size="lg"
                  className="bg-background text-foreground hover:bg-white"
                >
                  View on GitHub
                </Button>
              </a>
              <Link href="/docs">
                <Button
                  size="lg"
                  variant="outline"
                  className="border-white/25 bg-transparent text-background hover:bg-white/10"
                >
                  Read the docs
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
