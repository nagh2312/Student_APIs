import type { ApiParam } from "@/types/api";
import { Badge } from "@/components/ui/badge";

export function ParamTable({ params }: { params: ApiParam[] }) {
  if (!params.length) {
    return (
      <p className="text-sm text-muted-foreground">No parameters for this endpoint.</p>
    );
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-border">
      <table className="min-w-full text-left text-sm">
        <thead className="bg-surface text-xs uppercase tracking-wide text-muted-foreground">
          <tr>
            <th className="px-4 py-3 font-medium">Name</th>
            <th className="px-4 py-3 font-medium">In</th>
            <th className="px-4 py-3 font-medium">Type</th>
            <th className="px-4 py-3 font-medium">Required</th>
            <th className="px-4 py-3 font-medium">Description</th>
          </tr>
        </thead>
        <tbody>
          {params.map((param) => (
            <tr key={`${param.in}-${param.name}`} className="border-t border-border">
              <td className="px-4 py-3 font-mono text-xs text-foreground">
                {param.name}
              </td>
              <td className="px-4 py-3">
                <Badge>{param.in}</Badge>
              </td>
              <td className="px-4 py-3 font-mono text-xs text-muted-foreground">
                {param.type}
              </td>
              <td className="px-4 py-3 text-muted-foreground">
                {param.required ? "yes" : "no"}
              </td>
              <td className="px-4 py-3 text-muted-foreground">
                {param.description}
                {param.example ? (
                  <span className="mt-1 block font-mono text-[11px]">
                    e.g. {param.example}
                  </span>
                ) : null}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
