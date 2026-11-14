
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


import argparse
from pathlib import Path
import shutil

from pyoxigraph import Store

from src.scripts.constants import DBLP_RDF_GZ_FILE, DBLP_RDF_FILE, DBLP_STORE_FILE, CONFERENCES_FILE, JOURNALS_FILE, INSTITUTIONS_FILE, CORRECTED_INSTITUTION_DUPLICATES_FILE, METADATA_FILE, DBLP_RAW_METADATA_FILE

from src.scripts.download.dblp_rdf import download_dblp_rdf_data

from src.scripts.pre_process.generate_dblp_store import generate_dblp_store

from src.scripts.process.process_dblp_metadata import process_dblp_metadata
from src.scripts.process.get_and_save_venues_data import get_and_save_venues_data
from src.scripts.process.get_and_save_institutions_data import get_and_save_institutions_data




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
argparser.add_argument('--skip_download', action='store_true', help='Skip downloading the DBLP RDF data.')
argparser.add_argument('--skip_process_metadata', action='store_true', help='Skip processing the DBLP RDF metadata.')
argparser.add_argument('--skip_generate_store', action='store_true', help='Skip generating the DBLP store.')
argparser.add_argument('--skip_process_venues', action='store_true', help='Skip processing and saving venues data.')
argparser.add_argument('--skip_process_institutions', action='store_true', help='Skip processing and saving institutions data.')
args = argparser.parse_args()


if not args.skip_download:
    download_dblp_rdf_data(Path(args.rdf_gz_file), Path(args.rdf_file))

if not args.skip_process_metadata:
    process_dblp_metadata(Path(args.raw_metadata_file), Path(args.metadata_file))

if not args.skip_generate_store:
    if os.path.exists(args.store_file):
        shutil.rmtree(args.store_file)
    generate_dblp_store(args.rdf_file, args.store_file)

store = Store(args.store_file)

if not args.skip_process_venues:
    get_and_save_venues_data(store, args.conferences_file, args.journals_file)

if not args.skip_process_institutions:
    get_and_save_institutions_data(store, args.institutions_file, args.corrected_institution_duplicates_file)