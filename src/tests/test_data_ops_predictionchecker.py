import unittest, mock
from datetime import datetime, date

# import test data
from test_data import test_independent_df

# import PredictionChecker class for testing
from covid_ml.data_ops import PredictionChecker


class TestPredictionCheckerGetMaxPredictionData(unittest.TestCase):

    # database file doesn't exist
    @mock.patch("covid_ml.data_ops.DbChecker.check_for_db", return_value=None)
    def test_no_db(self, mock_db_checker):
        check_obj = PredictionChecker()
        check_val = check_obj.get_max_prediction_date()

        self.assertEqual(check_val, False, "No DB file, expecting False")

    # no predictions have been made -> max predict date returns (None,)
    @mock.patch('covid_ml.data_ops.sqlite3.connect')
    @mock.patch("covid_ml.data_ops.DbChecker.check_for_db", return_value=True)
    def test_no_data_none(self, mock_db_checker, mock_sql_conn):
        mock_sql_conn.return_value.cursor().fetchone.return_value = (None,)
        check_obj = PredictionChecker()
        check_val = check_obj.get_max_prediction_date()

        self.assertEqual(check_val, None, "No prediction data in DB, returned (None,), expecting None")
    
    # no predictions have been made -> max predict date returns []
    @mock.patch('covid_ml.data_ops.sqlite3.connect')
    @mock.patch("covid_ml.data_ops.DbChecker.check_for_db", return_value=True)
    def test_no_data_empty_list(self,mock_db_checker, mocksql_conn):
        mocksql_conn.return_value.cursor().fetchone.return_value = []
        check_obj = PredictionChecker()
        check_val = check_obj.get_max_prediction_date()

        self.assertEqual(check_val, None, "No prediction data in DB, returned [], expecting None")

    # max prediction date of '2021-01-05 00:00:00'
    @mock.patch('covid_ml.data_ops.sqlite3.connect')
    @mock.patch("covid_ml.data_ops.DbChecker.check_for_db", return_value=True)
    def test_max_pred_found(self, mock_db_checker, mocksql_conn):
        mocksql_conn.return_value.cursor().fetchone.return_value = ('2021-01-05 00:00:00',)
        check_obj = PredictionChecker()
        check_val = check_obj.get_max_prediction_date()

        self.assertEqual(check_val, datetime.strptime('2021-01-05 00:00:00', "%Y-%m-%d %H:%M:%S"), "2021-01-05 returned from DB, expecting 2021-01-05")


class TestPredictionCheckerGetPredictionData(unittest.TestCase):

    # no current predictions, mock today() so that 2 rows are returned in the final dataframe
    @mock.patch('covid_ml.data_ops.date', mock.Mock(today=mock.Mock(return_value=date(2021, 9, 3))))
    def test_no_predictions(self):
        check_obj = PredictionChecker()
        check_val = check_obj.get_prediction_data(None, test_independent_df)

        self.assertEqual(check_val.shape[0],2,"expecting 2 rows in resulting dataframe")
    
    # no current predictions, mock today() so that independent data is too old
    @mock.patch('covid_ml.data_ops.date', mock.Mock(today=mock.Mock(return_value=date(2021, 9, 22))))
    def test_no_predictions_old_independent(self):
        check_obj = PredictionChecker()
        check_val = check_obj.get_prediction_data(None, test_independent_df)

        self.assertEqual(check_val, False,"no independent data recent enough, excpecting False")

    # max current prediction 2021-09-16 (13 days past the mocked current date)
    @mock.patch('covid_ml.data_ops.date', mock.Mock(today=mock.Mock(return_value=date(2021, 9, 3))))
    def test_no_predictions_one_row(self):
        check_obj = PredictionChecker()
        check_val = check_obj.get_prediction_data(datetime(2021, 9, 16, 0, 0, 0), test_independent_df)

        self.assertEqual(check_val.shape[0],1,"expecting 1 rows in resulting dataframe")

if __name__ == "__main__":
    unittest.main()