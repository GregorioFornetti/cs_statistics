

from tqdm import tqdm
import json


def get_and_save_venues_data(store):
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

    for row in tqdm(results):
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

    with open('data/processed/conferences.json', 'w') as f:
        json.dump(conferences_data, f, indent=4, ensure_ascii=False)

    with open('data/processed/journals.json', 'w') as f:
        json.dump(journal_data, f, indent=4, ensure_ascii=False)



if __name__ == "__main__":
    from cs_statistics.src.scripts.utils import get_store
    store = get_store()
    get_and_save_venues_data(store)