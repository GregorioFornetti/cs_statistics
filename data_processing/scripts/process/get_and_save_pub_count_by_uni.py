
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.scripts.constants import DBLP_STORE_FILE, CONF_COUNT_BY_UNI_FOLDER, JOURNAL_COUNT_BY_UNI_FOLDER



from tqdm import tqdm
import json
import argparse
from pyoxigraph import Store





def get_and_save_pub_count_by_uni(store, conf_count_by_uni_folder: str, journal_count_by_uni_folder: str, metadata: dict = None):
    query = """
    PREFIX dblp: <https://dblp.org/rdf/schema#>
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT DISTINCT ?publication ?stream ?institution ?year ?type
    WHERE {
        ?stream rdf:type ?type .

        FILTER (?type != dblp:Stream)

        ?publication dblp:yearOfPublication ?year ;
                    dblp:publishedInStream ?stream ;
                    dblp:hasSignature ?signature .

        ?signature dblp:signatureInstitution ?institution .
    }
    """

    results = store.query(query)

    conferences_data = {}
    journal_data = {}

    publication_ids = set()

    total = None
    if metadata and 'publications' in metadata:
        total = metadata['publications']

    pbar = tqdm(total=total, desc="Processing publications", unit="publication")

    for row in results:
        institution_id = row['institution'].value.replace("https://dblp.org/inst/", "")
        year = row['year'].value
        if row['type'].value == "https://dblp.org/rdf/schema#Conference":
            conference_id = row['stream'].value.replace('https://dblp.org/streams/conf/', '')
            if conference_id not in conferences_data:
                conferences_data[conference_id] = {}
            if year not in conferences_data[conference_id]:
                conferences_data[conference_id][year] = {}
            conferences_data[conference_id][year][institution_id] = conferences_data[conference_id][year].get(institution_id, 0) + 1
        elif row['type'].value == "https://dblp.org/rdf/schema#Journal":
            journal_id = row['stream'].value.replace('https://dblp.org/streams/journals/', '')
            if journal_id not in journal_data:
                journal_data[journal_id] = {}
            if year not in journal_data[journal_id]:
                journal_data[journal_id][year] = {}
            journal_data[journal_id][year][institution_id] = journal_data[journal_id][year].get(institution_id, 0) + 1

        publication_id = row['publication'].value
        if publication_id not in publication_ids:
            publication_ids.add(publication_id)
            pbar.update(1)

    print(f"Saving conference publication counts by university to {conf_count_by_uni_folder}")
    for conference_id, counts_by_year in conferences_data.items():
        output_file = os.path.join(conf_count_by_uni_folder, f"{conference_id}.json")
        with open(output_file, 'w') as f:
            json.dump(counts_by_year, f, indent=4)

    print(f"Saving journal publication counts by university to {journal_count_by_uni_folder}")
    for journal_id, counts_by_year in journal_data.items():
        output_file = os.path.join(journal_count_by_uni_folder, f"{journal_id}.json")
        with open(output_file, 'w') as f:
            json.dump(counts_by_year, f, indent=4)






if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get and save the publication counts by university from the DBLP store."
    )
    parser.add_argument(
        "--dblp_store_path",
        type=str,
        default=DBLP_STORE_FILE,
        help="Path to the DBLP store file (default: %(default)s)"
    )
    parser.add_argument(
        "--conf_count_by_uni_folder",
        type=str,
        default=CONF_COUNT_BY_UNI_FOLDER,
        help="Folder to save the conference publication counts by university (default: %(default)s)"
    )
    parser.add_argument(
        "--journal_count_by_uni_folder",
        type=str,
        default=JOURNAL_COUNT_BY_UNI_FOLDER,
        help="Folder to save the journal publication counts by university (default: %(default)s)"
    )
    parser.add_argument(
        "--store_file",
        type=str,
        default=DBLP_STORE_FILE,
        help="Path to the DBLP store file (default: %(default)s)"
    )
    args = parser.parse_args()

    store = Store(args.dblp_store_path)

    os.makedirs(args.conf_count_by_uni_folder, exist_ok=True)
    os.makedirs(args.journal_count_by_uni_folder, exist_ok=True)

    get_and_save_pub_count_by_uni(store, args.conf_count_by_uni_folder, args.journal_count_by_uni_folder)