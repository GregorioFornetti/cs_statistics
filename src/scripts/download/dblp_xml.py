

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.scripts.constants import ROOT_DIR



import sys
from pathlib import Path
import argparse
from utils import download_file, extract_gzip



BASE_URL = "https://dblp.uni-trier.de/xml/"

FILES = {
    "dblp.xml.gz": BASE_URL + "dblp.xml.gz",
    "dblp.dtd": BASE_URL + "dblp.dtd",
}




def download_dblp_xml_data(save_path: Path) -> None:
    '''
    Download and extract the DBLP XML dataset.
    '''
    save_path.mkdir(parents=True, exist_ok=True)

    try:
        for filename, url in FILES.items():
            destination = save_path / filename

            download_file(url, destination)

        # Extract the XML dump.
        archive = save_path / "dblp.xml.gz"
        xml_file = save_path / "dblp.xml"

        extract_gzip(archive, xml_file)

        print("\nDBLP download and extraction completed!")

    except Exception as error:
        print(f"\nError: {error}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download and extract the DBLP XML dataset."
    )
    parser.add_argument(
        "--save-path",
        type=Path,
        default='data/raw',
        help="Directory to save the downloaded files.",
    )
    args = parser.parse_args()

    save_path = Path(ROOT_DIR) / Path(args.save_path)

    download_dblp_xml_data(save_path)


if __name__ == "__main__":
    main()
