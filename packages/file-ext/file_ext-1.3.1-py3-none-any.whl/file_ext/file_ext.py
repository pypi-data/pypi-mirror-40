# coding:utf-8
import os


def read_to_list(path_to_file: str):
    if os.path.exists(path_to_file):
        rows = list()
        for line in open(path_to_file).readlines():
            line = line.strip()
            if line != '' and not line.startswith('#'):
                rows.append(line)

        return rows

    import xprint as xp
    xp.error('"{}" does not exist.'.format(path_to_file))
    return list()
