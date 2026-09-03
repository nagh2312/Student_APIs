"""Seed helper entrypoint."""

from app.modules.countries.schemas import MOCK_COUNTRIES
from app.modules.universities.mock_data import MOCK_UNIVERSITIES


def main() -> None:
    print(f"Mock universities available: {len(MOCK_UNIVERSITIES)}")
    print(f"Mock countries available: {len(MOCK_COUNTRIES)}")
    print("With MOCK_MODE=true, data is served in-memory (no DB seed required).")
    print("For live DB seeding, set MOCK_MODE=false and run ingest scripts.")


if __name__ == "__main__":
    main()
