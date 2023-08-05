"""
Setting config for storage
"""


class TreeConfig:
    """
    Class for initialize config params
    """

    def __init__(self, params=None, **kwargs):

        if params:
            for key, value in params.items():
                setattr(self, key, value)

        for key, value in kwargs.items():
            setattr(self, key, value)
