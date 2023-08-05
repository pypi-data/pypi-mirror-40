from os import path


def file_parts(path_str):
    dir_name = path.dirname(path_str)
    file_postfix = path.basename(path_str)
    return [dir_name] + list(path.splitext(file_postfix))
