"""
Collection custom exception
"""


class TreeDirNoneExist(Exception):
    """
    Except if TreeStorage class initialized without `path` parameter
    """
    pass
