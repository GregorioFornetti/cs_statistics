
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


from src.scripts.constants import COUNTRIES_BY_CONTINENT_FILE, COUNTRIES_TO_ISO_CODES_FILE

import json
import urllib.request
from collections import defaultdict
from pathlib import Path
import argparse






SOURCE_URL = (
    "https://raw.githubusercontent.com/"
    "mledoze/countries/master/dist/countries.json"
)



def get_and_save_countries_by_continent(country_to_continent_file_path: Path, countries_to_iso_codes_file_path: Path):
    # Download source JSON
    with urllib.request.urlopen(SOURCE_URL) as response:
        countries = json.load(response)

    # Group countries by continent
    countries_by_continent = defaultdict(list)
    countries_to_iso_codes = {}

    for entry in countries:
        country_common_name = entry["name"]["common"]
        country_official_name = entry["name"]["official"]
        country_iso_code = entry["cca2"]
        country_continent = entry["region"]

        countries_by_continent[country_continent].append(country_iso_code)
        countries_to_iso_codes[country_common_name] = country_iso_code
        countries_to_iso_codes[country_official_name] = country_iso_code

    # Save countries by continent to JSON
    with open(country_to_continent_file_path, "w", encoding="utf-8") as f:
        json.dump(countries_by_continent, f, ensure_ascii=False, indent=4)

    # Save countries to ISO codes to JSON
    with open(countries_to_iso_codes_file_path, "w", encoding="utf-8") as f:
        json.dump(countries_to_iso_codes, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download and format countries by continent."
    )
    parser.add_argument(
        "--output",
        type=str,
        default=COUNTRIES_BY_CONTINENT_FILE,
        help="Output file path for countries by continent JSON.",
    )
    parser.add_argument(
        "--iso_output",
        type=str,
        default=COUNTRIES_TO_ISO_CODES_FILE,
        help="Output file path for countries to ISO codes JSON.",
    )
    args = parser.parse_args()

    get_and_save_countries_by_continent(
        Path(args.output),
        Path(args.iso_output)
    )
