

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.scripts.constants import DBLP_RAW_METADATA_FILE, DBLP_RDF_FILE, DBLP_RDF_GZ_FILE



from src.scripts.download.utils import download_file, extract_gzip
import sys
from pathlib import Path
import argparse


FILENAME = "dblp.ttl.gz"
URL = "https://dblp.org/rdf/dblp.ttl.gz"
URL_METADATA = "https://dblp.org/rdf/STATISTICS.txt"


def download_dblp_rdf_data(compressed_file_path: Path, extracted_file_path: Path) -> None:
    '''
    Download and extract the DBLP RDF dataset.
    '''
    try:
        download_file(URL, compressed_file_path)

        extract_gzip(compressed_file_path, extracted_file_path)

        print("DBLP download and extraction completed!")

    except Exception as error:
        print(f"\nError: {error}", file=sys.stderr)
        sys.exit(1)

def download_dblp_rdf_metadata(metadata_file_path: Path) -> None:
    '''
    Download the DBLP RDF metadata.
    '''
    try:
        download_file(URL_METADATA, metadata_file_path)

        print("DBLP metadata download completed!")

    except Exception as error:
        print(f"\nError: {error}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download and extract the DBLP RDF dataset."
    )
    parser.add_argument(
        "--compressed_file_path",
        type=Path,
        default=DBLP_RDF_GZ_FILE,
        help="Path to the compressed DBLP RDF file.",
    )
    parser.add_argument(
        "--extracted_file_path",
        type=Path,
        default=DBLP_RDF_FILE,
        help="Path to the extracted DBLP RDF file.",
    )
    parser.add_argument(
        "--metadata_file_path",
        type=Path,
        default=DBLP_RAW_METADATA_FILE,
        help="Path to the DBLP RDF metadata file.",
    )
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.compressed_file_path), exist_ok=True)
    os.makedirs(os.path.dirname(args.extracted_file_path), exist_ok=True)
    os.makedirs(os.path.dirname(args.metadata_file_path), exist_ok=True)

    download_dblp_rdf_data(Path(args.compressed_file_path), Path(args.extracted_file_path))
    download_dblp_rdf_metadata(args.metadata_file_path)


if __name__ == "__main__":
    main()
