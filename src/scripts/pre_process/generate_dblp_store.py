import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.scripts.constants import DBLP_RDF_FILE, DBLP_STORE_FILE

import argparse
from pyoxigraph import Store, RdfFormat




def generate_dblp_store(dblp_rdf_file_path: str, dblp_store_path: str) -> None:
    """
    Generate the DBLP store from the RDF file.
    """
    print(f"Generating DBLP store...")
    os.makedirs(os.path.dirname(dblp_store_path), exist_ok=True)
    store = Store(dblp_store_path)
    store.bulk_load(
        path=dblp_rdf_file_path,
        format=RdfFormat.TURTLE,
    )
    print(f"DBLP store generated.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate the DBLP store from the RDF file."
    )
    parser.add_argument(
        "--dblp_rdf_file_path",
        type=str,
        default=DBLP_RDF_FILE,
        help="Path to the DBLP RDF file.",
    )
    parser.add_argument(
        "--dblp_store_path",
        type=str,
        default=DBLP_STORE_FILE,
        help="Path to the DBLP store.",
    )
    args = parser.parse_args()

    generate_dblp_store(args.dblp_rdf_file_path, args.dblp_store_path)
