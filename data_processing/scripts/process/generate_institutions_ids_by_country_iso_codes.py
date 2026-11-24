
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.scripts.constants import INSTITUTIONS_FILE, INSTITUTIONS_BY_COUNTRY_ISO_CODES_FILE



import json
import argparse
from collections import defaultdict









def generate_institutions_ids_by_country_iso_codes(institutions_file: str, output_file: str):
    # Load institutions data
    with open(institutions_file, 'r', encoding='utf-8') as f:
        institutions_data = json.load(f)

    # Create a dictionary to hold institutions grouped by country ISO codes
    institutions_by_country_iso_codes = defaultdict(list)

    for institution_id, institution in institutions_data.items():
        country_iso_code = institution.get('country_iso_code')
        if country_iso_code:
            institutions_by_country_iso_codes[country_iso_code].append(institution_id)

    # Save the grouped data to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(institutions_by_country_iso_codes, f, ensure_ascii=False, indent=4)








if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a JSON file mapping country ISO codes to lists of institution IDs."
    )
    parser.add_argument(
        "--institutions_file",
        type=str,
        default=INSTITUTIONS_FILE,
        help="Path to the institutions JSON file.",
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default=INSTITUTIONS_BY_COUNTRY_ISO_CODES_FILE,
        help="Path to the output JSON file.",
    )
    args = parser.parse_args()

    generate_institutions_ids_by_country_iso_codes(args.institutions_file, args.output_file)