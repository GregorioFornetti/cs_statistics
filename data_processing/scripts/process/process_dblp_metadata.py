
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.scripts.constants import DBLP_RAW_METADATA_FILE, METADATA_FILE


import sys
from pathlib import Path
import argparse
import json
from datetime import datetime



def process_dblp_metadata(metadata_raw_file_path: Path, metadata_processed_file_path: Path) -> None:
    '''
    Process the DBLP RDF metadata.
    '''
    try:
        with open(metadata_raw_file_path, 'r') as raw_file:
            lines = raw_file.readlines()

        processed_json = {}
        for line in lines:
            if line.startswith("# DBLP RDF STATISTICS"):
                continue  # Skip header line

            line_w_no_spaces = line.replace(" ", "")
            if len(line_w_no_spaces.split(':')) != 2:
                continue  # Skip lines that don't have exactly one colon
            key, value = line_w_no_spaces.split(":", 1)
            processed_json[key] = int(value.strip())

        processed_json['raw_data_origin'] = "https://dblp.org/rdf/"
        # Get the last modified time of the raw metadata and put in a human-readable format
        processed_json['download_date'] = os.path.getmtime(metadata_raw_file_path)
        processed_json['download_date'] = datetime.fromtimestamp(
            os.path.getmtime(metadata_raw_file_path)
        ).strftime('%Y-%m-%d %H:%M:%S')

        with open(metadata_processed_file_path, 'w') as processed_file:
            json.dump(processed_json, processed_file, indent=4)

        print("DBLP metadata processing completed!")

        return processed_json

    except Exception as error:
        print(f"\nError: {error}", file=sys.stderr)
        sys.exit(1)





if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process the DBLP RDF metadata."
    )
    parser.add_argument(
        "--metadata_raw_file_path",
        type=Path,
        default=DBLP_RAW_METADATA_FILE,
        help="Path to the raw DBLP RDF metadata file.",
    )
    parser.add_argument(
        "--metadata_processed_file_path",
        type=Path,
        default=METADATA_FILE,
        help="Path to save the processed DBLP RDF metadata JSON file.",
    )
    args = parser.parse_args()

    process_dblp_metadata(args.metadata_raw_file_path, args.metadata_processed_file_path)