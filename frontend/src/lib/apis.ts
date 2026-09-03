import type { ApiDefinition, ApiErrorDoc } from "@/types/api";
import { API_BASE_URL } from "@/lib/config";

const commonErrors: ApiErrorDoc[] = [
  {
    code: "VALIDATION_ERROR",
    httpStatus: 400,
    description: "One or more query or path parameters are invalid.",
  },
  {
    code: "RESOURCE_NOT_FOUND",
    httpStatus: 404,
    description: "The requested resource does not exist.",
  },
  {
    code: "RATE_LIMIT_EXCEEDED",
    httpStatus: 429,
    description: "Too many requests. Wait for the rate-limit window to reset.",
  },
  {
    code: "UNAUTHORIZED",
    httpStatus: 401,
    description: "API key is missing or invalid (when a key is required).",
  },
  {
    code: "PROVIDER_ERROR",
    httpStatus: 503,
    description: "An upstream data provider is temporarily unavailable.",
  },
  {
    code: "INTERNAL_ERROR",
    httpStatus: 500,
    description: "Unexpected server error. Include the request_id when reporting.",
  },
];

function examples(path: string, note?: string) {
  const url = `${API_BASE_URL}${path}`;
  const comment = note ? `\n# ${note}` : "";
  return {
    exampleCurl: `curl -s "${url}" \\
  -H "Accept: application/json"${comment}`,
    exampleJavascript: `const res = await fetch("${url}", {
  headers: { Accept: "application/json" },
});
const json = await res.json();
console.log(json.data);`,
    examplePython: `import requests

resp = requests.get(
    "${url}",
    headers={"Accept": "application/json"},
)
resp.raise_for_status()
print(resp.json()["data"])`,
  };
}

