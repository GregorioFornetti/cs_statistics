
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


from src.scripts.constants import COUNTRIES_BY_CONTINENT_FILE

import json
import urllib.request
from collections import defaultdict
from pathlib import Path
import argparse






SOURCE_URL = (
    "https://raw.githubusercontent.com/"
    "samayo/country-json/master/src/country-by-continent.json"
)


def get_and_save_countries_by_continent(output_file: Path):
    # Download source JSON
    with urllib.request.urlopen(SOURCE_URL) as response:
        countries = json.load(response)

    # Group countries by continent
    continents = defaultdict(list)

    for entry in countries:
        country = entry["country"]
        continent = entry["continent"]

        continents[continent].append(country)

    # Sort countries alphabetically
    result = {
        continent: sorted(country_list)
        for continent, country_list in sorted(continents.items())
    }

    # Save formatted JSON
    with output_file.open("w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    print(f"Successfully generated {output_file}")
    print(f"Total countries: {sum(map(len, result.values()))}")
    print(f"Total continents: {len(result)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download and format countries by continent."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=COUNTRIES_BY_CONTINENT_FILE,
        help="Output file path (default: %(default)s)",
    )
    args = parser.parse_args()

    get_and_save_countries_by_continent(args.output)
