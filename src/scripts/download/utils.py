
import gzip
from pathlib import Path
import requests
from tqdm import tqdm



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