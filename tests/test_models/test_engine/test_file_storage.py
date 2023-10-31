#!/usr/bin/python3
"""Contains the TestFileStorage Unittests"""
from datetime import datetime
from models import *
from models.engine.file_storage import FileStorage
import os
import unittest


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') == 'db',
                 "Database storage is not using FileStorage")
class TestFileStorage(unittest.TestCase):
    """Test the file storage class"""
    def setUp(self):
        """Set up the test environment"""
        self.store = FileStorage()

        test_args = {'updated_at': datetime(2017, 2, 12, 0, 31, 53, 331997),
                     'id': 'f519fb40-1f5c-458b-945c-2ee8eaaf4900',
                     'created_at': datetime(2017, 2, 12, 0, 31, 53, 331900)}
        self.model = BaseModel(**test_args)

        self.test_len = len(self.store.all())

    def test_all(self):
        """Test the all() method"""
        self.assertEqual(len(self.store.all()), self.test_len)

    def test_all_arg(self):
        """Test the all(cls) method"""
        new_obj = State()
        new_obj.save()
        everything = self.store.all()
        nb_states = 0
        for e in everything.values():
            if e.__class__.__name__ == "State":
                nb_states += 1
        self.assertEqual(len(self.store.all("State")), nb_states)

    def test_new(self):
        """Test the new() method"""
        test_len = len(self.store.all())
        new_obj = State()
        new_obj.save()
        self.assertEqual(len(self.store.all()), test_len + 1)
        a = BaseModel()
        a.save()
        self.assertEqual(len(self.store.all()), self.test_len + 2)

    def test_save(self):
        """Test the save() method"""
        self.test_len = len(self.store.all())
        a = BaseModel()
        a.save()
        self.assertEqual(len(self.store.all()), self.test_len + 1)
        b = User()
        self.assertNotEqual(len(self.store.all()), self.test_len + 2)
        b.save()
        self.assertEqual(len(self.store.all()), self.test_len + 2)

    def test_reload(self):
        """Test the reload() method"""
        self.model.save()
        a = BaseModel()
        a.save()
        self.store.reload()
        for value in self.store.all().values():
            self.assertIsInstance(value.created_at, datetime)

    def test_state(self):
        """Test State creation with an argument"""
        a = State(name="nairobi", id="nairobi254")
        a.save()
        self.assertIn("nairobi254", self.store.all("State").keys())

    def test_count(self):
        """Test the count() method"""
        test_len = len(self.store.all())
        a = Amenity(name="test_amenity")
        a.save()
        self.assertEqual(test_len + 1, self.store.count())

    def test_count_arg(self):
        """Test the count(cls) method"""
        test_len = len(self.store.all("Amenity"))
        a = Amenity(name="test_amenity_2")
        a.save()
        self.assertEqual(test_len + 1, self.store.count("Amenity"))

    def test_count_bad_arg(self):
        """Test the count() method with a bad class name"""
        self.assertEqual(-1, self.store.count("Dummy"))

    def test_get(self):
        """Test the get(cls, id) method with valid cls and id"""
        a = Amenity(name="test_amenity3", id="test_3")
        a.save()
        result = self.store.get("Amenity", "test_3")
        self.assertEqual(a.name, result.name)
        self.assertEqual(a.created_at, result.created_at)

    def test_get_bad_cls(self):
        """Test the get(cls, id) method with an invalid cls"""
        result = self.store.get("Dummy", "test")
        self.assertIsNone(result)

    def test_get_bad_id(self):
        """Test the get(cls, id) method with an invalid id"""
        result = self.store.get("State", "very_bad_id")
        self.assertIsNone(result)


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(1, os.path.join(os.path.split(__file__)[0], '../../..'))
    from models import *
    from models.engine.file_storage import FileStorage
    unittest.main()
