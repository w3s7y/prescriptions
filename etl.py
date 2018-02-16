"""Python module to handle the extract from CSV, transform (strip whitespace, etc) and load into postgres."""
import os
import sqlalchemy
import googlemaps
import pandas


class haz_bad_data_load_exception(Exception):
    pass


class data_extractor:
    """The 'E' in ETL.
    Opens the file handles and makes the raw CSV payload available to transform."""

    def __init__(self, gp_address_file, prescriptions_file, drug_subs_file):
        self.addresses = pandas.read_csv(open(gp_address_file, 'r'))
        self.prescriptions = pandas.read_csv(open(prescriptions_file, 'r'))
        self.chem_subs = pandas.read_csv(open(drug_subs_file, 'r'))


class data_transformer:
    """The 'T' in ETL (Also another 'E' for Enrichment?)"""

    def __init__(self, google_api_token, extractor):
        self.gmaps = googlemaps.Client(key=google_api_token)
        self.extractor = extractor

    def transform_and_enrich_addresses(self):
        addrs = self.extractor.addresses  # Pandas DataFrame object

        # Strip off the 'yrmon' column (it's GARRRBAGGE)
        addrs = addrs.drop(columns=['yrmon'])

        # str.strip(), str.lower() and str.capitalize() address fields.
        for field in ['practice_name', 'address_1', 'address_2', 'address_3', 'address_4']:
            addrs[field] = addrs[field].map(lambda x: x.strip().lower().capitalize())

        # TODO Adding 2 new fields 'latitude' and 'longitude' gathered from google geolocation API

        return addrs

    def transform_and_enrich_prescriptions(self):
        scripts = self.extractor.prescriptions

        # cut crap columns off
        scripts = scripts.drop(columns=['period', 'blank'])

        # Strip whitespace off text cols
        for field in ['drug_name']:
            scripts[field] = scripts[field].map(lambda x: x.strip())

        return scripts

    def transform_and_enrich_subs(self):
        subs = self.extractor.chem_subs

        # Drop the blank column off the end
        subs = subs.drop(columns=['blank'])

        # Strip the fields of whitespace
        for field in ['chemical_code', 'chemical_name']:
            subs[field] = subs[field].map(lambda x: x.strip())

        return subs

class data_loader:
    """The 'L' in ETL"""
    def __init__(self, db_host, db_username, db_password, db_name, db_schema, transformer):
        self.db_engine = sqlalchemy.create_engine(
            'postgresql+psycopg2://{}:{}@{}/{}'.format(db_username, db_password, db_host, db_name))
        self.transformer = transformer
        self.schema = db_schema

    def load(self, table_name):
        if table_name == 'addresses':
            self.transformer.transform_and_enrich_addresses().to_sql(
                table_name, self.db_engine, schema=self.schema, if_exists='replace')
        elif table_name == 'scripts':
            self.transformer.transform_and_enrich_prescriptions().to_sql(
                table_name, self.db_engine, schema=self.schema, if_exists='replace', chunksize=100000)
        elif table_name == 'subs':
            self.transformer.transform_and_enrich_subs().to_sql(
                table_name, self.db_engine, schema=self.schema, if_exists='replace')
        else:
            raise haz_bad_data_load_exception

class etl_controller:
    """Defaults and stuff, basic logic control."""

    def __init__(self):
        # Vars for the Extractor
        gp_addresses = 'T201710ADDR+BNFT.CSV'
        prescriptions_data = 'T201710PDPI+BNFT.CSV'
        drug_substitutions = 'T201710CHEM+SUBS.CSV'

        # Vars for the data transformer & enrichment
        google_token = os.environ.get('GOOGLE_API_TOKEN')

        # Vars for the loader
        db_user = os.environ.get('DB_USER')
        db_pass = os.environ.get('DB_PASS')
        db_host = os.environ.get('DB_HOST')
        db_name = os.environ.get('DB_NAME')
        db_schema = os.environ.get('DB_SCHEMA')

        # Create the ETL objects.
        self.extractor = data_extractor(gp_addresses, prescriptions_data, drug_substitutions)
        self.transformer = data_transformer(google_token, self.extractor)
        self.loader = data_loader(db_host, db_user, db_pass, db_name, db_schema, self.transformer)


# Main run code
if __name__ == '__main__':
    print('This is not designed to be ran from the command line, only imported into other modules.')
