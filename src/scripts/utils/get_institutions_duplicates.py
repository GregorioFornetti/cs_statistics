import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.scripts.constants import DBLP_STORE_FILE, CORRECTED_INSTITUTION_DUPLICATES_FILE, DUPLICATE_INSTITUTIONS_FILE, DUPLICATE_INSTITUTIONS_NOT_CORRECTED_FILE, METADATA_FILE


import json
from tqdm import tqdm
from pyoxigraph import Store
import argparse


parser = argparse.ArgumentParser(
    description="Get the institutions with duplicates."
)
parser.add_argument(
    "--dblp_store_path",
    type=str,
    default=DBLP_STORE_FILE,
    help="Path to the DBLP store.",
)
parser.add_argument(
    "--corrected_institution_duplicates_path",
    type=str,
    default=CORRECTED_INSTITUTION_DUPLICATES_FILE,
    help="Path to the corrected institution duplicates JSON file.",
)
parser.add_argument(
    "--duplicate_institutions_path",
    type=str,
    default=DUPLICATE_INSTITUTIONS_FILE,
    help="Path to the duplicate institutions JSON file.",
)
parser.add_argument(
    "--duplicate_institutions_not_corrected_path",
    type=str,
    default=DUPLICATE_INSTITUTIONS_NOT_CORRECTED_FILE,
    help="Path to the duplicate institutions not corrected JSON file.",
)
parser.add_argument(
    '--metadata_path',
    type=str,
    default=METADATA_FILE,
    help='Path to the metadata JSON file.',
)
args = parser.parse_args()

store_path = args.dblp_store_path
corrected_institution_duplicates_path = args.corrected_institution_duplicates_path
duplicate_institutions_path = args.duplicate_institutions_path
duplicate_institutions_not_corrected_path = args.duplicate_institutions_not_corrected_path

# Persistent database stored on disk
store = Store("data/raw/dblp_store")

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

with open(corrected_institution_duplicates_path, 'r') as f:
    corrected_institution_duplicates = json.load(f)

with open(args.metadata_path, 'r') as f:
    metadata = json.load(f)

institutions_total = metadata['institutions']

institutions_data = {}
results = store.query(query)

pbar = tqdm(results, total=institutions_total, desc="Processing institutions")

for row in results:

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
        institutions_data[institution_id] = [data]
        pbar.update(1)
    else:
        if len(data) > len(institutions_data[institution_id][0]):
            institutions_data[institution_id][0] = data
        elif len(data) == len(institutions_data[institution_id][0]) and data != institutions_data[institution_id][0]:
            institutions_data[institution_id].append(data)

pbar.close()

duplicate_institutions = {k: v for k, v in institutions_data.items() if len(v) > 1}

duplicate_institutions_not_corrected = {k: v for k, v in duplicate_institutions.items() if k not in corrected_institution_duplicates}

print(f"Number of institutions with duplicates: {len(duplicate_institutions)}")
print(f"Number of institutions with duplicates not corrected: {len(duplicate_institutions_not_corrected)}")

print('Saving data...')

os.makedirs('data/temp', exist_ok=True)

with open(duplicate_institutions_path, 'w') as f:
    json.dump(duplicate_institutions, f, indent=4, ensure_ascii=False)

with open(duplicate_institutions_not_corrected_path, 'w') as f:
    json.dump(duplicate_institutions_not_corrected, f, indent=4, ensure_ascii=False)