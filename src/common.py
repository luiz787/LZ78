import os

NUMBER_SIZE = 3


def longest_common_prefix(str1, str2):
    prefix = ""
    size = min(len(str1), len(str2))

    for i in range(size):
        if str1[i] is not str2[i]:
            return prefix
        else:
            prefix += str1[i]

    return prefix


def get_filename_no_extension(filename):
    basename = os.path.basename(filename)
    return os.path.splitext(basename)[0]
