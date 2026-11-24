
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


from src.scripts.constants import COUNTRIES_BY_CONTINENT_FILE, INSTITUTIONS_FILE
import json
import argparse





def check_countries_dblp_vs_countries_json(institutions_file: str, countries_by_continent_file: str):
    # Load institutions data
    with open(institutions_file, 'r', encoding='utf-8') as f:
        institutions_data = json.load(f)

    # Load countries by continent data
    with open(countries_by_continent_file, 'r', encoding='utf-8') as f:
        countries_by_continent_data = json.load(f)

    # Create a set of all countries from the countries_by_continent_data
    all_countries_set = set()
    for continent, countries in countries_by_continent_data.items():
        all_countries_set.update(countries)

    not_found_countries = set()
    for _, institution in institutions_data.items():
        country = institution.get('country')
        if country and country not in all_countries_set:
            not_found_countries.add(country)

    print(f"Countiries not found from DBLP RDF institutions countries at the countries_by_continent JSON: {len(not_found_countries)}. List of countries not found:")
    for country in sorted(not_found_countries):
        print(country)





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check countries in institutions.json against countries_by_continent.json")
    parser.add_argument("--institutions_file", type=str, default=INSTITUTIONS_FILE, help="Path to institutions.json")
    parser.add_argument("--countries_by_continent_file", type=str, default=COUNTRIES_BY_CONTINENT_FILE, help="Path to countries_by_continent.json")
    args = parser.parse_args()

    check_countries_dblp_vs_countries_json(args.institutions_file, args.countries_by_continent_file)
