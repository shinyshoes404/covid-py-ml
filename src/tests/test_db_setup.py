import unittest, mock, os, platform

# import function to test
from db_setup import build_db

@mock.patch('db_ops.db_ops.DbConfig') # create mock DbConfig for entire class
class TestDbSetupBuilDb(unittest.TestCase):
    
    def setUp(self):
        # set a new db dir and file path for testing
        self.TEST_DIR = os.path.dirname(os.path.abspath(__file__))
        if platform.system() == "Windows":
            self.TEMP_DB_DIR = os.path.join(self.TEST_DIR, ".\\data_test")
            self.DB_PATH = os.path.join(self.TEMP_DB_DIR, ".\\test.db")
            
        else:
            self.TEMP_DB_DIR = os.path.join(self.TEST_DIR, "./data_test")
            self.DB_PATH = os.path.join(self.TEMP_DB_DIR, "./test.db")
            

    def tearDown(self):
        # clean up any dirs or files created during testing
        if os.path.isfile(self.DB_PATH):
            os.remove(self.DB_PATH)
        if os.path.isdir(self.TEMP_DB_DIR):
            os.rmdir(self.TEMP_DB_DIR)
    
    # verify db is created
    def test_db_creates(self, mock_db_config):
        # add the properties to our mock_db_config object
        type(mock_db_config).db_dir = mock.PropertyMock(return_value=self.TEMP_DB_DIR)
        type(mock_db_config).db_path = mock.PropertyMock(return_value=self.DB_PATH)

        # create the database
        build_db()

        # verify that the database was created in the test location
        self.assertEqual(os.path.isfile(self.DB_PATH), True, "db file should be created, expecting True")

if __name__ == "__main__":
    unittest.main()