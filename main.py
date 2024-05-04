# Importar bibliotecas
import pandas as pd
import numpy as np
import pyodbc
from app.etl import extract_from_sql_server


with open(r'sql\SELECT_PERSON.sql', 'r') as person:
    query_person = person.read()


if __name__ == '__main__':
    
    df = extract_from_sql_server(query_person)

    print(df.head())
