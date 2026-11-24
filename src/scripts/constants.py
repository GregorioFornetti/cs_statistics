import os

# General data paths
DATA_PATH = 'data'
PROCESSED_DATA_PATH = os.path.join(DATA_PATH, 'processed')
RAW_DATA_PATH = os.path.join(DATA_PATH, 'raw')
TEMP_DATA_PATH = os.path.join(DATA_PATH, 'temp')
UTILS_DATA_PATH = os.path.join(DATA_PATH, 'utils')

# DBLP RDF files
DBLP_RDF_FILE = os.path.join(RAW_DATA_PATH, 'dblp.ttl')
DBLP_RDF_GZ_FILE = os.path.join(RAW_DATA_PATH, 'dblp.ttl.gz')
DBLP_STORE_FILE = os.path.join(RAW_DATA_PATH, 'dblp_store')
DBLP_RAW_METADATA_FILE = os.path.join(RAW_DATA_PATH, 'dblp_metadata.txt')

# Utils files
CORRECTED_INSTITUTION_DUPLICATES_FILE = os.path.join(UTILS_DATA_PATH, 'corrected_institution_duplicates.json')

# Temp files
DUPLICATE_INSTITUTIONS_FILE = os.path.join(TEMP_DATA_PATH, 'duplicate_institutions.json')
DUPLICATE_INSTITUTIONS_NOT_CORRECTED_FILE = os.path.join(TEMP_DATA_PATH, 'duplicate_institutions_not_corrected.json')

# Processed files
CONFERENCES_FILE = os.path.join(PROCESSED_DATA_PATH, 'conferences.json')
JOURNALS_FILE = os.path.join(PROCESSED_DATA_PATH, 'journals.json')
INSTITUTIONS_FILE = os.path.join(PROCESSED_DATA_PATH, 'institutions.json')
METADATA_FILE = os.path.join(PROCESSED_DATA_PATH, 'metadata.json')
CONF_COUNT_BY_UNI_FOLDER = os.path.join(PROCESSED_DATA_PATH, 'conf_count_by_uni')
JOURNAL_COUNT_BY_UNI_FOLDER = os.path.join(PROCESSED_DATA_PATH, 'journal_count_by_uni')
COUNTRIES_BY_CONTINENT_FILE = os.path.join(PROCESSED_DATA_PATH, 'countries_by_continent.json')
COUNTRIES_TO_ISO_CODES_FILE = os.path.join(PROCESSED_DATA_PATH, 'countries_to_iso_codes.json')
INSTITUTIONS_BY_COUNTRY_ISO_CODES_FILE = os.path.join(PROCESSED_DATA_PATH, 'institutions_by_country_iso_codes.json')