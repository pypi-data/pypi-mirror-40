"""
Testing add file to the storage
"""

import io
import os
import shutil
from unittest import TestCase
from PIL import Image

from tree_storage.tree import TreeStorage


class TreeBreedTest(TestCase):

    path = os.path.dirname(os.path.abspath(__file__)) + "/storage/"

    def setUp(self):
        self.tree = TreeStorage(path=self.path)

    def tearDown(self):
        if os.path.isfile(self.path):
            shutil.rmtree(self.path)

    def test_insert_simple_picture(self):
        """
        Test upload simple picture
        """
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        status_insert = self.tree.breed(file.read())
        self.assertIsNotNone(status_insert)
