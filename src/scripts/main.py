
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


import argparse
from pathlib import Path
import shutil

from pyoxigraph import Store

from src.scripts.constants import DBLP_RDF_GZ_FILE, DBLP_RDF_FILE, DBLP_STORE_FILE, CONFERENCES_FILE, JOURNALS_FILE, INSTITUTIONS_FILE, CORRECTED_INSTITUTION_DUPLICATES_FILE

from src.scripts.download.dblp_rdf import download_dblp_rdf_data

from src.scripts.pre_process.generate_dblp_store import generate_dblp_store

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
args = argparser.parse_args()




#download_dblp_rdf_data(Path(args.rdf_gz_file), Path(args.rdf_file))

#if os.path.exists(args.store_file):
#    shutil.rmtree(args.store_file)

#generate_dblp_store(args.rdf_file, args.store_file)

store = Store(args.store_file)

#get_and_save_venues_data(store, args.conferences_file, args.journals_file)
get_and_save_institutions_data(store, args.institutions_file, args.corrected_institution_duplicates_file)