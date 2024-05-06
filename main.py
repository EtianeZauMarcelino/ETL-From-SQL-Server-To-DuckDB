# Importar bibliotecas
import duckdb
import numpy as np
import pandas as pd
import pandera as pa
import pyodbc

from app.etl import extract_from_sql_server
from app.extract_validation import (extract_from_sql_server_and_validate,
                                    load_from_sql_server_to_duckdb,
                                    read_from_duckdb_and_print)

with open(r'sql\SELECT_PERSON.sql', 'r') as person:
    query_person = person.read()


if __name__ == '__main__':
    
    #df = extract_from_sql_server(query_person)
    df = extract_from_sql_server_and_validate(query_person)

    #load_from_sql_server_to_duckdb(df=df, table_name="tabela_from_sql_server")

    # Nome da tabela para consulta
    table_name = "tabela_from_sql_server"
    
    # Ler dados da tabela e imprimir os resultados
    read_from_duckdb_and_print(table_name)

    # print(df.head())
