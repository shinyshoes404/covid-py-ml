import unittest, mock, os, platform, json


# import the api flask app
from api import app as flask_api

class TestApiGetModels(unittest.TestCase):
    def setUp(self):
        self.api_app = flask_api
        self.api_app.testing = True
        self.client = self.api_app.test_client()

    # test if no db has been setup
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value = None)
    def test_no_db(self, mock_check_for_db):
      
        res = self.client.get('/ml/api/models')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b'Database is missing')

    # test if exception happened during query
    @mock.patch('api.ModelDataGetter.get_models', return_value=False)
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value = True)
    def test_query_exception(self, mock_check_for_db, mock_get_models):
      
        res = self.client.get('/ml/api/models')

        self.assertEqual(res.status_code, 500)
        self.assertEqual(res.data, b'Internal database error')

    
    # test if no data was found
    @mock.patch('api.ModelDataGetter.get_models', return_value=None)
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value = True)
    def test_no_data(self, mock_check_for_db, mock_get_models):
      
        res = self.client.get('/ml/api/models')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b'No data for prediction models') 

    # test if data was found
    @mock.patch('api.ModelDataGetter.get_models', return_value={"models" : [{"model_id":1, "model_date" : "09/03/2021", "model_score": 0.65, "model_poly_degree": 3, "model_mv_avg_days":7}]})
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value = True)
    def test_valid_data(self, mock_check_for_db, mock_get_models):
      
        res = self.client.get('/ml/api/models')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data), json.loads('{"models" : [{"model_id":1, "model_date" : "09/03/2021", "model_score": 0.65, "model_poly_degree": 3, "model_mv_avg_days":7}]}')) 


class TestApiGetPredictions(unittest.TestCase):
    def setUp(self):
        self.api_app = flask_api
        self.api_app.testing = True
        self.client = self.api_app.test_client()

    # test if no db has been setup
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value = None)
    def test_no_db(self, mock_check_for_db):
      
        res = self.client.get('/ml/api/predictions')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b'Database is missing')

    # test if exception happened during query
    @mock.patch('api.ModelDataGetter.get_predictions', return_value=False)
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value = True)
    def test_query_exception(self, mock_check_for_db, mock_get_models):
      
        res = self.client.get('/ml/api/predictions')

        self.assertEqual(res.status_code, 500)
        self.assertEqual(res.data, b'Internal database error')

    
    # test if no data was found
    @mock.patch('api.ModelDataGetter.get_predictions', return_value=None)
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value = True)
    def test_no_data(self, mock_check_for_db, mock_get_models):
      
        res = self.client.get('/ml/api/predictions')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b'No data for prediction models') 

    # test if data was found
    @mock.patch('api.ModelDataGetter.get_predictions', return_value={"predictions" : [{"model_id":1, "icu_16_prediction": 0.65, "predict_date" : "09/17/2021"}]})
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value = True)
    def test_valid_data(self, mock_check_for_db, mock_get_models):
      
        res = self.client.get('/ml/api/predictions')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data), json.loads('{"predictions" : [{"model_id":1, "icu_16_prediction": 0.65, "predict_date" : "09/17/2021"}]}')) 


class TestApiGetModelData(unittest.TestCase):
    def setUp(self):
        self.api_app = flask_api
        self.api_app.testing = True
        self.client = self.api_app.test_client()

    # test if a string is provided in the url
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value = None)
    def test_wrong_url(self, mock_check_for_db):
      
        res = self.client.get('/ml/api/model-data/string')

        self.assertEqual(res.status_code, 404)

    # test if no db has been setup
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value = None)
    def test_no_db(self, mock_check_for_db):
      
        res = self.client.get('/ml/api/model-data/1')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b'Database is missing')

    # test if exception happened during query
    @mock.patch('api.ModelDataGetter.get_model_data', return_value=False)
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value = True)
    def test_query_exception(self, mock_check_for_db, mock_get_models):
      
        res = self.client.get('/ml/api/model-data/1')

        self.assertEqual(res.status_code, 500)
        self.assertEqual(res.data, b'Internal database error')

    
    # test if no data was found
    @mock.patch('api.ModelDataGetter.get_model_data', return_value=None)
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value = True)
    def test_no_data(self, mock_check_for_db, mock_get_models):
      
        res = self.client.get('/ml/api/model-data/1')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b'No model data') 

    # test if data was found
    @mock.patch('api.ModelDataGetter.get_model_data', return_value={"observation_date" : "09/03/2021", "model_id" : 1, "casecount_mv_avg" : 150.5, "pos_test_mv_avg" : 0.145, "icu_top16_total_util" : 0.75})
    @mock.patch('db_ops.db_ops.DbChecker.check_for_db', return_value = True)
    def test_valid_data(self, mock_check_for_db, mock_get_models):
      
        res = self.client.get('/ml/api/model-data/1')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data), json.loads('{"observation_date" : "09/03/2021", "model_id" : 1, "casecount_mv_avg" : 150.5, "pos_test_mv_avg" : 0.145, "icu_top16_total_util" : 0.75}')) 

if __name__ == "__main__":
    unittest.main()