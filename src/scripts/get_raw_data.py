
import gzip
import sys
from pathlib import Path

import requests
from tqdm import tqdm
import argparse



BASE_URL = "https://dblp.uni-trier.de/xml/"

FILES = {
    "dblp.xml.gz": BASE_URL + "dblp.xml.gz",
    "dblp.dtd": BASE_URL + "dblp.dtd",
}

CHUNK_SIZE = 1024 * 1024  # 1 MiB


def download_file(url: str, destination: Path):
    temp_path = destination.with_suffix(destination.suffix + ".part")

    try:
        with requests.get(
            url, stream=True, timeout=(30, 120)
        ) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))

            with open(temp_path, "wb") as file:
                with tqdm(
                    total=total_size or None,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=f"Downloading {destination.name}",
                ) as progress:
                    for chunk in response.iter_content(
                        chunk_size=CHUNK_SIZE
                    ):
                        if chunk:
                            file.write(chunk)
                            progress.update(len(chunk))

        temp_path.replace(destination)

    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def extract_gzip(source: Path, destination: Path) -> None:
    """Extract a gzip file with a progress bar."""
    total_size = source.stat().st_size

    # Read the compressed stream in chunks to keep memory usage low.
    with gzip.open(source, "rb") as compressed:
        with open(destination, "wb") as extracted:
            with tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc=f"Extracting {destination.name}",
            ) as progress:
                while True:
                    chunk = compressed.read(CHUNK_SIZE)
                    if not chunk:
                        break

                    extracted.write(chunk)
                    progress.update(len(chunk))

def get_raw_data(save_path: Path) -> None:
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

    save_path = Path(args.save_path)

    get_raw_data(save_path)


if __name__ == "__main__":
    main()
