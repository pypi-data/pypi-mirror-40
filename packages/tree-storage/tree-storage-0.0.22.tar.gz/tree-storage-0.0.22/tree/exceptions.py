"""
Collection custom exception
"""


class TreeDirNoneExist(Exception):
    """
    Error class if storage initializing  without config parameter
    """
    def __init__(self):
        self.msg = "Storage initialize must be have a config variable"


class TreeFileNoneExist(FileNotFoundError):
    """
    Error class if hash non exist in tree storage
    """
    def __init__(self, file_hash_name):
        self.msg = "File with such hash is not found: {}".format(file_hash_name)
