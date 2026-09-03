# Data Sources

Every external dataset or provider used by this platform.

**Rule:** If licensing is unclear, do not include the data.

---

## Universities

| Field | Value |
|-------|-------|
| Source | [Hipo/university-domains-list](https://github.com/Hipo/university-domains-list) |
| URL | https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json |
| License | MIT |
| Attribution | Hipo Labs and contributors |
| Update frequency | Periodic re-ingest (manual / scheduled) |
| Fields | name, country, alpha_two_code, state-province, domains, web_pages |
| Restrictions | MIT terms; retain copyright notice |
| Ingestion | `backend/scripts/ingest/universities.py` → `backend/app/data/universities.json` |
| Last documented | 2026-09-03 |

Mock/offline mode serves the **full bundled Hipo list** (~10,000 universities). Use pagination (`page`, `limit`; max `limit=100`) to page through results; check `meta.total` for the full count.

---

## Countries

| Field | Value |
|-------|-------|
| Source | [mledoze/countries](https://github.com/mledoze/countries) (bundled seed) |
| URL | https://github.com/mledoze/countries |
| License | Open Data / project terms — see upstream repository |
| Attribution | mledoze/countries contributors |
| Update frequency | Re-generate `backend/app/data/countries.json` periodically |
| Fields | ISO codes, capital, region, currencies, languages, timezones, lat/lng |
| Restrictions | Prefer bundled seed for redistribution; do not scrape restricted APIs |
| Ingestion | Seed file under `backend/app/data/countries.json` |
| Last documented | 2026-09-03 |

Demo `states` / `cities` arrays are enriched for a few common country codes (US, IN, GB, …) and labeled as sample place lists.

---

## Geography / Geocoding

| Field | Value |
|-------|-------|
| Source | OpenStreetMap Nominatim (live) / DemoProvider (mock) |
| URL | https://nominatim.openstreetmap.org |
| License | [ODbL](https://www.openstreetmap.org/copyright) for OSM data |
| Attribution | © OpenStreetMap contributors |
| Update frequency | Live queries (cached) |
| Restrictions | Respect Nominatim [usage policy](https://operations.osmfoundation.org/policies/nominatim/) — valid User-Agent, rate limits, caching |
| Provider | `OpenStreetMapProvider` / `DemoProvider` |
| Last documented | 2026-09-02 |

Distance calculations use haversine on WGS84 coordinates (no external license).

---

## Weather

| Field | Value |
|-------|-------|
| Source | [Open-Meteo](https://open-meteo.com/) (default live) / MockWeatherProvider |
| URL | https://api.open-meteo.com |
| License | Free for non-commercial; see Open-Meteo terms for commercial |
| Attribution | Weather data by Open-Meteo.com |
| Update frequency | Live (Redis TTL cache) |
| Restrictions | Do not abuse; cache responses; optional API key providers via env only |
| Env | `WEATHER_PROVIDER`, `WEATHER_API_KEY` (optional) |
| Last documented | 2026-09-02 |

---

## Books

| Field | Value |
|-------|-------|
| Source | [Open Library](https://openlibrary.org/developers/api) |
| URL | https://openlibrary.org |
| License | Various work licenses; API usage per Open Library terms; prefer metadata |
| Attribution | Open Library / Internet Archive |
| Update frequency | Live search (cached) |
| Restrictions | Respect rate limits; cover images subject to source rights — link, don't hotlink abusively |
| Provider | `OpenLibraryProvider` / `MockBooksProvider` |
| Last documented | 2026-09-02 |

---

## Currency

| Field | Value |
|-------|-------|
| Source | [Frankfurter](https://www.frankfurter.app/) (ECB rates) |
| URL | https://api.frankfurter.app |
| License | Free; ECB reference rates |
| Attribution | European Central Bank via Frankfurter |
| Update frequency | Daily ECB publication; cached |
| Restrictions | Not for critical financial decisions; educational use |
| Provider | `FrankfurterProvider` / `MockCurrencyProvider` |
| Last documented | 2026-09-02 |

---

## Time / Timezones

| Field | Value |
|-------|-------|
| Source | IANA Time Zone Database via Python `zoneinfo` |
| License | Public domain (IANA TZDB) |
| Attribution | IANA Time Zone Database |
| Update frequency | With Python/OS updates |
| Restrictions | None significant |
| Last documented | 2026-09-02 |

---

## Holidays (planned)

| Field | Value |
|-------|-------|
| Source | TBD — candidates: Nager.Date, OpenHolidays API |
| Status | Not ingested until license verified for redistribution |
| Last documented | 2026-09-02 |

---

## Prohibited Practices

- Scraping behind auth / paywalls
- Ignoring robots.txt or API ToS
- Redistributing copyrighted corpora without rights
- Claiming mock/demo data as live authoritative data
