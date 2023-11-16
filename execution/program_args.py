import os
import json


def get_program_args():
    # Obtendo o caminho absoluto para o arquivo

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(parent_dir, os.pardir, "exec_configs.json")

    with open(filepath, "r") as file:
        args = json.load(file)

    return args
