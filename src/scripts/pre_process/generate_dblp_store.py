

from pyoxigraph import Store, RdfFormat

data_path = 'data/raw/dblp.ttl'

# Persistent database stored on disk
store = Store("data/raw/dblp_store")

# Run this once to import the dataset
store.bulk_load(
    path=data_path,
    format=RdfFormat.TURTLE,
)