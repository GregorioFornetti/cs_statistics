
import json
from tqdm import tqdm
from pyoxigraph import Store
from tqdm import tqdm
import os

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

with open('data/utils/corrected_institution_duplicates.json', 'r') as f:
    corrected_institution_duplicates = json.load(f)

institutions_data = {}
results = store.query(query)

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
    else:
        if len(data) > len(institutions_data[institution_id][0]):
            institutions_data[institution_id][0] = data
        elif len(data) == len(institutions_data[institution_id][0]) and data != institutions_data[institution_id][0]:
            institutions_data[institution_id].append(data)

duplicate_institutions = {k: v for k, v in institutions_data.items() if len(v) > 1}

duplicate_institutions_not_corrected = {k: v for k, v in duplicate_institutions.items() if k not in corrected_institution_duplicates}

print(f"Number of institutions with duplicates: {len(duplicate_institutions)}")
print(f"Number of institutions with duplicates not corrected: {len(duplicate_institutions_not_corrected)}")

print('Saving data...')

os.makedirs('data/temp', exist_ok=True)

with open('data/temp/duplicate_institutions.json', 'w') as f:
    json.dump(duplicate_institutions, f, indent=4, ensure_ascii=False)

with open('data/temp/duplicate_institutions_not_corrected.json', 'w') as f:
    json.dump(duplicate_institutions_not_corrected, f, indent=4, ensure_ascii=False)