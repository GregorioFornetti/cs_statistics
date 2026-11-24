

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.scripts.constants import DBLP_STORE_FILE, CONFERENCES_FILE, JOURNALS_FILE



from tqdm import tqdm
import json
import argparse
from pyoxigraph import Store



def get_and_save_venues_data(store, conferences_file_path: str, journals_file_path: str, metadata: dict = None):
    query = """
    PREFIX dblp: <https://dblp.org/rdf/schema#>
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?venue ?type ?name
    WHERE {
        ?type rdfs:subClassOf+ dblp:Stream .

        ?venue rdf:type ?type .

        OPTIONAL {
            ?venue dblp:primaryStreamTitle ?name
        }
    }
    """

    results = store.query(query)

    conferences_data = {}
    journal_data = {}

    total = None
    if metadata and 'streams' in metadata:
        print(f"Total number of streams from metadata: {metadata['streams']}. It may not match the actual number of streams in the DBLP store.")
        total = metadata['streams']

    for row in tqdm(results, total=total, desc="Processing venues"):
        data = {
            "name": row['name'].value
        }

        if row['type'].value == "https://dblp.org/rdf/schema#Conference":
            conference_id = row['venue'].value.replace('https://dblp.org/streams/conf/', '')
            assert conference_id not in conferences_data, f"Duplicate conference venue found: {row['venue'].value}"
            conferences_data[conference_id] = data
        
        elif row['type'].value == "https://dblp.org/rdf/schema#Journal":
            journal_id = row['venue'].value.replace('https://dblp.org/streams/journals/', '')
            assert journal_id not in journal_data, f"Duplicate journal venue found: {row['venue'].value}"
            journal_data[journal_id] = data

    with open(conferences_file_path, 'w') as f:
        json.dump(conferences_data, f, indent=4, ensure_ascii=False)

    with open(journals_file_path, 'w') as f:
        json.dump(journal_data, f, indent=4, ensure_ascii=False)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get and save the venues data (conferences and journals) from the DBLP store."
    )
    parser.add_argument(
        "--dblp_store_path",
        type=str,
        default=DBLP_STORE_FILE,
        help="Path to the DBLP store.",
    )
    parser.add_argument(
        "--conferences_file_path",
        type=str,
        default=CONFERENCES_FILE,
        help="Path to the conferences JSON file.",
    )
    parser.add_argument(
        "--journals_file_path",
        type=str,
        default=JOURNALS_FILE,
        help="Path to the journals JSON file.",
    )
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.conferences_file_path), exist_ok=True)
    os.makedirs(os.path.dirname(args.journals_file_path), exist_ok=True)

    # Persistent database stored on disk
    store = Store(args.dblp_store_path)

    get_and_save_venues_data(store, args.conferences_file_path, args.journals_file_path)