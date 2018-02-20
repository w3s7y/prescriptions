"""Elasticsearch ingest pipeline"""
import sqlalchemy
import elasticsearch
import pandas
import os

elastic_host = os.environ.get('ELASTIC_HOST')
elastic_port = os.environ.get('ELASTIC_PORT')
elastic_index = os.environ.get('ELASTIC_INDEX')
elastic_client = elasticsearch.Elasticsearch('http://{}:{}'.format(elastic_host, elastic_port))

def load_addresses():
    df = pandas.read_sql_table(
        'addresses',
        sqlalchemy.create_engine('postgresql+psycopg2://ubuntu:1234qwer@192.168.33.122:5432/test'),
        schema='prescriptions')



