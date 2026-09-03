import type { Metadata } from "next";
import Link from "next/link";
import { API_BASE_URL, GITHUB_URL } from "@/lib/config";
import { Button } from "@/components/ui/button";
import { CodeBlock } from "@/components/ui/code-block";
import { Alert } from "@/components/ui/alert";

export const metadata: Metadata = {
  title: "Getting Started",
  description: "Go from zero to your first Student API call in five minutes.",
};

const steps = [
  {
    title: "Confirm the API is running",
    body: (
      <>
        Start the FastAPI backend locally (default{" "}
        <code className="font-mono text-foreground">{API_BASE_URL}</code>
        ). Health checks live at{" "}
        <code className="font-mono text-foreground">/health</code>.
      </>
    ),
    code: `curl -s ${API_BASE_URL}/health`,
    language: "bash",
  },
  {
    title: "Make your first request",
    body: (
      <>
        Call a Phase 0 endpoint under{" "}
        <code className="font-mono text-foreground">/v1</code>. Responses always
        use the <code className="font-mono text-foreground">{"{ data, meta, error }"}</code>{" "}
        envelope.
      </>
    ),
    code: `curl -s "${API_BASE_URL}/v1/universities?q=MIT&limit=3" \\
  -H "Accept: application/json"`,
    language: "bash",
  },
  {
    title: "Parse the envelope",
    body: (
      <>
        Read <code className="font-mono text-foreground">data</code> on success.
        On failure, check{" "}
        <code className="font-mono text-foreground">error.code</code> and{" "}
        <code className="font-mono text-foreground">error.message</code> — and keep{" "}
        <code className="font-mono text-foreground">request_id</code> for debugging.
      </>
    ),
    code: `const res = await fetch("${API_BASE_URL}/v1/countries/US");
const json = await res.json();
if (json.error) {
  console.error(json.error.code, json.error.message);
} else {
  console.log(json.data);
}`,
    language: "javascript",
  },
  {
    title: "Optional: raise rate limits with an API key",
    body: (
      <>
        Anonymous traffic is fine for demos. For higher quotas, send{" "}
        <code className="font-mono text-foreground">X-API-Key</code> as a header —
        never in the URL.
      </>
    ),
    code: `curl -s "${API_BASE_URL}/v1/weather/current?lat=40.44&lon=-79.99" \\
  -H "Accept: application/json" \\
  -H "X-API-Key: YOUR_KEY"`,
    language: "bash",
  },
  {
    title: "Explore docs and contribute",
    body: (
      <>
        Open any API page for parameters, examples, and the interactive Try It
        explorer. Found a bug or want a new endpoint? Open a GitHub issue.
      </>
    ),
    code: null,
    language: "bash",
  },
];

export default function GettingStartedPage() {
  return (
    <div className="container-page section-space">
      <div className="mb-12 max-w-2xl">
        <h1 className="font-serif text-4xl tracking-tight text-foreground">
          Getting started
        </h1>
        <p className="mt-3 text-base leading-relaxed text-muted-foreground">
          Five minutes from clone to a successful <code className="font-mono">/v1</code>{" "}
          response.
        </p>
      </div>

      <Alert tone="info" className="mb-10 max-w-3xl" title="Configure the portal">
        Copy <code className="font-mono text-foreground">.env.example</code> to{" "}
        <code className="font-mono text-foreground">.env.local</code> and set{" "}
        <code className="font-mono text-foreground">NEXT_PUBLIC_API_BASE_URL</code>{" "}
        if your backend is not on localhost:8000.
      </Alert>

      <ol className="mx-auto max-w-3xl space-y-8">
        {steps.map((step, index) => (
          <li
            key={step.title}
            className="rounded-2xl border border-border bg-card p-6 shadow-soft"
          >
            <p className="font-mono text-xs text-muted-foreground">
              Step {String(index + 1).padStart(2, "0")}
            </p>
            <h2 className="mt-2 font-serif text-2xl text-foreground">
              {step.title}
            </h2>
            <div className="mt-3 text-sm leading-relaxed text-muted-foreground">
              {step.body}
            </div>
            {step.code ? (
              <div className="mt-5">
                <CodeBlock code={step.code} language={step.language} />
              </div>
            ) : (
              <div className="mt-5 flex flex-wrap gap-3">
                <Link href="/apis">
                  <Button>Browse APIs</Button>
                </Link>
                <a href={GITHUB_URL} target="_blank" rel="noopener noreferrer">
                  <Button variant="outline">GitHub</Button>
                </a>
              </div>
            )}
          </li>
        ))}
      </ol>
    </div>
  );
}
