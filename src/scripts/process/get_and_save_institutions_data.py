

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.scripts.constants import DBLP_STORE_FILE, INSTITUTIONS_FILE, CORRECTED_INSTITUTION_DUPLICATES_FILE



from tqdm import tqdm
import json
import argparse
from pyoxigraph import Store





def get_and_save_institutions_data(store, institutions_file_path: str, corrected_institution_duplicates: str):
    query = """
    PREFIX dblp: <https://dblp.org/rdf/schema#>
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT DISTINCT ?institution ?name ?country ?state ?city
    WHERE {
        ?institution rdf:type dblp:Institution .

        OPTIONAL {
        ?institution dblp:institutionName ?institutionName .
        }
        OPTIONAL {
            ?institution dblp:primaryInstitutionName ?primaryName .
        }
        BIND(COALESCE(?primaryName, ?institutionName) AS ?name)

        OPTIONAL {
            ?institution dblp:hasLocation ?location .

            OPTIONAL {
                ?location dblp:countryName ?country .
            }

            OPTIONAL {
                ?location dblp:stateName ?state .
            }

            OPTIONAL {
                ?location dblp:cityName ?city .
            }
        }
    }
    """
    institutions_data = corrected_institution_duplicates.copy()
    results = store.query(query)

    for row in tqdm(results):

        institution_id = row['institution'].value.replace("https://dblp.org/inst/", "")
        data = {
            "name": row['name'].value
        }

        if row['country']:
            data["country"] = row['country'].value
        if row['state']:
            data["state"] = row['state'].value
        if row['city']:
            data["city"] = row['city'].value

        if not institution_id in institutions_data:
            institutions_data[institution_id] = data
        else:
            if len(data) > len(institutions_data[institution_id]):
                institutions_data[institution_id] = data

            if len(data) == len(institutions_data[institution_id]) and institution_id not in corrected_institution_duplicates:
                raise ValueError(f"Duplicate institution found: {institution_id} with data: {data} and {institutions_data[institution_id]}. Run src/scripts/utils/get_institutions_duplicates.py to get the list of duplicates and correct them.")

    with open(institutions_file_path, 'w') as f:
        json.dump(institutions_data, f, indent=4, ensure_ascii=False)






if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get and save the institutions data from the DBLP store."
    )
    parser.add_argument(
        "--dblp_store_path",
        type=str,
        default=DBLP_STORE_FILE,
        help="Path to the DBLP store.",
    )
    parser.add_argument(
        "--institutions_file_path",
        type=str,
        default=INSTITUTIONS_FILE,
        help="Path to the institutions JSON file.",
    )
    parser.add_argument(
        "--corrected_institution_duplicates_path",
        type=str,
        default=CORRECTED_INSTITUTION_DUPLICATES_FILE,
        help="Path to the corrected institution duplicates JSON file.",
    )
    args = parser.parse_args()

    store = Store(args.dblp_store_path)

    with open(args.corrected_institution_duplicates_path, 'r') as f:
        corrected_institution_duplicates = json.load(f)

    get_and_save_institutions_data(store, args.institutions_file_path, corrected_institution_duplicates)