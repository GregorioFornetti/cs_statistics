

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.scripts.constants import ROOT_DIR



from utils import download_file, extract_gzip
import sys
from pathlib import Path
import argparse


FILENAME = "dblp.ttl.gz"
URL = "https://dblp.org/rdf/dblp.ttl.gz"




def download_dblp_rdf_data(save_path: Path) -> None:
    '''
    Download and extract the DBLP RDF dataset.
    '''
    save_path.mkdir(parents=True, exist_ok=True)

    try:
        download_file(URL, save_path / "dblp.ttl.gz")

        # Extract the RDF dump.
        archive = save_path / "dblp.ttl.gz"
        ttl_file = save_path / "dblp.ttl"

        extract_gzip(archive, ttl_file)

        print("\nDBLP download and extraction completed!")

    except Exception as error:
        print(f"\nError: {error}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download and extract the DBLP RDF dataset."
    )
    parser.add_argument(
        "--save-path",
        type=Path,
        default='data/raw',
        help="Directory to save the downloaded files.",
    )
    args = parser.parse_args()

    save_path = Path(ROOT_DIR) / Path(args.save_path)

    download_dblp_rdf_data(save_path)


if __name__ == "__main__":
    main()
