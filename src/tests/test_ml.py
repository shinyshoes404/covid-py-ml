from datetime import datetime, date
import unittest, mock, os, platform, sqlite3
from test_data import test_casecasecount_fulltest_json, test_testing_fulltest_json, test_icu_16_fulltest_json
from ml_config.ml_config import MlConfig

# import the db setup funtion for full sytem testing
from db_setup import build_db
# import function to test
from ml import ml_main


class TestMlMlMain(unittest.TestCase):
    
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
    

    # no case count data
    @mock.patch('ml.DataGetter')    
    def test_no_casecount_data(self, mock_getter):
        mock_getter.return_value.get_casecount_data.return_value = None
        with self.assertRaises(SystemExit) as cm:
            # run the main ml method
            ml_main()
        self.assertEqual(cm.exception.code, 1, "Should have exited, expecting 1")

    # no testing data
    @mock.patch('ml.DataGetter')
    def test_no_testing_data(self, mock_getter):
        mock_getter.return_value.get_casecount_data.return_value = True
        mock_getter.return_value.get_testing_data.return_value = None
        with self.assertRaises(SystemExit) as cm:
            # run the main ml method
            ml_main()
        self.assertEqual(cm.exception.code, 1, "Should have exited, expecting 1")
   
    # no icu data
    @mock.patch('ml.DataGetter')
    def test_no_icu_data(self,mock_getter):
        mock_getter.return_value.get_casecount_data.return_value = True
        mock_getter.return_value.get_testing_data.return_value = True
        mock_getter.return_value.get_icu_16_data.return_value = None

        with self.assertRaises(SystemExit) as cm:
            # run the main ml method
            ml_main()
        self.assertEqual(cm.exception.code, 1, "Should have exited, expecting 1")
   
    # no database
    @mock.patch('ml.PredictionChecker')
    @mock.patch('ml.DataGetter')
    def test_no_db(self, mock_getter, mock_pred_check):
        mock_getter.return_value.get_casecount_data.return_value = True
        mock_getter.return_value.get_testing_data.return_value = True
        mock_getter.return_value.get_icu_16_data.return_value = True

        mock_pred_check.return_value.get_max_prediction_date.return_value = False

        with self.assertRaises(SystemExit) as cm:
            # run the main ml method
            ml_main()
        self.assertEqual(cm.exception.code, 1, "Should have exited, expecting 1")
   
    # no prediction data returned in dataframe
    @mock.patch('ml.PredictionChecker')
    @mock.patch('ml.DataGetter')
    def test_no_pred_data(self, mock_getter, mock_pred_check):
        mock_getter.return_value.get_casecount_data.return_value = True
        mock_getter.return_value.get_testing_data.return_value = True
        mock_getter.return_value.get_icu_16_data.return_value = True

        mock_pred_check.return_value.get_max_prediction_date.return_value = datetime(2021, 9, 14, 0, 0, 0)
        mock_pred_check.return_value.get_prediction_data.return_value = None

        with self.assertRaises(SystemExit) as cm:
            # run the main ml method
            ml_main()
        self.assertEqual(cm.exception.code, 1, "Should have exited, expecting 1")

    # no independent variable data
    @mock.patch('ml.PredictionChecker')
    @mock.patch('ml.DataGetter')
    def test_no_indep_data(self, mock_getter, mock_pred_check):
        mock_getter.return_value.get_casecount_data.return_value = True
        mock_getter.return_value.get_testing_data.return_value = True
        mock_getter.return_value.get_icu_16_data.return_value = True

        mock_pred_check.return_value.get_max_prediction_date.return_value = datetime(2021, 9, 14, 0, 0, 0)
        mock_pred_check.return_value.get_prediction_data.return_value = False
        
        with self.assertRaises(SystemExit) as cm:
            # run the main ml method
            ml_main()
        self.assertEqual(cm.exception.code, 1, "Should have exited, expecting 1")

    # predict df and model data df returned
    @mock.patch('ml.PredictionChecker')
    @mock.patch('ml.DataGetter')
    def test_no_indep_data(self, mock_getter, mock_pred_check):
        mock_getter.return_value.get_casecount_data.return_value = True
        mock_getter.return_value.get_testing_data.return_value = True
        mock_getter.return_value.get_icu_16_data.return_value = True

        mock_pred_check.return_value.get_max_prediction_date.return_value = datetime(2021, 9, 14, 0, 0, 0)
        mock_pred_check.return_value.get_prediction_data.return_value = False
        
        with self.assertRaises(SystemExit) as cm:
            # run the main ml method
            ml_main()
        self.assertEqual(cm.exception.code, 1, "Should have exited, expecting 1")

    # define a function to mock the raw json returned by get_api_data
    def get_api_side_effect_func(url):
        if url == MlConfig.conf_urls.get('casecounts'):
            return ["json",test_casecasecount_fulltest_json]
        if url == MlConfig.conf_urls.get('testing'):
            return ["json", test_testing_fulltest_json]
        if url == MlConfig.conf_urls.get('icu-top16'):
            return ["json", test_icu_16_fulltest_json]
        else:
            return None

    # test full system by providing test json data
    @mock.patch('covid_ml.data_ops.date', mock.Mock(today=mock.Mock(return_value=date(2021, 9, 16))))
    @mock.patch('covid_ml.data_ops.DataGetter.get_api_data', side_effect=get_api_side_effect_func) # mock to prevent from calling
    @mock.patch('covid_ml.data_ops.DbConfig')
    @mock.patch('db_ops.db_ops.DbConfig')
    def test_intet_ml_full_system(self, mock_db_config, mock_db_config_2, mock_get_api):
        # db config info is called in two places, so we need to set the properties for both places
        # add the properties to our mock_db_config object
        type(mock_db_config).db_dir = mock.PropertyMock(return_value=self.TEMP_DB_DIR)
        type(mock_db_config).db_path = mock.PropertyMock(return_value=self.DB_PATH)

        # add the properties to our mock_db_config 2 object
        type(mock_db_config_2).db_dir = mock.PropertyMock(return_value=self.TEMP_DB_DIR)
        type(mock_db_config_2).db_path = mock.PropertyMock(return_value=self.DB_PATH)
        
        # setup the test database using the paths mocked above (method imported from db_setup.py)
        build_db()        
        
        # run the main ml function
        ml_main()

        # check the test database to see if we have the right number of records
        conn = sqlite3.connect(self.DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM models;")
        models_result = cur.fetchall()
        cur.execute("SELECT * FROM model_prediction;")
        model_pred_result = cur.fetchall()
        cur.execute("SELECT * FROM model_data;")
        model_data_result = cur.fetchall()
        cur.close()
        conn.close()

        results_list = [len(models_result), len(model_pred_result), len(model_data_result)]
        self.assertEqual(results_list, [1,1,2], "There should be one model, one prediction, and two model data points in the db; expecting [1,1,2]")

if __name__ == "__main__":
    unittest.main()