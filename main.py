# Importar bibliotecas
import numpy as np
import pandas as pd
import pyodbc
import pandera as pa

from app.etl import extract_from_sql_server
from app.extract_validation import extract_from_sql_server_and_validate


with open(r'sql\SELECT_PERSON.sql', 'r') as person:
    query_person = person.read()


if __name__ == '__main__':
    
    #df = extract_from_sql_server(query_person)
    df = extract_from_sql_server_and_validate(query_person)

    print(df.head())
