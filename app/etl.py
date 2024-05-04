# Importar bibliotecas
import pandas as pd

import numpy as np
import pyodbc
from config.config import configuracoes

import pandera as pa

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

# Conexão com o server
def extract_from_sql_server(query: str) -> pd.DataFrame:

    config = configuracoes()

    try:
        sql_server_Connection = pyodbc.connect(
            f"""DRIVER={'SQL Server'};
                SERVER={config['db_server']};
                DATABASE={config['db_name']};
                UID={config['db_user']};
                PWD={config['db_pass']};"""
        )

        sql_server_cursor = sql_server_Connection.cursor()
        print("SQLSERVER01 Server Connected")

        df_AdventureWorks = pd.read_sql(query, sql_server_Connection)

        schema_AdventureWorks = pa.infer_schema(df_AdventureWorks)

        with open(f'schema\schema_AdventureWorks.py', 'w', encoding='utf-8') as schema_file:
            schema_file.write(schema_AdventureWorks.to_script())

    except Exception as error:
        sql_server_Connection.close()
        print("SQLSERVER01 Disconnected because of an error")

        print(f"Error message: {error}")

    finally:
        sql_server_Connection.close()

    return df_AdventureWorks


