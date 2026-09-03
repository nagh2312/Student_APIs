import type { ApiEndpoint } from "@/types/api";
import { Badge } from "@/components/ui/badge";
import { CodeBlock } from "@/components/ui/code-block";
import { ParamTable } from "@/components/documentation/param-table";

export function EndpointDocs({ endpoint }: { endpoint: ApiEndpoint }) {
  return (
    <article className="space-y-5 rounded-2xl border border-border bg-card p-5 shadow-soft">
      <div className="flex flex-wrap items-center gap-2">
        <Badge
          tone={endpoint.method === "GET" ? "success" : "info"}
          className="font-mono"
        >
          {endpoint.method}
        </Badge>
        <code className="font-mono text-sm text-foreground">{endpoint.path}</code>
      </div>
      <div>
        <h3 className="font-serif text-xl text-foreground">{endpoint.summary}</h3>
        <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
          {endpoint.description}
        </p>
      </div>
      <div className="space-y-2">
        <h4 className="text-sm font-semibold text-foreground">Parameters</h4>
        <ParamTable params={endpoint.params} />
      </div>
      <div className="space-y-2">
        <h4 className="text-sm font-semibold text-foreground">
          Example response
        </h4>
        <CodeBlock
          language="json"
          code={JSON.stringify(endpoint.sampleResponse, null, 2)}
        />
      </div>
    </article>
  );
}
