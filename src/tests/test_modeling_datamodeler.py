import unittest, mock


# import class to test
from covid_ml.modeling import DataModeler

# testing the DataModeler class
class TestDataModeler(unittest.TestCase):
    
    @mock.patch('covid_ml.modeling.MlConfig')
    def test_train_n_1(self, mock_n):
        type(mock_n).poly_degree = mock.PropertyMock(return_value = 1)
        x = [[0],[1],[2],[3],[4]]
        y = [0,1,2,3,4]

        check_obj = DataModeler()
        check_obj.model_train(x,y)

        self.assertEqual(check_obj.model_score, 1, "Linear, expecting 1.0")

    @mock.patch('covid_ml.modeling.MlConfig')
    def test_train_n_2(self, mock_n):
        type(mock_n).poly_degree = mock.PropertyMock(return_value = 2)
        x = [[-2],[-1],[0],[1],[2]]
        y = [4, 1, 0, 1,4]

        check_obj = DataModeler()
        check_obj.model_train(x,y)

        self.assertEqual(check_obj.model_score, 1, "quadratic, expecting 1.0")
    
    @mock.patch('covid_ml.modeling.MlConfig')
    def test_predict_n_1(self, mock_n):
        type(mock_n).poly_degree = mock.PropertyMock(return_value = 1)
        x = [[0],[1],[2],[3],[4]]
        y = [0,1,2,3,4]

        check_obj = DataModeler()
        check_obj.model_train(x,y)
        check_val = check_obj.predict([[5]])
        
        self.assertEqual(check_val[0], 5, "Linear, expecting 5")

    @mock.patch('covid_ml.modeling.MlConfig')
    def test_train_n_2(self, mock_n):
        type(mock_n).poly_degree = mock.PropertyMock(return_value = 2)
        x = [[-2],[-1],[0],[1],[2]]
        y = [4, 1, 0, 1,4]

        check_obj = DataModeler()
        check_obj.model_train(x,y)
        check_val = check_obj.predict([[3]])

        self.assertEqual(round(check_val[0],2), 9.00, "quadratic, expecting 9.00")
    