export const APIS: ApiDefinition[] = [
  {
    slug: "universities",
    name: "Universities API",
    shortName: "Universities",
    description:
      "Search universities worldwide by name, country, and domain. Ideal for campus apps and education projects.",
    category: "Education",
    version: "v1",
    status: "stable",
    auth: "None (optional API key)",
    rateLimitAnonymous: "60 req/min",
    rateLimitAuthenticated: "300 req/min",
    basePath: "/v1/universities",
    tags: ["education", "search", "open-data"],
    popular: true,
    overview: [
      "Query a normalized catalog of universities with country codes, websites, and domains.",
      "Anonymous read access is enabled. Attach an optional X-API-Key header for higher rate limits.",
      "Responses use the standard platform envelope: { data, meta, error }.",
    ],
    endpoints: [
      {
        id: "list-universities",
        method: "GET",
        path: "/v1/universities",
        summary: "List / search universities",
        description:
          "Paginated search across universities. Filter by country or free-text name.",
        params: [
          {
            name: "q",
            in: "query",
            type: "string",
            required: false,
            description: "Free-text search (name).",
            example: "Carnegie",
          },
          {
            name: "country",
            in: "query",
            type: "string",
            required: false,
            description: "ISO 3166-1 alpha-2 country code.",
            example: "US",
          },
          {
            name: "page",
            in: "query",
            type: "integer",
            required: false,
            description: "Page number (1-based).",
            default: "1",
            example: "1",
          },
          {
            name: "limit",
            in: "query",
            type: "integer",
            required: false,
            description: "Page size (max 100).",
            default: "20",
            example: "10",
          },
        ],
        tryItDefaults: { q: "Carnegie", country: "US", page: "1", limit: "5" },
        sampleResponse: {
          data: [
            {
              id: "cmu",
              name: "Carnegie Mellon University",
              country: "United States",
              country_code: "US",
              state: "Pennsylvania",
              city: "Pittsburgh",
              website: "https://www.cmu.edu",
              domains: ["cmu.edu"],
            },
          ],
          meta: {
            request_id: "req_demo",
            page: 1,
            limit: 5,
            total: 1,
            has_next: false,
            has_prev: false,
          },
          error: null,
        },
      },
      {
        id: "get-university",
        method: "GET",
        path: "/v1/universities/{id}",
        summary: "Get university by ID",
        description: "Fetch a single university record by stable identifier.",
        params: [
          {
            name: "id",
            in: "path",
            type: "string",
            required: true,
            description: "University ID.",
            example: "cmu",
          },
        ],
        tryItDefaults: { id: "cmu" },
        sampleResponse: {
          data: {
            id: "cmu",
            name: "Carnegie Mellon University",
            country: "United States",
            country_code: "US",
            website: "https://www.cmu.edu",
            domains: ["cmu.edu"],
          },
          meta: { request_id: "req_demo" },
          error: null,
        },
      },
    ],
    errors: commonErrors,
    ...examples("/v1/universities?q=Carnegie&country=US&limit=5"),
  },
  {
    slug: "countries",
    name: "Countries API",
    shortName: "Countries",
    description:
      "Country metadata: names, codes, capitals, regions, languages, currencies, and timezones.",
    category: "Geography",
    version: "v1",
    status: "stable",
    auth: "None (optional API key)",
    rateLimitAnonymous: "60 req/min",
    rateLimitAuthenticated: "300 req/min",
    basePath: "/v1/countries",
    tags: ["geography", "reference", "metadata"],
    popular: true,
    overview: [
      "Look up countries by ISO code or search by name/region.",
      "Useful as a shared reference layer for almost any student project.",
      "Data is seeded from open country datasets; live providers are abstracted.",
    ],
    endpoints: [
      {
        id: "list-countries",
        method: "GET",
        path: "/v1/countries",
        summary: "List / search countries",
        description: "Paginated country catalog with optional region filter.",
        params: [
          {
            name: "q",
            in: "query",
            type: "string",
            required: false,
            description: "Search by common or official name.",
            example: "united",
          },
          {
            name: "region",
            in: "query",
            type: "string",
            required: false,
            description: "Region filter (e.g. Europe, Asia).",
            example: "Europe",
          },
          {
            name: "page",
            in: "query",
            type: "integer",
            required: false,
            default: "1",
            description: "Page number.",
            example: "1",
          },
          {
            name: "limit",
            in: "query",
            type: "integer",
            required: false,
            default: "20",
            description: "Page size (max 100).",
            example: "10",
          },
        ],
        tryItDefaults: { q: "united", limit: "5" },
        sampleResponse: {
          data: [
            {
              name: "United States",
              cca2: "US",
              cca3: "USA",
              capital: "Washington, D.C.",
              region: "Americas",
              subregion: "North America",
            },
          ],
          meta: { request_id: "req_demo", page: 1, limit: 5, total: 1 },
          error: null,
        },
      },
      {
        id: "get-country",
        method: "GET",
        path: "/v1/countries/{code}",
        summary: "Get country by code",
        description: "Fetch a country by ISO 3166-1 alpha-2 or alpha-3 code.",
        params: [
          {
            name: "code",
            in: "path",
            type: "string",
            required: true,
            description: "Country code (cca2 or cca3).",
            example: "US",
          },
        ],
        tryItDefaults: { code: "US" },
        sampleResponse: {
          data: {
            name: "United States",
            cca2: "US",
            capital: "Washington, D.C.",
            currencies: ["USD"],
            timezones: ["UTC-12:00", "UTC-04:00"],
          },
          meta: { request_id: "req_demo" },
          error: null,
        },
      },
    ],
    errors: commonErrors,
    ...examples("/v1/countries?q=united&limit=5"),
  },
  {
    slug: "geography",
    name: "Geography API",
    shortName: "Geography",
    description:
      "Geocoding, reverse geocoding, and great-circle distance for maps and location features.",
    category: "Geography",
    version: "v1",
    status: "beta",
    auth: "None (optional API key)",
    rateLimitAnonymous: "60 req/min",
    rateLimitAuthenticated: "300 req/min",
    basePath: "/v1/geography",
    tags: ["geocode", "maps", "distance"],
    popular: true,
    overview: [
      "Forward and reverse geocode place names and coordinates.",
      "Compute haversine distance between two WGS84 points.",
      "Respect upstream provider rate limits; responses may be cached.",
    ],
    endpoints: [
      {
        id: "geocode",
        method: "GET",
        path: "/v1/geography/geocode",
        summary: "Forward geocode",
        description: "Resolve a place query to latitude/longitude.",
        params: [
          {
            name: "q",
            in: "query",
            type: "string",
            required: true,
            description: "Place name or address fragment.",
            example: "Pittsburgh, PA",
          },
          {
            name: "limit",
            in: "query",
            type: "integer",
            required: false,
            default: "5",
            description: "Max results.",
            example: "3",
          },
        ],
        tryItDefaults: { q: "Pittsburgh, PA", limit: "3" },
        sampleResponse: {
          data: [
            {
              display_name: "Pittsburgh, Allegheny County, Pennsylvania, USA",
              lat: 40.4406,
              lon: -79.9959,
            },
          ],
          meta: { request_id: "req_demo" },
          error: null,
        },
      },
      {
        id: "reverse",
        method: "GET",
        path: "/v1/geography/reverse",
        summary: "Reverse geocode",
        description: "Resolve coordinates to a human-readable place.",
        params: [
          {
            name: "lat",
            in: "query",
            type: "number",
            required: true,
            description: "Latitude.",
            example: "40.4406",
          },
          {
            name: "lon",
            in: "query",
            type: "number",
            required: true,
            description: "Longitude.",
            example: "-79.9959",
          },
        ],
        tryItDefaults: { lat: "40.4406", lon: "-79.9959" },
        sampleResponse: {
          data: {
            display_name: "Pittsburgh, Pennsylvania, United States",
            lat: 40.4406,
            lon: -79.9959,
          },
          meta: { request_id: "req_demo" },
          error: null,
        },
      },
      {
        id: "distance",
        method: "GET",
        path: "/v1/geography/distance",
        summary: "Distance between points",
        description: "Haversine distance in kilometers between two coordinates.",
        params: [
          {
            name: "from_lat",
            in: "query",
            type: "number",
            required: true,
            description: "Origin latitude.",
            example: "40.4406",
          },
          {
            name: "from_lon",
            in: "query",
            type: "number",
            required: true,
            description: "Origin longitude.",
            example: "-79.9959",
          },
          {
            name: "to_lat",
            in: "query",
            type: "number",
            required: true,
            description: "Destination latitude.",
            example: "42.3601",
          },
          {
            name: "to_lon",
            in: "query",
            type: "number",
            required: true,
            description: "Destination longitude.",
            example: "-71.0589",
          },
        ],
        tryItDefaults: {
          from_lat: "40.4406",
          from_lon: "-79.9959",
          to_lat: "42.3601",
          to_lon: "-71.0589",
        },
        sampleResponse: {
          data: { kilometers: 777.4, meters: 777400 },
          meta: { request_id: "req_demo" },
          error: null,
        },
      },
    ],
    errors: commonErrors,
    ...examples("/v1/geography/geocode?q=Pittsburgh%2C%20PA&limit=3"),
  },
  {
    slug: "weather",
    name: "Weather API",
    shortName: "Weather",
    description:
      "Current conditions and short-range forecasts for dashboards, travel, and IoT demos.",
    category: "Weather",
    version: "v1",
    status: "stable",
    auth: "None (optional API key)",
    rateLimitAnonymous: "60 req/min",
    rateLimitAuthenticated: "300 req/min",
    basePath: "/v1/weather",
    tags: ["weather", "forecast", "climate"],
    popular: true,
    overview: [
      "Normalized weather payloads independent of the upstream provider.",
      "Default live provider is Open-Meteo; mock mode returns deterministic samples.",
      "Coordinates are required — pair with the Geography API to geocode a city first.",
    ],
    endpoints: [
      {
        id: "current-weather",
        method: "GET",
        path: "/v1/weather/current",
        summary: "Current weather",
        description: "Current temperature, wind, and conditions for a location.",
        params: [
          {
            name: "lat",
            in: "query",
            type: "number",
            required: true,
            description: "Latitude.",
            example: "40.44",
          },
          {
            name: "lon",
            in: "query",
            type: "number",
            required: true,
            description: "Longitude.",
            example: "-79.99",
          },
          {
            name: "units",
            in: "query",
            type: "string",
            required: false,
            default: "metric",
            description: "metric or imperial.",
            example: "metric",
          },
        ],
        tryItDefaults: { lat: "40.44", lon: "-79.99", units: "metric" },
        sampleResponse: {
          data: {
            temperature_c: 18.2,
            wind_speed_kmh: 12.4,
            condition: "Partly cloudy",
            observed_at: "2026-09-02T18:00:00Z",
          },
          meta: { request_id: "req_demo" },
          error: null,
        },
      },
      {
        id: "forecast",
        method: "GET",
        path: "/v1/weather/forecast",
        summary: "Weather forecast",
        description: "Daily forecast for the next several days.",
        params: [
          {
            name: "lat",
            in: "query",
            type: "number",
            required: true,
            description: "Latitude.",
            example: "40.44",
          },
          {
            name: "lon",
            in: "query",
            type: "number",
            required: true,
            description: "Longitude.",
            example: "-79.99",
          },
          {
            name: "days",
            in: "query",
            type: "integer",
            required: false,
            default: "5",
            description: "Number of forecast days (1–7).",
            example: "3",
          },
        ],
        tryItDefaults: { lat: "40.44", lon: "-79.99", days: "3" },
        sampleResponse: {
          data: {
            days: [
              { date: "2026-09-03", high_c: 22, low_c: 14, condition: "Clear" },
              { date: "2026-09-04", high_c: 20, low_c: 13, condition: "Rain" },
            ],
          },
          meta: { request_id: "req_demo" },
          error: null,
        },
      },
    ],
    errors: commonErrors,
    ...examples("/v1/weather/current?lat=40.44&lon=-79.99&units=metric"),
  },
  {
    slug: "books",
    name: "Books API",
    shortName: "Books",
    description:
      "Search books and fetch metadata for library, reading list, and catalog projects.",
    category: "Reference",
    version: "v1",
    status: "stable",
    auth: "None (optional API key)",
    rateLimitAnonymous: "60 req/min",
    rateLimitAuthenticated: "300 req/min",
    basePath: "/v1/books",
    tags: ["books", "library", "search"],
    popular: true,
    overview: [
      "Search titles, authors, and subjects via a provider-abstracted interface.",
      "Default live provider is Open Library; mock mode ships sample titles.",
      "Prefer linking cover art rather than hotlinking aggressively.",
    ],
    endpoints: [
      {
        id: "search-books",
        method: "GET",
        path: "/v1/books/search",
        summary: "Search books",
        description: "Full-text search across book metadata.",
        params: [
          {
            name: "q",
            in: "query",
            type: "string",
            required: true,
            description: "Search query.",
            example: "design patterns",
          },
          {
            name: "limit",
            in: "query",
            type: "integer",
            required: false,
            default: "20",
            description: "Max results.",
            example: "5",
          },
        ],
        tryItDefaults: { q: "design patterns", limit: "5" },
        sampleResponse: {
          data: [
            {
              id: "OL123M",
              title: "Design Patterns",
              authors: ["Erich Gamma"],
              publish_year: 1994,
            },
          ],
          meta: { request_id: "req_demo" },
          error: null,
        },
      },
      {
        id: "get-book",
        method: "GET",
        path: "/v1/books/{id}",
        summary: "Get book by ID",
        description: "Fetch a single book record by provider ID.",
        params: [
          {
            name: "id",
            in: "path",
            type: "string",
            required: true,
            description: "Book identifier.",
            example: "OL123M",
          },
        ],
        tryItDefaults: { id: "OL123M" },
        sampleResponse: {
          data: {
            id: "OL123M",
            title: "Design Patterns",
            authors: ["Erich Gamma", "Richard Helm"],
            subjects: ["Software engineering"],
          },
          meta: { request_id: "req_demo" },
          error: null,
        },
      },
    ],
    errors: commonErrors,
    ...examples("/v1/books/search?q=design%20patterns&limit=5"),
  },
  {
    slug: "currency",
    name: "Currency API",
    shortName: "Currency",
    description:
      "FX reference rates and currency conversion powered by open ECB-sourced data.",
    category: "Finance",
    version: "v1",
    status: "stable",
    auth: "None (optional API key)",
    rateLimitAnonymous: "60 req/min",
    rateLimitAuthenticated: "300 req/min",
    basePath: "/v1/currency",
    tags: ["fx", "finance", "conversion"],
    popular: true,
    overview: [
      "Fetch latest or base-relative exchange rates.",
      "Convert an amount between two currencies in one call.",
      "Rates are cached; treat values as reference rates, not trading quotes.",
    ],
    endpoints: [
      {
        id: "rates",
        method: "GET",
        path: "/v1/currency/rates",
        summary: "Latest FX rates",
        description: "Rates relative to a base currency.",
        params: [
          {
            name: "base",
            in: "query",
            type: "string",
            required: false,
            default: "USD",
            description: "Base currency code.",
            example: "USD",
          },
          {
            name: "symbols",
            in: "query",
            type: "string",
            required: false,
            description: "Comma-separated quote currencies.",
            example: "EUR,GBP,JPY",
          },
        ],
        tryItDefaults: { base: "USD", symbols: "EUR,GBP,JPY" },
        sampleResponse: {
          data: {
            base: "USD",
            date: "2026-09-01",
            rates: { EUR: 0.92, GBP: 0.78, JPY: 149.2 },
          },
          meta: { request_id: "req_demo" },
          error: null,
        },
      },
      {
        id: "convert",
        method: "GET",
        path: "/v1/currency/convert",
        summary: "Convert amount",
        description: "Convert an amount from one currency to another.",
        params: [
          {
            name: "amount",
            in: "query",
            type: "number",
            required: true,
            description: "Amount to convert.",
            example: "100",
          },
          {
            name: "from",
            in: "query",
            type: "string",
            required: true,
            description: "Source currency.",
            example: "USD",
          },
          {
            name: "to",
            in: "query",
            type: "string",
            required: true,
            description: "Target currency.",
            example: "EUR",
          },
        ],
        tryItDefaults: { amount: "100", from: "USD", to: "EUR" },
        sampleResponse: {
          data: {
            amount: 100,
            from: "USD",
            to: "EUR",
            result: 92.0,
            rate: 0.92,
          },
          meta: { request_id: "req_demo" },
          error: null,
        },
      },
    ],
    errors: commonErrors,
    ...examples("/v1/currency/convert?amount=100&from=USD&to=EUR"),
  },
  {
    slug: "time",
    name: "Time API",
    shortName: "Time",
    description:
      "Current time, timezone listings, and conversions for scheduling and world clocks.",
    category: "Utilities",
    version: "v1",
    status: "beta",
    auth: "None (optional API key)",
    rateLimitAnonymous: "60 req/min",
    rateLimitAuthenticated: "300 req/min",
    basePath: "/v1/time",
    tags: ["time", "timezone", "scheduling"],
    popular: false,
    overview: [
      "Get the current time in any IANA timezone.",
      "List common zones and convert timestamps between zones.",
      "Low-maintenance utility API — great first integration for new projects.",
    ],
    endpoints: [
      {
        id: "now",
        method: "GET",
        path: "/v1/time/now",
        summary: "Current time",
        description: "Current wall-clock time for a timezone.",
        params: [
          {
            name: "timezone",
            in: "query",
            type: "string",
            required: false,
            default: "UTC",
            description: "IANA timezone name.",
            example: "America/New_York",
          },
        ],
        tryItDefaults: { timezone: "America/New_York" },
        sampleResponse: {
          data: {
            timezone: "America/New_York",
            datetime: "2026-09-02T14:30:00-04:00",
            utc_offset: "-04:00",
            unix: 1788369000,
          },
          meta: { request_id: "req_demo" },
          error: null,
        },
      },
      {
        id: "zones",
        method: "GET",
        path: "/v1/time/zones",
        summary: "List timezones",
        description: "List supported IANA timezones (optionally filtered).",
        params: [
          {
            name: "q",
            in: "query",
            type: "string",
            required: false,
            description: "Filter zones by substring.",
            example: "America/",
          },
        ],
        tryItDefaults: { q: "America/" },
        sampleResponse: {
          data: ["America/New_York", "America/Chicago", "America/Denver"],
          meta: { request_id: "req_demo" },
          error: null,
        },
      },
      {
        id: "convert-time",
        method: "GET",
        path: "/v1/time/convert",
        summary: "Convert between zones",
        description: "Convert an ISO-8601 timestamp from one zone to another.",
        params: [
          {
            name: "datetime",
            in: "query",
            type: "string",
            required: true,
            description: "ISO-8601 datetime.",
            example: "2026-09-02T14:30:00",
          },
          {
            name: "from",
            in: "query",
            type: "string",
            required: true,
            description: "Source timezone.",
            example: "America/New_York",
          },
          {
            name: "to",
            in: "query",
            type: "string",
            required: true,
            description: "Target timezone.",
            example: "Europe/London",
          },
        ],
        tryItDefaults: {
          datetime: "2026-09-02T14:30:00",
          from: "America/New_York",
          to: "Europe/London",
        },
        sampleResponse: {
          data: {
            from: {
              timezone: "America/New_York",
              datetime: "2026-09-02T14:30:00-04:00",
            },
            to: {
              timezone: "Europe/London",
              datetime: "2026-09-02T19:30:00+01:00",
            },
          },
          meta: { request_id: "req_demo" },
          error: null,
        },
      },
    ],
    errors: commonErrors,
    ...examples("/v1/time/now?timezone=America%2FNew_York"),
  },
];

export const API_CATEGORIES = Array.from(
  new Set(APIS.map((api) => api.category)),
).sort();

export function getApiBySlug(slug: string): ApiDefinition | undefined {
  return APIS.find((api) => api.slug === slug);
}

export function getPopularApis(): ApiDefinition[] {
  return APIS.filter((api) => api.popular);
}

export const STATUS_SERVICES = APIS.map((api) => ({
  name: api.name,
  slug: api.slug,
  status: "operational" as const,
  category: api.category,
}));
