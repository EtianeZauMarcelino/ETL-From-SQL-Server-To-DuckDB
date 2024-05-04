import os
from dotenv import load_dotenv

def configuracoes():
    load_dotenv(r'env\.env')

    settings = {
        "db_server" : os.getenv("server"),
        "db_name" : os.getenv("db"),
        "db_user" : os.getenv("user"),
        "db_pass" : os.getenv("pw")
    }

    return settings


