from kubernetes.client import models as k8s
from dotenv import load_dotenv
import os
from typing import List, Union


def generate_k8s_secrets(secret_names: List[str]) -> List[k8s.V1EnvVar]:
    """
    Generate k8s secrets from environment variables.

    :param secret_names: A list of secret names
    :return: A list of k8s secrets
    """
    load_dotenv()
    return [
        k8s.V1EnvVar(name=name, value=os.environ.get(name, "")) for name in secret_names
    ]


def read_sql(path: str, multi: bool = False) -> Union[str, List[str]]:
    """
    Read a file at a given path
    :param path: filepath string
    :param multi: whether the file contains multiple statements or not
    :return: query string or list of query strings
    """
    try:
        with open(path, "r") as f:
            contents = f.read()

        if multi:
            statements = contents.split(";")
            return [i for i in statements if i != ""]
        else:
            return contents
    except FileNotFoundError:
        raise
    except Exception:
        raise
