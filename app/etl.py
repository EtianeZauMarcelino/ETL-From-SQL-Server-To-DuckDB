# Ignore warnings
import warnings

# Importar bibliotecas
import numpy as np
import pandas as pd
import pandera as pa
import pyodbc

from config.config import configuracoes

warnings.filterwarnings("ignore")

# Conexão com o server
def extract_from_sql_server(query: str) -> pd.DataFrame:
    """
    Extracts data from a SQL Server database using the provided query and returns it as a pandas DataFrame.

    Parameters:
    - query (str): SQL query to extract data from the SQL Server database.

    Returns:
    - pd.DataFrame: DataFrame containing the extracted data.

    Raises:
    - Exception: If there's an error during the extraction process.

    Example:
    ```
    data = extract_from_sql_server("SELECT * FROM TableName")
    ```
    """
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

        with open(f'schema\schema_AdventureWorks.py', 'w', encoding='utf-8') as schema_Adventure_Works:
            schema_Adventure_Works.write(schema_AdventureWorks.to_script())

    except Exception as error:
        sql_server_Connection.close()
        print("SQLSERVER01 Disconnected because of an error")

        print(f"Error message: {error}")

    finally:
        sql_server_Connection.close()

    return df_AdventureWorks
