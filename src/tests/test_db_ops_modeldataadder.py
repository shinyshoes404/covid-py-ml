import unittest, mock, os, platform, sqlite3
from sqlite3 import IntegrityError
from datetime import datetime

from pandas.io import sql

from test_data import test_model_data_df, test_predict_data_df, test_predictions


# import class to test
from db_ops.db_ops import ModelDataAdder, DbBuilder

@mock.patch('db_ops.db_ops.DbConfig') # create mock DbConfig for entire class
class TestModelDataAdderAddData(unittest.TestCase):
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


    def test_integ_verify_models_tbl(self, mock_db_config):
        # add the properties to our mock_db_config object
        type(mock_db_config).db_dir = mock.PropertyMock(return_value=self.TEMP_DB_DIR)
        type(mock_db_config).db_path = mock.PropertyMock(return_value=self.DB_PATH)

        # create the database to use for testing
        db_build = DbBuilder()
        db_build.create_db()

        # intantiate the ModelDataAdder class to create our check object
        check_obj = ModelDataAdder(model_date=datetime(2021, 9, 3, 0, 0, 0),
                                    model_score=0.65,
                                    model_data=test_model_data_df[['date','casecount-mv-avg','pos-test-mv-avg', 'icu-top16-hosp-total-util']],
                                    icu_predictions=test_predictions,
                                    icu_prediction_dates=test_predict_data_df['predict-date'])
        # add data to test db
        check_obj.add_data()
        # assert that db exists before we try to check for data, if there was no db file, creating
        # the connection in the next step would make one
        self.assertEqual(os.path.isfile(self.DB_PATH), True, "A test db file should already exist, expecting True")

        # make sure our data is in the database
        sql_check = "SELECT * FROM models;"
        conn = sqlite3.connect(self.DB_PATH)
        cur = conn.cursor()
        cur.execute(sql_check)
        check_results = cur.fetchall()
        cur.close()
        conn.close()

        # verify that we have one row of data
        self.assertEqual(len(check_results), 1,"Should be one model stored in db, expecting 1")

    def test_integ_verify_model_prediction_tbl(self, mock_db_config):
        # add the properties to our mock_db_config object
        type(mock_db_config).db_dir = mock.PropertyMock(return_value=self.TEMP_DB_DIR)
        type(mock_db_config).db_path = mock.PropertyMock(return_value=self.DB_PATH)

        # create the database to use for testing
        db_build = DbBuilder()
        db_build.create_db()

        # intantiate the ModelDataAdder class to create our check object
        check_obj = ModelDataAdder(model_date=datetime(2021, 9, 3, 0, 0, 0),
                                    model_score=0.65,
                                    model_data=test_model_data_df[['date','casecount-mv-avg','pos-test-mv-avg', 'icu-top16-hosp-total-util']],
                                    icu_predictions=test_predictions,
                                    icu_prediction_dates=test_predict_data_df['predict-date'])
        # add data to test db
        check_obj.add_data()
        # assert that db exists before we try to check for data, if there was no db file, creating
        # the connection in the next step would make one
        self.assertEqual(os.path.isfile(self.DB_PATH), True, "A test db file should already exist, expecting True")

        # make sure our data is in the database
        sql_check = "SELECT * FROM model_prediction;"
        conn = sqlite3.connect(self.DB_PATH)
        cur = conn.cursor()
        cur.execute(sql_check)
        check_results = cur.fetchall()
        cur.close()
        conn.close()

        # verify that we have one row of data
        self.assertEqual(len(check_results), 2,"Should be two predictions stored in db, expecting 2")


    def test_integ_verify_model_data_tbl(self, mock_db_config):
        # add the properties to our mock_db_config object
        type(mock_db_config).db_dir = mock.PropertyMock(return_value=self.TEMP_DB_DIR)
        type(mock_db_config).db_path = mock.PropertyMock(return_value=self.DB_PATH)

        # create the database to use for testing
        db_build = DbBuilder()
        db_build.create_db()

        # intantiate the ModelDataAdder class to create our check object
        check_obj = ModelDataAdder(model_date=datetime(2021, 9, 3, 0, 0, 0),
                                    model_score=0.65,
                                    model_data=test_model_data_df[['date','casecount-mv-avg','pos-test-mv-avg', 'icu-top16-hosp-total-util']],
                                    icu_predictions=test_predictions,
                                    icu_prediction_dates=test_predict_data_df['predict-date'])
        # add data to test db
        check_obj.add_data()
        # assert that db exists before we try to check for data, if there was no db file, creating
        # the connection in the next step would make one
        self.assertEqual(os.path.isfile(self.DB_PATH), True, "A test db file should already exist, expecting True")

        # make sure our data is in the database
        sql_check = "SELECT * FROM model_data;"
        conn = sqlite3.connect(self.DB_PATH)
        cur = conn.cursor()
        cur.execute(sql_check)
        check_results = cur.fetchall()
        cur.close()
        conn.close()

        # verify that we have one row of data
        self.assertEqual(len(check_results), 2,"Should be two model data points in db, expecting 2")


    def test_integ_verify_except_rollback(self, mock_db_config):
        # add the properties to our mock_db_config object
        type(mock_db_config).db_dir = mock.PropertyMock(return_value=self.TEMP_DB_DIR)
        type(mock_db_config).db_path = mock.PropertyMock(return_value=self.DB_PATH)

        # create the database to use for testing
        db_build = DbBuilder()
        db_build.create_db()

        # intantiate the ModelDataAdder class to create our check object
        check_obj = ModelDataAdder(model_date=datetime(2021, 9, 3, 0, 0, 0),
                                    model_score=None, # will cause an integrity error
                                    model_data=test_model_data_df[['date','casecount-mv-avg','pos-test-mv-avg', 'icu-top16-hosp-total-util']],
                                    icu_predictions=test_predictions,
                                    icu_prediction_dates=test_predict_data_df['predict-date'])

        check_obj.add_data()

        self.assertEqual(check_obj.rollback, True, "Should cause integrity error in sqlite, expecting True")

       