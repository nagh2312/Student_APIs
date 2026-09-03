import type { ApiStatus } from "@/types/api";
import { Badge } from "@/components/ui/badge";

const statusTone: Record<
  ApiStatus,
  "success" | "warning" | "info" | "neutral"
> = {
  stable: "success",
  beta: "warning",
  experimental: "info",
  deprecated: "neutral",
};

export function StatusBadge({ status }: { status: ApiStatus }) {
  return (
    <Badge tone={statusTone[status]} className="capitalize">
      {status}
    </Badge>
  );
}
