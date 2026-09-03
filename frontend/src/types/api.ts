export type ApiStatus = "stable" | "beta" | "experimental" | "deprecated";
export type ApiCategory =
  | "Education"
  | "Geography"
  | "Weather"
  | "Reference"
  | "Finance"
  | "Utilities";

export type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export interface ApiParam {
  name: string;
  in: "query" | "path" | "header";
  type: string;
  required: boolean;
  description: string;
  example?: string;
  default?: string;
}

export interface ApiEndpoint {
  id: string;
  method: HttpMethod;
  path: string;
  summary: string;
  description: string;
  params: ApiParam[];
  sampleResponse: unknown;
  tryItDefaults?: Record<string, string>;
}

export interface ApiErrorDoc {
  code: string;
  httpStatus: number;
  description: string;
}

export interface ApiDefinition {
  slug: string;
  name: string;
  shortName: string;
  description: string;
  category: ApiCategory;
  version: string;
  status: ApiStatus;
  auth: "None (optional API key)" | "Optional API key";
  rateLimitAnonymous: string;
  rateLimitAuthenticated: string;
  basePath: string;
  tags: string[];
  overview: string[];
  popular?: boolean;
  endpoints: ApiEndpoint[];
  errors: ApiErrorDoc[];
  exampleCurl: string;
  exampleJavascript: string;
  examplePython: string;
}

export interface ApiEnvelope<T = unknown> {
  data: T | null;
  meta: Record<string, unknown>;
  error: {
    code: string;
    message: string;
    details?: unknown;
    request_id?: string;
  } | null;
}

export interface TryItResult {
  url: string;
  status: number | null;
  statusText: string;
  durationMs: number;
  ok: boolean;
  body: unknown;
  rawText: string;
  errorMessage?: string;
}
