# Ignore warnings
import warnings

# Importar bibliotecas
import numpy as np
import pandas as pd
import pandera as pa
import pyodbc

from schema.schema_AdventureWorks import schema_Adventure_Works

from config.config import configuracoes

warnings.filterwarnings("ignore")

# Conexão com o server
@pa.check_output(schema_Adventure_Works, lazy=True)
def extract_from_sql_server_and_validate(query: str) -> pd.DataFrame:
    """
    
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

        # schema_AdventureWorks = pa.infer_schema(df_AdventureWorks)

        # with open(f'schema\schema_AdventureWorks.py', 'w', encoding='utf-8') as schema_file:
        #     schema_file.write(schema_AdventureWorks.to_script())

    except Exception as error:
        sql_server_Connection.close()
        print("SQLSERVER01 Disconnected because of an error")

        print(f"Error message: {error}")

    finally:
        sql_server_Connection.close()

    return df_AdventureWorks



import duckdb


@pa.check_input(schema_Adventure_Works, lazy=True)
def load_from_sql_server_to_duckdb(df: pd.DataFrame, table_name: str, db_file: str = 'From_SQL_Server.db'):
    """
    Carrega o DataFrame no DuckDB, criando ou substituindo a tabela especificada.

    Args:
        df: DataFrame do Pandas para ser carregado no DuckDB.
        table_name: Nome da tabela no DuckDB onde os dados serão inseridos.
        db_file: Caminho para o arquivo DuckDB. Se não existir, será criado.
    """
    # Conectar ao DuckDB. Se o arquivo não existir, ele será criado.
    con = duckdb.connect(database=db_file, read_only=False)
    
    # Registrar o DataFrame como uma tabela temporária
    con.register('df_from_sql_server', df)
    
    # Utilizar SQL para inserir os dados da tabela temporária em uma tabela permanente
    # Se a tabela já existir, substitui.
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df_from_sql_server")
    
    # Fechar a conexão
    con.close()



def read_from_duckdb_and_show(table_name: str, db_file: str = 'From_SQL_Server.db'):
    """
    Lê dados de uma tabela DuckDB e imprime os resultados.

    Parâmetros:
    - table_name: Nome da tabela de onde os dados serão lidos.
    - db_file: Caminho para o arquivo DuckDB.
    """
    # Conectar ao DuckDB
    con = duckdb.connect(database=db_file)

    # Executar consulta SQL
    con.sql(f"""
        SELECT * FROM {table_name} limit 10
        """).show()

    # Fechar a conexão
    con.close()

    # Imprimir os resultados
    # for row in result:
    #     print(row)