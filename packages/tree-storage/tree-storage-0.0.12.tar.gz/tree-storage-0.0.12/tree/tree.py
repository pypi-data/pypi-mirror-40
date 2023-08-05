import os

from tree.exceptions import (
    TreeConfigNoneExist,
    TreeFileNoneExist,
)
from .utils import (
    hash_to_path,
    hashing_file,
)


class TreeStorage:
    """
    Main object for the manipulate of the tree storage
    """

    def __init__(self, config=None):
        """
        When initialize TreeStorage client
        must be initialize TreeConfig
        """
        if not config:
            raise TreeConfigNoneExist
        self.config = config
        self.file_hash_name = ''

    def breed(self, file_byte, mode='wb'):
        """
        Insert file to the data tree storage
        """
        try:
            self.file_hash_name = hashing_file(file_byte)
            hash_dir, hash_file = hash_to_path(hash_name=self.file_hash_name)
            os.makedirs(self.config.PATH_TO_TREE + hash_dir)
            with open(os.path.join(self.config.PATH_TO_TREE, hash_dir, hash_file),
                      mode=mode) as file_hash:
                return file_hash.write(file_byte)
        except IOError as error:
            return error.filename

    def cut(self, file_hash_name, greedy=False):
        """
        Remove file from the tree storage
        """
        try:
            if greedy:
                pass  # TODO: if dir is empty must be remove
            hash_dir, hash_file = hash_to_path(hash_name=file_hash_name)
            path = os.path.join(self.config.PATH_TO_TREE, hash_dir, hash_file)
            return os.remove(path)
        except TreeFileNoneExist(file_hash_name=file_hash_name) as error:
            return error.msg
