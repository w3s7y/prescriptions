"""Elasticsearch ingest pipeline, reads SQL database and creates elasticsearch docs (1 per row)."""
import sqlalchemy
import elasticsearch
import pandas
import os
import logging


elastic_host = os.environ.get('ELASTIC_HOST', default='localhost')
elastic_port = os.environ.get('ELASTIC_PORT', default='9200')
elastic_index = os.environ.get('ELASTIC_INDEX', default='prescriptions')
elastic_client = elasticsearch.Elasticsearch('http://{}:{}'.format(elastic_host, elastic_port))


def load_addresses():
    df = pandas.read_sql_table(
        'addresses',
        sqlalchemy.create_engine('postgresql+psycopg2://ubuntu:1234qwer@192.168.33.122:5432/test'),
        schema='prescriptions')


