import Link from "next/link";
import type { ApiDefinition } from "@/types/api";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { StatusBadge } from "@/components/api/status-badge";

export function ApiCard({ api }: { api: ApiDefinition }) {
  return (
    <Card className="group flex h-full flex-col transition duration-300 hover:-translate-y-0.5 hover:shadow-lift">
      <CardHeader>
        <div className="flex items-start justify-between gap-3">
          <div>
            <CardTitle className="text-lg group-hover:text-primary">
              <Link href={`/apis/${api.slug}`}>{api.name}</Link>
            </CardTitle>
            <p className="mt-1 font-mono text-xs text-muted-foreground">
              {api.basePath}
            </p>
          </div>
          <StatusBadge status={api.status} />
        </div>
        <CardDescription className="pt-2">{api.description}</CardDescription>
      </CardHeader>
      <CardContent className="mt-auto space-y-4">
        <div className="flex flex-wrap gap-2">
          <Badge tone="info">{api.category}</Badge>
          <Badge>{api.version}</Badge>
          <Badge tone="accent">{api.auth}</Badge>
        </div>
        <dl className="grid grid-cols-2 gap-3 text-xs text-muted-foreground">
          <div>
            <dt className="font-medium text-foreground">Anonymous</dt>
            <dd className="font-mono">{api.rateLimitAnonymous}</dd>
          </div>
          <div>
            <dt className="font-medium text-foreground">With API key</dt>
            <dd className="font-mono">{api.rateLimitAuthenticated}</dd>
          </div>
        </dl>
        <div className="flex items-center justify-between gap-3 border-t border-border pt-4">
          <Link
            href={`/apis/${api.slug}`}
            className="text-sm font-medium text-primary hover:underline"
          >
            Docs
          </Link>
          <code className="truncate font-mono text-[11px] text-muted-foreground">
            GET {api.endpoints[0]?.path}
          </code>
        </div>
      </CardContent>
    </Card>
  );
}
