import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets')
DAGS_DIR = os.path.join(ROOT_DIR, 'dags')


DBT_PROFILES_PARAM_NAMES = [
    'DBT_ACCOUNT',
    'DBT_USER',
    'DBT_PASSWORD',
    'DBT_DATABASE',
    'DBT_SCHEMA',
    'DBT_WAREHOUSE',
    'DBT_ROLE'
]
