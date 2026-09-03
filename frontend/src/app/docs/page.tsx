import type { Metadata } from "next";
import Link from "next/link";
import { APIS } from "@/lib/apis";
import { GITHUB_URL } from "@/lib/config";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export const metadata: Metadata = {
  title: "Documentation",
  description: "Documentation index for the Student API Platform.",
};

const guides = [
  {
    title: "Getting started",
    description: "Five-minute onboarding from health check to first /v1 call.",
    href: "/getting-started",
  },
  {
    title: "API catalog",
    description: "Browse every Phase 0 API with search and category filters.",
    href: "/apis",
  },
  {
    title: "Status page",
    description: "Operational status for the public portfolio.",
    href: "/status",
  },
  {
    title: "GitHub repository",
    description: "Source, specs, contribution guide, and issue tracker.",
    href: GITHUB_URL,
    external: true,
  },
];

export default function DocsPage() {
  return (
    <div className="container-page section-space">
      <div className="mb-12 max-w-2xl">
        <h1 className="font-serif text-4xl tracking-tight text-foreground">
          Documentation
        </h1>
        <p className="mt-3 text-base leading-relaxed text-muted-foreground">
          Start with onboarding, then dive into per-API reference pages with live
          explorers.
        </p>
      </div>

      <section className="mb-14">
        <h2 className="mb-5 font-serif text-2xl text-foreground">Guides</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          {guides.map((guide) => (
            <Card key={guide.title} className="transition hover:shadow-lift">
              <CardHeader>
                <CardTitle className="text-lg">
                  {guide.external ? (
                    <a
                      href={guide.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-primary"
                    >
                      {guide.title}
                    </a>
                  ) : (
                    <Link href={guide.href} className="hover:text-primary">
                      {guide.title}
                    </Link>
                  )}
                </CardTitle>
                <CardDescription>{guide.description}</CardDescription>
              </CardHeader>
            </Card>
          ))}
        </div>
      </section>

      <section>
        <h2 className="mb-5 font-serif text-2xl text-foreground">API reference</h2>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {APIS.map((api) => (
            <Card key={api.slug}>
              <CardContent className="p-5">
                <Link
                  href={`/apis/${api.slug}`}
                  className="font-serif text-lg text-foreground hover:text-primary"
                >
                  {api.name}
                </Link>
                <p className="mt-1 font-mono text-xs text-muted-foreground">
                  {api.basePath}
                </p>
                <p className="mt-2 text-sm text-muted-foreground line-clamp-2">
                  {api.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>
    </div>
  );
}
