import Link from "next/link";
import { GITHUB_URL, SITE_NAME } from "@/lib/config";

export function Footer() {
  return (
    <footer className="mt-auto border-t border-border bg-surface/60">
      <div className="mx-auto grid max-w-6xl gap-8 px-4 py-12 sm:px-6 md:grid-cols-4">
        <div className="md:col-span-2">
          <p className="font-serif text-xl text-foreground">{SITE_NAME}</p>
          <p className="mt-2 max-w-md text-sm leading-relaxed text-muted-foreground">
            Open-source, CAMARA-inspired APIs so student developers can ship
            projects instead of rebuilding infrastructure.
          </p>
        </div>
        <div>
          <p className="text-sm font-semibold text-foreground">Explore</p>
          <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
            <li>
              <Link href="/apis" className="hover:text-foreground">
                API Catalog
              </Link>
            </li>
            <li>
              <Link href="/getting-started" className="hover:text-foreground">
                Getting Started
              </Link>
            </li>
            <li>
              <Link href="/docs" className="hover:text-foreground">
                Documentation
              </Link>
            </li>
            <li>
              <Link href="/status" className="hover:text-foreground">
                Status
              </Link>
            </li>
          </ul>
        </div>
        <div>
          <p className="text-sm font-semibold text-foreground">Community</p>
          <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
            <li>
              <a
                href={GITHUB_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-foreground"
              >
                GitHub
              </a>
            </li>
            <li>
              <a
                href={`${GITHUB_URL}/issues`}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-foreground"
              >
                Issues
              </a>
            </li>
          </ul>
        </div>
      </div>
      <div className="border-t border-border">
        <div className="mx-auto flex max-w-6xl flex-col gap-2 px-4 py-5 text-xs text-muted-foreground sm:flex-row sm:items-center sm:justify-between sm:px-6">
          <p>MIT License. Built for learners and builders.</p>
          <p className="font-mono">/v1 · envelope responses · optional API keys</p>
        </div>
      </div>
    </footer>
  );
}
