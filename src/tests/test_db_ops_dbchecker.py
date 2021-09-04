import unittest, mock, os, platform


# import class to test
from db_ops.db_ops import DbChecker

@mock.patch('db_ops.db_ops.DbConfig') # create mock DbConfig for entire clas
class TestDbChecker(unittest.TestCase):
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
    
    # no db dir present, test return value    
    @mock.patch('db_ops.db_ops.os.path.isdir', return_value=False)
    def test_no_dir_ret_val(self, mock_isdir, mock_db_config):
        type(mock_db_config).db_dir = mock.PropertyMock(return_value=self.TEMP_DB_DIR)
        type(mock_db_config).db_path = mock.PropertyMock(return_value=self.DB_PATH)
        check_obj = DbChecker()
        self.assertEqual(check_obj.db_exists, None, "No dir, expecting None")
    
    # no db dir present, test dir made   
    def test_no_dir_dir_made(self, mock_db_config):
        type(mock_db_config).db_dir = mock.PropertyMock(return_value=self.TEMP_DB_DIR)
        type(mock_db_config).db_path = mock.PropertyMock(return_value=self.DB_PATH)

        # for isdir: using context manager rather than decorator so that I can use a not mocked isdir in assertion
        with mock.patch('db_ops.db_ops.os.path.isdir', return_value=False) as mock_is_dir:
            check_obj = DbChecker()

        self.assertEqual(os.path.isdir(self.TEMP_DB_DIR), True, "No dir, expecting new dir made => True")
    
    # db dir is present, no db file is present
    @mock.patch('db_ops.db_ops.os.path.exists', return_value=False)
    @mock.patch('db_ops.db_ops.os.path.isdir', return_value=True)
    def test_yesdir_nodbfile(self, mock_isdir, mock_exists, mock_db_config):
        type(mock_db_config).db_dir = mock.PropertyMock(return_value=self.TEMP_DB_DIR)
        type(mock_db_config).db_path = mock.PropertyMock(return_value=self.DB_PATH)

        check_obj = DbChecker()
        self.assertEqual(check_obj.db_exists, None, "No db file, expecting None")

    # db dir is present, db file is present
    @mock.patch('db_ops.db_ops.os.path.exists', return_value=True)
    @mock.patch('db_ops.db_ops.os.path.isdir', return_value=True)
    def test_yesdir_yesdbfile(self, mock_isdir, mock_exists, mock_db_config):
        type(mock_db_config).db_dir = mock.PropertyMock(return_value=self.TEMP_DB_DIR)
        type(mock_db_config).db_path = mock.PropertyMock(return_value=self.DB_PATH)

        check_obj = DbChecker()
        self.assertEqual(check_obj.db_exists, True, "db file exists, expecting True")
