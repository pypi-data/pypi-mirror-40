"""
Testing delete file from storage
"""
import io
import os
import shutil
from unittest import TestCase

from PIL import Image

from tree_storage.tree import TreeStorage
from tree_storage.utils import hash_name_generator


class TreeCutTest(TestCase):

    path = os.path.dirname(os.path.abspath(__file__)) + "/storage/"

    def setUp(self):
        self.tree = TreeStorage(path=self.path)

    def tearDown(self):
        if os.path.isfile(self.path):
            shutil.rmtree(self.path)

    def test_remove_simple_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        self.tree.breed(file.read())
        status_remove = self.tree.cut(self.tree.file_hash_name)
        self.assertEqual(status_remove, None)

    def test_cut_non_exist_file(self):
        self.assertEqual(self.tree.cut(hash_name_generator()), None)
