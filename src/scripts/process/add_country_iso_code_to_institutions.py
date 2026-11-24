
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.scripts.constants import INSTITUTIONS_FILE, COUNTRIES_TO_ISO_CODES_FILE

import json
import argparse




def add_country_iso_code_to_institutions(institutions_file: str, countries_to_iso_codes_file: str):
    # Load institutions data
    with open(institutions_file, 'r', encoding='utf-8') as f:
        institutions_data = json.load(f)

    # Load countries to ISO codes data
    with open(countries_to_iso_codes_file, 'r', encoding='utf-8') as f:
        countries_to_iso_codes_data = json.load(f)

    # Add ISO codes to institutions data
    for _, institution in institutions_data.items():
        country_name = institution.get('country')
        if country_name:
            if country_name not in countries_to_iso_codes_data:
                print(f"Country {country_name} not found in ISO codes data")
                print("Run src/scripts/utils/check_countries_dblp_vs_countries_json.py to find missing countries and add them to the countries_to_iso_codes.json file.")
                raise ValueError(f"Country {country_name} not found in ISO codes data")
            
            institution['country_iso_code'] = countries_to_iso_codes_data[country_name]

    # Save updated institutions data back to the file
    with open(institutions_file, 'w', encoding='utf-8') as f:
        json.dump(institutions_data, f, ensure_ascii=False, indent=4)





if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add country ISO codes to institutions data."
    )
    parser.add_argument(
        "--institutions_file",
        type=str,
        default=INSTITUTIONS_FILE,
        help="Path to the institutions JSON file.",
    )
    parser.add_argument(
        "--countries_to_iso_codes_file",
        type=str,
        default=COUNTRIES_TO_ISO_CODES_FILE,
        help="Path to the countries to ISO codes JSON file.",
    )
    args = parser.parse_args()

    add_country_iso_code_to_institutions(args.institutions_file, args.countries_to_iso_codes_file)