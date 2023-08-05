# coding:utf-8


def read_to_list(path_to_file):
    rows = []
    for line in open(path_to_file).readlines():
        line = line.strip()
        if line != '' and not line.startswith('#'):
            rows.append(line)

    return rows
