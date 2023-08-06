'''
Optional module to persist dataset dataframes in database instead of filesystem
'''

from simpleml.persistables.base_sqlalchemy import BaseSQLAlchemy
from sqlalchemy import MetaData, event, DDL

__author__ = 'Elisha Yadgaran'

# Use different schemas/databases for storage optionality (dataframes are big in size)
DATASET_SCHEMA = 'DATASETS'
# Separate out for clarity - can merge later
RAW_DATASET_SCHEMA = 'RAW_DATASETS'


class DatasetStorage(BaseSQLAlchemy):
    __abstract__ = True
    metadata = MetaData(schema=DATASET_SCHEMA)
    event.listen(metadata, 'before_create', DDL('''CREATE SCHEMA IF NOT EXISTS "{}";'''.format(DATASET_SCHEMA)))


class RawDatasetStorage(BaseSQLAlchemy):
    __abstract__ = True
    metadata = MetaData(schema=RAW_DATASET_SCHEMA)
    event.listen(metadata, 'before_create', DDL('''CREATE SCHEMA IF NOT EXISTS "{}";'''.format(RAW_DATASET_SCHEMA)))
