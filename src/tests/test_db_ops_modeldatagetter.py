import unittest, mock

from test_data import test_model_data_df, test_predict_data_df, test_predictions

# import the class we want to test
from db_ops.db_ops import ModelDataGetter

class TestModelDataGetterGetModels(unittest.TestCase):
    # db exists, exception raised
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value=True)
    @mock.patch('db_ops.db_ops.sqlite3')
    def test_get_models_exception(self, mock_sql, mock_check_for_db):
        mock_sql.connect().cursor().fetchall.side_effect = Exception
        check_obj = ModelDataGetter()
        check_val = check_obj.get_models()

        self.assertEqual(check_val, False, "An exception occurred during query, expecting False")
        
        
    # db exists, no data returned list with None
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value=True)
    @mock.patch('db_ops.db_ops.sqlite3')
    def test_get_models_none(self, mock_sql, mock_check_for_db):
        mock_sql.connect().cursor().fetchall.return_value = [(None,)]
        check_obj = ModelDataGetter()
        check_val = check_obj.get_models()

        self.assertEqual(check_val, None, "No records retrieved - list with None tuple, expecting None")
    
    # db exists, no data returned with empty list
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value=True)
    @mock.patch('db_ops.db_ops.sqlite3')
    def test_get_models_empty_list(self, mock_sql, mock_check_for_db):
        mock_sql.connect().cursor().fetchall.return_value = []
        check_obj = ModelDataGetter()
        check_val = check_obj.get_models()

        self.assertEqual(check_val, None, "No records retrieved - empty list, expecting None")


    # db exists, return row of data
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value=True)
    @mock.patch('db_ops.db_ops.sqlite3')
    def test_get_models_one_row(self, mock_sql, mock_check_for_db):
        mock_sql.connect().cursor().fetchall.return_value = [(1, '2021-08-29 00:00:00', 0.65, 3, 7)]
        check_obj = ModelDataGetter()
        check_val = check_obj.get_models()
        expected_return_val = {'models': [{'model_id': 1, 'model_date': '2021-08-29 00:00:00', 'model_score':0.65, 'model_poly_degree': 3, 'model_mv_avg_days' : 7}]}
        self.assertEqual(check_val, expected_return_val, "Expecting specific dictionary to return")



class TestModelDataGetterGetPredictions(unittest.TestCase):
    # db exists, exception raised
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value=True)
    @mock.patch('db_ops.db_ops.sqlite3')
    def test_get_predictions_exception(self, mock_sql, mock_check_for_db):
        mock_sql.connect().cursor().fetchall.side_effect = Exception
        check_obj = ModelDataGetter()
        check_val = check_obj.get_predictions()

        self.assertEqual(check_val, False, "An exception occurred during query, expecting False")
        
        
    # db exists, no data returned list with None
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value=True)
    @mock.patch('db_ops.db_ops.sqlite3')
    def test_get_predictions_none(self, mock_sql, mock_check_for_db):
        mock_sql.connect().cursor().fetchall.return_value = [(None,)]
        check_obj = ModelDataGetter()
        check_val = check_obj.get_predictions()

        self.assertEqual(check_val, None, "No records retrieved - list with None tuple, expecting None")
    
    # db exists, no data returned with empty list
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value=True)
    @mock.patch('db_ops.db_ops.sqlite3')
    def test_get_predictions_empty_list(self, mock_sql, mock_check_for_db):
        mock_sql.connect().cursor().fetchall.return_value = []
        check_obj = ModelDataGetter()
        check_val = check_obj.get_predictions()

        self.assertEqual(check_val, None, "No records retrieved - empty list, expecting None")


    # db exists, return row of data
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value=True)
    @mock.patch('db_ops.db_ops.sqlite3')
    def test_get_predictions_one_row(self, mock_sql, mock_check_for_db):
        mock_sql.connect().cursor().fetchall.return_value = [(1, 0.75, '2021-09-13 00:00:00')]
        check_obj = ModelDataGetter()
        check_val = check_obj.get_predictions()
        expected_return_val = {'predictions': [{'model_id': 1, 'predict_date': '2021-09-13 00:00:00', 'icu_16_prediction':0.75}]}
        self.assertEqual(check_val, expected_return_val, "Expecting specific dictionary to return")


class TestModelDataGetterGetModelData(unittest.TestCase):
    # db exists, exception raised
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value=True)
    @mock.patch('db_ops.db_ops.sqlite3')
    def test_get_model_data_exception(self, mock_sql, mock_check_for_db):
        mock_sql.connect().cursor().fetchall.side_effect = Exception
        check_obj = ModelDataGetter()
        check_val = check_obj.get_model_data(1)

        self.assertEqual(check_val, False, "An exception occurred during query, expecting False")
        
        
    # db exists, no data returned list with None
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value=True)
    @mock.patch('db_ops.db_ops.sqlite3')
    def test_get_model_data_none(self, mock_sql, mock_check_for_db):
        mock_sql.connect().cursor().fetchall.return_value = [(None,)]
        check_obj = ModelDataGetter()
        check_val = check_obj.get_model_data(1)

        self.assertEqual(check_val, None, "No records retrieved - list with None tuple, expecting None")
    
    # db exists, no data returned with empty list
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value=True)
    @mock.patch('db_ops.db_ops.sqlite3')
    def test_get_model_data_empty_list(self, mock_sql, mock_check_for_db):
        mock_sql.connect().cursor().fetchall.return_value = []
        check_obj = ModelDataGetter()
        check_val = check_obj.get_model_data(1)

        self.assertEqual(check_val, None, "No records retrieved - empty list, expecting None")


    # db exists, return row of data
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value=True)
    @mock.patch('db_ops.db_ops.sqlite3')
    def test_get_model_data_one_row(self, mock_sql, mock_check_for_db):
        mock_sql.connect().cursor().fetchall.return_value = [('2021-08-29 00:00:00',1, 155.0, 0.145, 0.85)]
        check_obj = ModelDataGetter()
        check_val = check_obj.get_model_data(1)
        expected_return_val = {'model_data': [{'observation_date':'2021-08-29 00:00:00', 'model_id': 1, 'casecount_mv_avg' : 155.0, 'pos_test_mv_avg' : 0.145, 'icu_top16_total_util':0.85}]}
        self.assertEqual(check_val, expected_return_val, "Expecting specific dictionary to return")