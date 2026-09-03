"use client";

import { useMemo, useState, type FormEvent } from "react";
import type { ApiEndpoint, TryItResult } from "@/types/api";
import { executeTryIt, buildUrl } from "@/lib/api-client";
import { formatDuration } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { CodeBlock } from "@/components/ui/code-block";

export function TryItExplorer({ endpoint }: { endpoint: ApiEndpoint }) {
  const pathParams = endpoint.params.filter((p) => p.in === "path");
  const queryParams = endpoint.params.filter((p) => p.in === "query");

  const [values, setValues] = useState<Record<string, string>>(() => {
    const initial: Record<string, string> = {};
    for (const param of endpoint.params) {
      initial[param.name] =
        endpoint.tryItDefaults?.[param.name] ??
        param.example ??
        param.default ??
        "";
    }
    return initial;
  });
  const [apiKey, setApiKey] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<TryItResult | null>(null);

  const previewUrl = useMemo(() => {
    const path: Record<string, string> = {};
    const query: Record<string, string> = {};
    for (const p of pathParams) path[p.name] = values[p.name] || `{${p.name}}`;
    for (const p of queryParams) query[p.name] = values[p.name] || "";
    try {
      return buildUrl(endpoint.path, path, query);
    } catch {
      return endpoint.path;
    }
  }, [endpoint.path, pathParams, queryParams, values]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    const path: Record<string, string> = {};
    const query: Record<string, string> = {};
    for (const p of pathParams) path[p.name] = values[p.name] || "";
    for (const p of queryParams) query[p.name] = values[p.name] || "";

    const missing = pathParams.filter((p) => p.required && !values[p.name]?.trim());
    const missingQuery = queryParams.filter(
      (p) => p.required && !values[p.name]?.trim(),
    );
    if (missing.length || missingQuery.length) {
      setResult({
        url: previewUrl,
        status: null,
        statusText: "Validation",
        durationMs: 0,
        ok: false,
        body: null,
        rawText: "",
        errorMessage: `Missing required parameter(s): ${[...missing, ...missingQuery]
          .map((p) => p.name)
          .join(", ")}`,
      });
      setLoading(false);
      return;
    }

    const res = await executeTryIt({
      pathTemplate: endpoint.path,
      pathParams: path,
      queryParams: query,
      apiKey,
    });
    setResult(res);
    setLoading(false);
  }

  return (
    <div className="space-y-5 rounded-2xl border border-border bg-card p-5 shadow-soft">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="font-serif text-xl text-foreground">Try it</h3>
          <p className="mt-1 text-sm text-muted-foreground">
            Live request against the configured backend. Secrets are never placed
            in the URL.
          </p>
        </div>
        <Badge tone="info" className="font-mono">
          {endpoint.method} {endpoint.path}
        </Badge>
      </div>

      <form onSubmit={onSubmit} className="space-y-4">
        {pathParams.length > 0 ? (
          <fieldset className="space-y-3">
            <legend className="text-sm font-semibold text-foreground">
              Path parameters
            </legend>
            <div className="grid gap-3 sm:grid-cols-2">
              {pathParams.map((param) => (
                <label key={param.name} className="space-y-1.5">
                  <span className="flex items-center gap-2 text-xs font-medium text-muted-foreground">
                    <span className="font-mono text-foreground">{param.name}</span>
                    {param.required ? (
                      <span className="text-danger">required</span>
                    ) : null}
                  </span>
                  <Input
                    value={values[param.name] || ""}
                    onChange={(e) =>
                      setValues((prev) => ({
                        ...prev,
                        [param.name]: e.target.value,
                      }))
                    }
                    placeholder={param.example || param.name}
                  />
                </label>
              ))}
            </div>
          </fieldset>
        ) : null}

        {queryParams.length > 0 ? (
          <fieldset className="space-y-3">
            <legend className="text-sm font-semibold text-foreground">
              Query parameters
            </legend>
            <div className="grid gap-3 sm:grid-cols-2">
              {queryParams.map((param) => (
                <label key={param.name} className="space-y-1.5">
                  <span className="flex items-center gap-2 text-xs font-medium text-muted-foreground">
                    <span className="font-mono text-foreground">{param.name}</span>
                    {param.required ? (
                      <span className="text-danger">required</span>
                    ) : (
                      <span>optional</span>
                    )}
                  </span>
                  <Input
                    value={values[param.name] || ""}
                    onChange={(e) =>
                      setValues((prev) => ({
                        ...prev,
                        [param.name]: e.target.value,
                      }))
                    }
                    placeholder={param.example || param.default || param.name}
                  />
                </label>
              ))}
            </div>
          </fieldset>
        ) : null}

        <label className="block space-y-1.5">
          <span className="text-xs font-medium text-muted-foreground">
            Optional API key{" "}
            <span className="font-normal">(sent as X-API-Key header only)</span>
          </span>
          <Input
            type="password"
            autoComplete="off"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Leave blank for anonymous access"
          />
        </label>

        <div className="rounded-xl border border-border bg-surface px-3 py-2">
          <p className="text-[11px] font-medium uppercase tracking-wide text-muted-foreground">
            Request URL
          </p>
          <p className="mt-1 break-all font-mono text-xs text-foreground">
            {previewUrl}
          </p>
        </div>

        <Button type="submit" disabled={loading} className="w-full sm:w-auto">
          {loading ? "Sending…" : "Try Request"}
        </Button>
      </form>

      {result ? (
        <div className="space-y-3 border-t border-border pt-5">
          <div className="flex flex-wrap items-center gap-2">
            <Badge tone={result.ok ? "success" : "danger"}>
              {result.status ?? "—"} {result.statusText}
            </Badge>
            <Badge tone="neutral">{formatDuration(result.durationMs)}</Badge>
          </div>

          {result.errorMessage ? (
            <Alert tone="danger" title="Request issue">
              {result.errorMessage}
            </Alert>
          ) : null}

          <CodeBlock
            language="json"
            code={
              typeof result.body === "string"
                ? result.body || "(empty response)"
                : JSON.stringify(result.body, null, 2)
            }
          />
        </div>
      ) : null}
    </div>
  );
}
