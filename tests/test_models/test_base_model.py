"""Defines unittests for models/base_model.py file."""

import unittest
import models
from models.base_model import BaseModel
from datetime import datetime
import os


class Test_Base_Model_Innit(unittest.TestCase):
    """unittests for instantiation of the Basemodel class."""

    def test_id(self):
        """Tests that the BaseModels id is of str type and is unique"""

        self.assertEqual(str, type(BaseModel().id))
        Bmodel1 = BaseModel()
        Bmodel2 = BaseModel()
        self.assertNotEqual(Bmodel1.id, Bmodel2.id)

    def test_created_and_updated_at_type(self):
        """Tests that the BaseModels created_at and updated_at are of datetime
        type """

        self.assertEqual(datetime, type(BaseModel().created_at))
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_created_and_updated_at_values(self):
        """Tests that the BaseModels created_at and updated_at values differ at
        different times"""
