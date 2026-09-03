"use client";

import { useCallback, useState } from "react";
import type { TryItResult } from "@/types/api";
import { executeTryIt } from "@/lib/api-client";

export function useApiRequest() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<TryItResult | null>(null);

  const run = useCallback(
    async (options: {
      pathTemplate: string;
      pathParams: Record<string, string>;
      queryParams: Record<string, string>;
      apiKey?: string;
    }) => {
      setLoading(true);
      const next = await executeTryIt(options);
      setResult(next);
      setLoading(false);
      return next;
    },
    [],
  );

  return { loading, result, run, setResult };
}
