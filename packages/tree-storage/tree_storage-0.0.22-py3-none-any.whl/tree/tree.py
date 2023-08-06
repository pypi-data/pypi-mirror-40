import os

from tree.exceptions import (
    TreeFileNoneExist,
    TreeDirNoneExist,
)
from tree.utils import (
    hash_to_path,
    hashing_file,
)


class TreeStorage:
    """
    Main object for the manipulate of the tree storage
    """

    def __init__(self, path=None):
        """
        When initialize TreeStorage client
        must be initialize TreeConfig
        """
        self.path_to_tree = path
        if not self.path_to_tree:
            raise TreeDirNoneExist
        self.file_hash_name = ''

    def breed(self, file_byte, mode='wb'):
        """
        Insert file to the data tree storage
        """
        try:
            self.file_hash_name = hashing_file(file_byte)
            hash_dir, hash_file = hash_to_path(hash_name=self.file_hash_name)
            os.makedirs(os.path.join(self.path_to_tree, hash_dir))
            with open(os.path.join(self.path_to_tree, hash_dir, hash_file),
                      mode=mode) as file_hash:
                return file_hash.write(file_byte)
        except IOError as error:
            return error.filename

    def cut(self, file_hash_name, greedy=False):
        """
        Remove file from the tree storage
        """
        if greedy:
            pass  # TODO: if dir is empty must be remove
        hash_dir, hash_file = hash_to_path(hash_name=file_hash_name)
        path = os.path.join(self.path_to_tree, hash_dir, hash_file)
        if os.path.isfile(path):
            return os.remove(path)
