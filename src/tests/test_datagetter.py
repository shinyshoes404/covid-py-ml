import unittest, mock, pandas as pd, json, requests
from test_data import test_case_json, test_casecount_df, test_testdata_json, test_testing_df, test_icu_16_json, test_icu_df, test_casecount_built_df

# import the DataGetter class for testing
from covid_ml.data_ops import DataGetter


# testing the get_api_data() method
class TestDataGetterGetApiData(unittest.TestCase):

    # happy path - request returns json data with status code of 200
    def test_unit_successful_req_json_response(self):
        # mock the requests.get() method to return a status code of 200 and test_case_json
        with mock.patch('covid_ml.data_ops.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = test_case_json
            validation_obj = DataGetter()
            check_validation = validation_obj.get_api_data('https://random.test.url')
        
        self.assertEqual(check_validation[0], "json", "DataGetter.get_api_data: expecting 'json'")
    
    # simulate status code of 404
    def test_unit_404_response(self):
        # mock requests.get() method to return a status code of 404 and html content
        with mock.patch('covid_ml.data_ops.requests.get') as mock_get:
            mock_get.return_value.status_code = 404
            mock_get.return_value.content = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>"'
            validation_obj = DataGetter()
            check_validation = validation_obj.get_api_data('https://random.test.url')
        
        self.assertEqual(check_validation[0],"error","DataGetter.get_api_data: expecting 'error'")
    
    # simulate status code of 200, but .json() creates a JSONDecodeError (would happen if response content was html)
    def test_unit_200_no_json(self):
        # mock requests.get() method to return a status code of 404 and html content
        with mock.patch('covid_ml.data_ops.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.side_effect = json.decoder.JSONDecodeError("No json","test doc", 1)
            validation_obj = DataGetter()
            check_validation = validation_obj.get_api_data('https://random.test.url')
        
        self.assertEqual(check_validation[0],"error","DataGetter.get_api_data: expecting 'error'")

    # simulate connection problem
    def test_unit_bad_connection(self):
        # mock requests.get() method to return a status code of 404 and html content
        with mock.patch('covid_ml.data_ops.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError
            validation_obj = DataGetter()
            check_validation = validation_obj.get_api_data('https://random.test.url')
        
        self.assertEqual(check_validation[0],"error","DataGetter.get_api_data: expecting 'error'")
    
    

# testing the build_df() method
class TestDataGetterBuildDf(unittest.TestCase):

    # verify with test data
    def test_unit_valid_data(self):
        validation_obj = DataGetter()
        check_validation = validation_obj.build_df(test_case_json, "casecountdate")
        self.assertEqual(len(check_validation), 2, "DataGetter.build_df: expecting 2")
    


# testing the get_casecount_data() method
class TestDataGetterGetCasecountData(unittest.TestCase):

    # Are we getting the right size data frame (only keeping the columns we want)
    @mock.patch('covid_ml.data_ops.DataGetter.get_api_data',return_value=["json",test_case_json]) # mock the method to return the the test json data
    @mock.patch('covid_ml.data_ops.DataGetter.build_df',return_value=test_casecount_df) # mock build_df() method to return the test pandas data frame
    def test_unit_remove_columns(self, mock_build_df, mock_get_api_data):
        validation_object = DataGetter()
        validation_object.get_casecount_data()
        self.assertEqual(len(validation_object.casecount_df.columns), 2, "DataGetter.get_casecount_data: Expecting 2")

    # verify that the final data frame is sorted correctly while actually calling build_df() method
    @mock.patch('covid_ml.data_ops.DataGetter.get_api_data',return_value=["json",test_case_json]) # mock the method to return the the test json data
    def test_integ_correct_sort(self, mock_requests_get):
        validation_object = DataGetter()
        validation_object.get_casecount_data()
        # expecting 01/02/2021 to be in the second row (0 index) in the date column
        self.assertEqual(validation_object.casecount_df.iloc[1]['casecountdate'], pd.Timestamp(2021, 1, 2), "DataGetter.get_casecount_data: Expecting '01/02/2021'")
    
    # are we catching an error response from get_api_data() 
    @mock.patch('covid_ml.data_ops.DataGetter.get_api_data',return_value=["error","connection error"]) # mock get_api_data() to return an error repsonse
    def test_unit_get_api_data_error(self, mock_get_api_data):
        validation_object = DataGetter()
        check_validation = validation_object.get_casecount_data()
        self.assertEqual(check_validation, None, "DataGetter.get_casecount_data: Expecting None")

# testing the get_testing_data() method
class TestDataGetterGetTestingData(unittest.TestCase):

    # Are we getting the right size data frame (only keeping the columns we want)
    @mock.patch('covid_ml.data_ops.DataGetter.get_api_data',return_value=["json",test_testdata_json]) # mock the method to return the the test json data
    @mock.patch('covid_ml.data_ops.DataGetter.build_df',return_value=test_testing_df) # mock build_df() method to return the test pandas data frame
    def test_unit_remove_columns(self, mock_build_df, mock_get_api_data):
        validation_object = DataGetter()
        validation_object.get_testing_data()
        self.assertEqual(len(validation_object.testing_df.columns), 2, "DataGetter.get_testing_data: Expecting 2")

    # verify that the final data frame is sorted correctly while actually calling build_df() method
    @mock.patch('covid_ml.data_ops.DataGetter.get_api_data',return_value=["json",test_testdata_json]) # mock the method to return the the test json data
    def test_integ_correct_sort(self, mock_requests_get):
        validation_object = DataGetter()
        validation_object.get_testing_data()
        # expecting 01/02/2021 to be in the second row (0 index) in the date column
        self.assertEqual(validation_object.testing_df.iloc[1]['testdate'], pd.Timestamp(2021, 1, 2), "DataGetter.get_testing_data: Expecting '01/02/2021'")
    
    # are we catching an error response from get_api_data() 
    @mock.patch('covid_ml.data_ops.DataGetter.get_api_data',return_value=["error","connection error"]) # mock get_api_data() to return an error repsonse
    def test_unit_get_api_data_error(self, mock_get_api_data):
        validation_object = DataGetter()
        check_validation = validation_object.get_testing_data()
        self.assertEqual(check_validation, None, "DataGetter.get_testing_data: Expecting None")


    
# testing the get_icu_16_data() method
class TestDataGetterGetIcu16Data(unittest.TestCase):

    # Are we getting the right size data frame (only keeping the columns we want)
    @mock.patch('covid_ml.data_ops.DataGetter.get_api_data',return_value=["json",test_icu_16_json]) # mock the method to return the the test json data
    @mock.patch('covid_ml.data_ops.DataGetter.build_df',return_value=test_icu_df) # mock build_df() method to return the test pandas data frame
    def test_unit_remove_columns(self, mock_build_df, mock_get_api_data):
        validation_object = DataGetter()
        validation_object.get_icu_16_data()
        self.assertEqual(len(validation_object.icu_16_df.columns), 2, "DataGetter.get_icu_16_data: Expecting 2")

    # verify that the final data frame is sorted correctly while actually calling build_df() method
    @mock.patch('covid_ml.data_ops.DataGetter.get_api_data',return_value=["json",test_icu_16_json]) # mock the method to return the the test json data
    def test_integ_correct_sort(self, mock_requests_get):
        validation_object = DataGetter()
        validation_object.get_icu_16_data()
        # expecting 01/02/2021 to be in the second row (0 index) in the date column
        self.assertEqual(validation_object.icu_16_df.iloc[1]['offset_date'], pd.Timestamp(2020, 12, 14), "DataGetter.get_icu_16_data: Expecting '12/14/2020'")
    
    # are we catching an error response from get_api_data() 
    @mock.patch('covid_ml.data_ops.DataGetter.get_api_data',return_value=["error","connection error"]) # mock get_api_data() to return an error repsonse
    def test_unit_get_api_data_error(self, mock_get_api_data):
        validation_object = DataGetter()
        check_validation = validation_object.get_icu_16_data()
        self.assertEqual(check_validation, None, "DataGetter.get_icu_16_data: Expecting None")

# testing the combine_model_df() method
# class TestDataGetterCombineModelDf(unittest.TestCase):



if __name__ == "__main__":
        unittest.main()