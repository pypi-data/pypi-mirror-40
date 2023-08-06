import os

from tree_storage.exceptions import TreeDirNoneExist
from tree_storage.utils import hash_to_path, hashing_file


class TreeStorage:
    """
    Main object for manipulate of the storage
    """

    file_hash_name = None
    full_path_to_file = None
    hash_dir = None
    hash_file = None

    def __init__(self, path):
        """
        When initialize TreeStorage client
        must be write path where want to save files
        """
        self.path_to_tree = path
        if not self.path_to_tree:
            raise TreeDirNoneExist

    def breed(self, file_byte, mode='wb'):
        """
        Insert file to the data tree storage
        """
        try:
            self.file_hash_name = hashing_file(file_byte)
            self.hash_dir, self.hash_file = hash_to_path(hash_name=self.file_hash_name)
            os.makedirs(os.path.join(self.path_to_tree, self.hash_dir))
            self.full_path_to_file = os.path.join(self.path_to_tree, self.hash_dir, self.hash_file)
            with open(self.full_path_to_file, mode=mode) as file_hash:
                file_hash.write(file_byte)
                return self.file_hash_name
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
