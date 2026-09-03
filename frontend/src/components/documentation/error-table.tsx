import type { ApiErrorDoc } from "@/types/api";

export function ErrorTable({ errors }: { errors: ApiErrorDoc[] }) {
  return (
    <div className="overflow-x-auto rounded-xl border border-border">
      <table className="min-w-full text-left text-sm">
        <thead className="bg-surface text-xs uppercase tracking-wide text-muted-foreground">
          <tr>
            <th className="px-4 py-3 font-medium">Code</th>
            <th className="px-4 py-3 font-medium">HTTP</th>
            <th className="px-4 py-3 font-medium">Description</th>
          </tr>
        </thead>
        <tbody>
          {errors.map((error) => (
            <tr key={error.code} className="border-t border-border">
              <td className="px-4 py-3 font-mono text-xs text-foreground">
                {error.code}
              </td>
              <td className="px-4 py-3 font-mono text-xs text-muted-foreground">
                {error.httpStatus}
              </td>
              <td className="px-4 py-3 text-muted-foreground">
                {error.description}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
