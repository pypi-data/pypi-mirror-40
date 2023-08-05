from os import path


def read_txt_file(filename: str, dirpath: str = None) -> str:
    if dirpath is not None:
        filepath = path.join(dirpath, filename)
    else:
        filepath = path.realpath(filename)

    assert path.isfile(filepath)

    with open(filepath, 'r') as f:
        return f.read()
