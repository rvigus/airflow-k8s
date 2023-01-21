from kubernetes.client import models as k8s
from dotenv import load_dotenv
import os

def generate_k8s_secrets(secret_names):
    load_dotenv(verbose=True)
    k8s_secrets = []
    for name in secret_names:
        k8s_secrets.append(
            k8s.V1EnvVar(name=name, value=os.environ.get(name, ''))
        )
    return k8s_secrets

def read_sql(path: str, multi=False):
    """
    Read a file at a given path
    :param path: filepath string
    :return: query string
    """
    try:
        with open(path, "r") as f:
            contents = f.read()

        if multi:
            statements = contents.split(';')
            return [i for i in statements if i != '']
        else:
            return contents
    except FileNotFoundError:
        raise
    except Exception:
        raise