
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


import argparse
from pathlib import Path
import shutil

from pyoxigraph import Store, RdfFormat

from src.scripts.constants import COUNTRIES_TO_ISO_CODES_FILE, DBLP_RDF_GZ_FILE, DBLP_RDF_FILE, DBLP_STORE_FILE, CONFERENCES_FILE, INSTITUTIONS_BY_COUNTRY_ISO_CODES_FILE, JOURNALS_FILE, INSTITUTIONS_FILE, CORRECTED_INSTITUTION_DUPLICATES_FILE, METADATA_FILE, DBLP_RAW_METADATA_FILE, CONF_COUNT_BY_UNI_FOLDER, JOURNAL_COUNT_BY_UNI_FOLDER

from src.scripts.download.dblp_rdf import download_dblp_rdf_data, download_dblp_rdf_metadata

from src.scripts.pre_process.generate_dblp_store import generate_dblp_store

from src.scripts.process.process_dblp_metadata import process_dblp_metadata

from src.scripts.process.get_and_save_venues_data import get_and_save_venues_data

from src.scripts.process.get_and_save_institutions_data import get_and_save_institutions_data
from src.scripts.process.add_country_iso_code_to_institutions import add_country_iso_code_to_institutions
from src.scripts.process.generate_institutions_ids_by_country_iso_codes import generate_institutions_ids_by_country_iso_codes

from src.scripts.process.get_and_save_pub_count_by_uni import get_and_save_pub_count_by_uni




argparser = argparse.ArgumentParser(description='Process DBLP data and save venues and institutions data.')
argparser.add_argument('--rdf_gz_file', type=str, default=DBLP_RDF_GZ_FILE, help='Path to the DBLP RDF GZ file.')
argparser.add_argument('--rdf_file', type=str, default=DBLP_RDF_FILE, help='Path to the DBLP RDF file.')
argparser.add_argument('--store_file', type=str, default=DBLP_STORE_FILE, help='Path to the DBLP store file.')
argparser.add_argument('--conferences_file', type=str, default=CONFERENCES_FILE, help='Path to the conferences JSON file.')
argparser.add_argument('--journals_file', type=str, default=JOURNALS_FILE, help='Path to the journals JSON file.')
argparser.add_argument('--institutions_file', type=str, default=INSTITUTIONS_FILE, help='Path to the institutions JSON file.')
argparser.add_argument('--corrected_institution_duplicates_file', type=str, default=CORRECTED_INSTITUTION_DUPLICATES_FILE, help='Path to the corrected institution duplicates JSON file.')
argparser.add_argument('--metadata_file', type=str, default=METADATA_FILE, help='Path to the metadata JSON file.')
argparser.add_argument('--raw_metadata_file', type=str, default=DBLP_RAW_METADATA_FILE, help='Path to the raw metadata file.')
argparser.add_argument('--institutions_ids_by_country_iso_codes_file', type=str, default=INSTITUTIONS_BY_COUNTRY_ISO_CODES_FILE, help='Path to the institutions IDs by country ISO codes JSON file.')
argparser.add_argument('--countries_to_iso_codes_file', type=str, default=COUNTRIES_TO_ISO_CODES_FILE, help='Path to the countries to ISO codes JSON file.')
argparser.add_argument('--conf_count_by_uni_folder', type=str, default=CONF_COUNT_BY_UNI_FOLDER, help='Folder to save the conference publication counts by university.')
argparser.add_argument('--journal_count_by_uni_folder', type=str, default=JOURNAL_COUNT_BY_UNI_FOLDER, help='Folder to save the journal publication counts by university.')
argparser.add_argument('--skip_download', action='store_true', help='Skip downloading the DBLP RDF data.')
argparser.add_argument('--skip_process_metadata', action='store_true', help='Skip processing the DBLP RDF metadata.')
argparser.add_argument('--skip_generate_store', action='store_true', help='Skip generating the DBLP store.')
argparser.add_argument('--skip_process_venues', action='store_true', help='Skip processing and saving venues data.')
argparser.add_argument('--skip_process_institutions', action='store_true', help='Skip processing and saving institutions data.')
argparser.add_argument('--skip_process_publication_counts', action='store_true', help='Skip processing and saving publication counts by university.')
argparser.add_argument('--load_all_on_memory', action='store_true', help='Load all data into memory for faster processing (may require more RAM).')
args = argparser.parse_args()

os.makedirs(os.path.dirname(args.rdf_gz_file), exist_ok=True)
os.makedirs(os.path.dirname(args.rdf_file), exist_ok=True)
os.makedirs(os.path.dirname(args.store_file), exist_ok=True)
os.makedirs(os.path.dirname(args.conferences_file), exist_ok=True)
os.makedirs(os.path.dirname(args.journals_file), exist_ok=True)
os.makedirs(os.path.dirname(args.institutions_file), exist_ok=True)
os.makedirs(os.path.dirname(args.corrected_institution_duplicates_file), exist_ok=True)
os.makedirs(os.path.dirname(args.metadata_file), exist_ok=True)
os.makedirs(os.path.dirname(args.raw_metadata_file), exist_ok=True)
os.makedirs(os.path.dirname(args.institutions_ids_by_country_iso_codes_file), exist_ok=True)
os.makedirs(os.path.dirname(args.countries_to_iso_codes_file), exist_ok=True)
os.makedirs(args.conf_count_by_uni_folder, exist_ok=True)
os.makedirs(args.journal_count_by_uni_folder, exist_ok=True)

if not args.skip_download:
    download_dblp_rdf_data(Path(args.rdf_gz_file), Path(args.rdf_file))
    download_dblp_rdf_metadata(Path(args.raw_metadata_file))

metadata = None
if not args.skip_process_metadata:
    metadata = process_dblp_metadata(Path(args.raw_metadata_file), Path(args.metadata_file))

if not args.skip_generate_store:
    if os.path.exists(args.store_file):
        shutil.rmtree(args.store_file)
    generate_dblp_store(args.rdf_file, args.store_file)

if args.load_all_on_memory:
    store = Store()
    print(f"Loading DBLP RDF data from {args.rdf_file} into memory...")
    store.load(path=args.rdf_file, format=RdfFormat.TURTLE)
else:
    store = Store(args.store_file)

if not args.skip_process_venues:
    get_and_save_venues_data(store, args.conferences_file, args.journals_file, metadata=metadata)

if not args.skip_process_institutions:
    get_and_save_institutions_data(store, args.institutions_file, args.corrected_institution_duplicates_file, metadata=metadata)
    add_country_iso_code_to_institutions(args.institutions_file, args.countries_to_iso_codes_file)
    generate_institutions_ids_by_country_iso_codes(args.institutions_file, args.institutions_ids_by_country_iso_codes_file)

if not args.skip_process_publication_counts:
    get_and_save_pub_count_by_uni(store, args.conf_count_by_uni_folder, args.journal_count_by_uni_folder, metadata=metadata)