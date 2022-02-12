import os


def read_file(filedir: str, name: str) -> str:
    path = os.path.join(filedir, name)
    with open(path, "r") as f:
        return f.read()
