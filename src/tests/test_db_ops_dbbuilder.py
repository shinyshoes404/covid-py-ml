import unittest, mock, os, platform


# import class to test
from db_ops.db_ops import DbBuilder

@mock.patch('db_ops.db_ops.DbConfig') # create mock DbConfig for entire class
class TestDbBuilder(unittest.TestCase):

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
    
    @mock.patch("covid_ml.data_ops.DbChecker.check_for_db", return_value=True)
    def test_integ_dbexists_nocreate(self,mock_check_db, mock_db_config):
        # add the properties to our mock_db_config object
        type(mock_db_config).db_dir = mock.PropertyMock(return_value=self.TEMP_DB_DIR)
        type(mock_db_config).db_path = mock.PropertyMock(return_value=self.DB_PATH)

        # create the db dir that would be used to store the db file
        os.mkdir(self.TEMP_DB_DIR)
        # instantiate the DbBuilder class, which will then run the DbChecker.check_for_db method
        # which we have mocked to return True, indicating that there is a db file already created
        # but we are intentially not creating one
        check_obj = DbBuilder()

        # run the create_db() method. We are execting this method to think that a db file already exists
        # (even though we intentionally did not create one), and therefore not create any sqlite connections
        check_obj.create_db()

        # if the connection was created in the method we just called, sqlite would automatically create
        # db file. If everything worked correctly, there should be not db file. Let's check
        self.assertEqual(os.path.exists(self.DB_PATH), False, "Should be no db file, expecting False")

        # the tearDown fixture will clean up the directory we made
    
    # no db dir or db file exists, expecting the classes to work together to
    # 1) create db dir  2) create db file in db dir when connection is created 3) run the create statements
    def test_integ_nodb_createdb(self, mock_db_config):
        # add the properties to our mock_db_config object
        type(mock_db_config).db_dir = mock.PropertyMock(return_value=self.TEMP_DB_DIR)
        type(mock_db_config).db_path = mock.PropertyMock(return_value=self.DB_PATH)
        
        check_obj = DbBuilder()
        check_obj.create_db()

        self.assertEqual(os.path.isfile(self.DB_PATH), True, "db file should have been made, expecting True")
        # the tearDown fixture will clean up the directory and file that get created

if __name__ == "__main__":
    unittest.main()
        
