import type { TryItResult } from "@/types/api";
import { API_BASE_URL } from "@/lib/config";
import { friendlyApiError } from "@/lib/utils";

function buildUrl(
  pathTemplate: string,
  pathParams: Record<string, string>,
  queryParams: Record<string, string>,
): string {
  let path = pathTemplate;
  for (const [key, value] of Object.entries(pathParams)) {
    path = path.replace(`{${key}}`, encodeURIComponent(value));
  }

  const url = new URL(path, API_BASE_URL);
  for (const [key, value] of Object.entries(queryParams)) {
    if (value.trim() !== "") {
      url.searchParams.set(key, value);
    }
  }
  return url.toString();
}

export async function executeTryIt(options: {
  pathTemplate: string;
  pathParams: Record<string, string>;
  queryParams: Record<string, string>;
  apiKey?: string;
}): Promise<TryItResult> {
  const { pathTemplate, pathParams, queryParams, apiKey } = options;
  const url = buildUrl(pathTemplate, pathParams, queryParams);
  const started = performance.now();

  try {
    const headers: HeadersInit = {
      Accept: "application/json",
    };
    // Optional key via header only — never place secrets in the URL.
    if (apiKey?.trim()) {
      headers["X-API-Key"] = apiKey.trim();
    }

    const response = await fetch(url, {
      method: "GET",
      headers,
      cache: "no-store",
    });

    const durationMs = performance.now() - started;
    const rawText = await response.text();
    let body: unknown = rawText;

    try {
      body = rawText ? JSON.parse(rawText) : null;
    } catch {
      body = rawText;
    }

    const friendly = friendlyApiError(body);

    return {
      url,
      status: response.status,
      statusText: response.statusText,
      durationMs,
      ok: response.ok,
      body,
      rawText,
      errorMessage: friendly || undefined,
    };
  } catch (error) {
    const durationMs = performance.now() - started;
    const message =
      error instanceof Error
        ? error.message
        : "Network error — is the API server running?";

    return {
      url,
      status: null,
      statusText: "Network Error",
      durationMs,
      ok: false,
      body: null,
      rawText: "",
      errorMessage: `Could not reach the API. ${message}`,
    };
  }
}

export { buildUrl };
