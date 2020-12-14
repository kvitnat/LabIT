import unittest
import os
from db_manager.database import DBManager, Table, Types


class DBTestCase(unittest.TestCase):
    manager = DBManager()

    def setUp(self):
        self.manager.path = "../"

    def test_get_nonexisting_table(self):
        with self.assertRaises(LookupError):
            self.manager.get_table("nan_db", "nonexisting_table")

    def test_delete_nonexisting_table(self):
        with self.assertRaises(LookupError):
            self.manager.delete_table("nan_db", "nonexisting_table")

    def test_create_existing_table(self):
        with self.assertRaises(LookupError):
            self.manager.create_table("nan_db", "existing_table")

    def test_create_table(self):
        self.manager.create_table("nan_db", "new_table")
        try:
            self.manager.get_table("nan_db", "new_table")
            self.manager.delete_table("nan_db", "new_table")
        except LookupError:
            self.fail("could not get table created by create_table")

    def test_intersection(self):
        table1 = self.manager.get_table("nan_db", "songs_table")
        table2 = self.manager.get_table("nan_db", "songs1_table")
        filename = os.path.join(self.manager.path, "nan_db", "intersection.json")
        if self.manager.exists("nan_db", "intersection"):
            self.manager.delete_table("nan_db", "intersection")
        table = Table.intersection(table1, table2, filename)
        self.assertEqual(table.row_count(), 3, "intersection should contain 3 rows")


if __name__ == '__main__':
    unittest.main()
