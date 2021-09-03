import unittest, mock


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
    def test_no_data_none_2(self,mock_db_checker, mocksql_conn):
        mocksql_conn.return_value.cursor().fetchone.return_value = []
        check_obj = PredictionChecker()
        check_val = check_obj.get_max_prediction_date()

        self.assertEqual(check_val, None, "No prediction data in DB, returned [], expecting None")

if __name__ == "__main__":
    unittest.main()