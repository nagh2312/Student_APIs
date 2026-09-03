# API Roadmap

Prioritization framework for the Student API Platform.

## Scoring Model

| Criterion | Weight |
|-----------|--------|
| Student demand | 30% |
| Breadth of use | 20% |
| Existing API gap | 15% |
| Open data availability | 15% |
| Technical feasibility | 10% |
| Maintenance cost (inverse) | 10% |

Score range: 1–10 per criterion. Weighted total out of 10.

---

## Candidate APIs (30+)

| # | API | Demand | Breadth | Gap | Open Data | Feasibility | Maint. | **Score** | Priority |
|---|-----|--------|---------|-----|-----------|-------------|--------|-----------|----------|
| 1 | Universities | 10 | 9 | 8 | 9 | 9 | 8 | **9.05** | P0 |
| 2 | Countries / Geography metadata | 9 | 10 | 6 | 10 | 10 | 9 | **8.85** | P0 |
| 3 | Weather | 10 | 10 | 5 | 8 | 8 | 7 | **8.35** | P0 |
| 4 | Books | 9 | 8 | 7 | 8 | 8 | 8 | **8.20** | P0 |
| 5 | Currency / FX | 9 | 9 | 6 | 8 | 9 | 7 | **8.15** | P0 |
| 6 | Time / Timezones | 8 | 9 | 5 | 10 | 10 | 10 | **8.25** | P0 |
| 7 | Geocoding / Distance | 9 | 9 | 6 | 8 | 7 | 6 | **7.85** | P0 |
| 8 | Holidays | 8 | 8 | 7 | 8 | 9 | 8 | **7.95** | P1 |
| 9 | Movies | 8 | 7 | 5 | 6 | 7 | 6 | **6.70** | P1 |
| 10 | Nutrition / Foods | 7 | 7 | 7 | 7 | 7 | 6 | **6.90** | P1 |
| 11 | News (headlines) | 8 | 8 | 4 | 4 | 6 | 4 | **6.10** | P2 |
| 12 | Airports / Airlines | 7 | 7 | 6 | 8 | 8 | 7 | **7.10** | P1 |
| 13 | Datasets (ML) | 9 | 8 | 8 | 9 | 7 | 6 | **8.05** | P1 |
| 14 | Campus (demo) | 8 | 6 | 9 | 7 | 8 | 7 | **7.50** | P1 |
| 15 | Academic Calendar | 7 | 6 | 8 | 5 | 7 | 6 | **6.55** | P2 |
| 16 | Courses / Subjects | 7 | 6 | 7 | 5 | 6 | 5 | **6.15** | P2 |
| 17 | Developer Tech Stack | 7 | 7 | 6 | 8 | 8 | 8 | **7.20** | P1 |
| 18 | Text utilities (AI/ML) | 9 | 8 | 5 | 7 | 6 | 5 | **7.05** | P2 |
| 19 | Quotes / Inspiration | 6 | 6 | 4 | 8 | 9 | 9 | **6.55** | P2 |
| 20 | Random / Utilities | 6 | 7 | 3 | 10 | 10 | 10 | **7.00** | P2 |
| 21 | Public Transit | 7 | 6 | 7 | 5 | 5 | 4 | **5.85** | P3 |
| 22 | Jobs / Internships | 9 | 7 | 6 | 3 | 5 | 3 | **5.95** | P3 |
| 23 | Scholarships | 8 | 6 | 8 | 4 | 5 | 4 | **6.20** | P2 |
| 24 | Recipes | 6 | 6 | 5 | 6 | 7 | 7 | **6.10** | P3 |
| 25 | Sports scores | 6 | 6 | 3 | 4 | 5 | 4 | **4.85** | P3 |
| 26 | Climate / Sustainability | 7 | 6 | 6 | 8 | 6 | 5 | **6.45** | P2 |
| 27 | Government / Census | 7 | 7 | 5 | 9 | 6 | 5 | **6.60** | P2 |
| 28 | Research papers | 8 | 6 | 5 | 5 | 5 | 4 | **5.80** | P3 |
| 29 | Language detect / NLP utils | 7 | 7 | 5 | 8 | 7 | 6 | **6.70** | P2 |
| 30 | Events (public) | 7 | 7 | 5 | 5 | 6 | 5 | **6.00** | P3 |
| 31 | QR / barcode utils | 5 | 6 | 4 | 10 | 9 | 9 | **6.45** | P3 |
| 32 | Color / design utils | 5 | 5 | 4 | 10 | 9 | 9 | **6.15** | P3 |
| 33 | ISBN / DOI lookup | 6 | 5 | 6 | 8 | 8 | 8 | **6.55** | P2 |
| 34 | IP geolocation | 7 | 7 | 4 | 6 | 7 | 6 | **6.20** | P2 |
| 35 | Fake/sample user data | 8 | 8 | 3 | 10 | 9 | 9 | **7.55** | P1 |

---

## Phase 0 — Initial Portfolio (this release)

Based on scores and the product vision, the first release implements:

1. **Universities API** (9.05) — education projects, campus apps
2. **Countries API** (8.85) — nearly universal need
3. **Geography API** (7.85) — geocode, reverse, distance
4. **Weather API** (8.35) — dashboards, travel, IoT demos
5. **Books API** (8.20) — library, reading, catalog apps
6. **Currency API** (8.15) — finance, travel converters
7. **Time API** (8.25) — scheduling, world clocks (low maintenance)

## Phase 1 — Next

- Holidays
- Datasets (ML)
- Campus (demo data)
- Airports
- Developer technologies
- Sample/fake user data

## Phase 2 — Later

- Movies, Nutrition, Text utilities, Scholarships, Government data

## Phase 3 — Explore Carefully

- News, Jobs, Transit (licensing, maintenance, ToS risk)

---

## Decision Notes

- **Universities** wins on demand + open Hipolabs/OpenData availability.
- **Time** scores high on feasibility/maintenance despite slightly lower "gap."
- **News/Jobs** deferred: licensing and ToS constraints.
- **AI endpoints** deferred until provider abstraction and cost model are clear.
