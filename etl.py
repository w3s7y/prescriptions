"""Python module to handle the extract from CSV, transform (strip whitespace, etc) and load into postgres."""
import os
import sqlalchemy
import googlemaps
import pandas
import logging

logger = logging.getLogger(__name__)
handle = logging.FileHandler('prescriptions.log')
handle.setLevel(logging.DEBUG)
logger.addHandler(handle)


class EtlPipeline:
    def __init__(self, gp_address_file, prescriptions_file, drug_subs_file, chunk_size, google_token,
                 db_host, db_username, db_password, db_name, db_schema):
        self.db_engine = sqlalchemy.create_engine(
            'postgresql+psycopg2://{}:{}@{}/{}'.format(db_username, db_password, db_host, db_name))
        self.schema = db_schema
        self.gmaps = googlemaps.Client(key=google_token)

        self.addresses = pandas.read_csv(open(gp_address_file, 'r'), chunksize=chunk_size)
        self.prescriptions = pandas.read_csv(open(prescriptions_file, 'r'), chunksize=chunk_size)
        self.substitutions = pandas.read_csv(open(drug_subs_file, 'r'), chunksize=chunk_size)

    def transform_and_load_addresses(self):
        logger.info('Running address transform.')
        for chunk in self.addresses:
            chunk = chunk.drop(columns=['yrmon'])
            for field in ['practice_name', 'address_1', 'address_2', 'address_3', 'address_4']:
                chunk[field] = chunk[field].map(lambda x: x.strip().lower().capitalize())

            # TODO Adding 2 new fields 'latitude' and 'longitude' gathered from google geo location API
            self.load('addresses', chunk)

    def transform_and_load_prescriptions(self):
        for chunk in self.prescriptions:
            chunk = chunk.drop(columns=['period', 'blank'])
            for field in ['drug_name']:
                chunk[field] = chunk[field].map(lambda x: x.strip())
            self.load('prescriptions', chunk)

    def transform_and_load_subs(self):
        for chunk in self.substitutions:
            chunk = chunk.drop(columns=['blank'])
            for field in ['chemical_code', 'chemical_name']:
                chunk[field] = chunk[field].map(lambda x: x.strip())
            self.load('substitutions', chunk)

    def load(self, table, chunk):
        chunk.to_sql(
            table, self.db_engine, schema=self.schema, if_exists='append')


class etl_controller:
    """Defaults and stuff, basic logic control."""

    def __init__(self):
        # Vars for the Extractor
        gp_addresses = 'T201710ADDR+BNFT.CSV'
        prescriptions_data = 'T201710PDPI+BNFT.CSV'
        drug_substitutions = 'T201710CHEM+SUBS.CSV'
        chunk_size = 1000

        # Vars for the data transformer & enrichment
        google_token = os.environ.get('GOOGLE_API_TOKEN')

        # Vars for the loader
        db_user = os.environ.get('DB_USER', default='ubuntu')
        db_pass = os.environ.get('DB_PASS', default='1234qwer')
        db_host = os.environ.get('DB_HOST', default='192.168.33.122')
        db_name = os.environ.get('DB_NAME', default='test')
        db_schema = os.environ.get('DB_SCHEMA', default='prescriptions')
        # Create the pipeline object.
        self.pipeline = EtlPipeline(gp_addresses, prescriptions_data, drug_substitutions, chunk_size, google_token,
                                    db_host, db_user, db_pass, db_name, db_schema)

    def run_pipe(self):
        self.pipeline.transform_and_load_addresses()
        self.pipeline.transform_and_load_prescriptions()
        self.pipeline.transform_and_load_subs()
