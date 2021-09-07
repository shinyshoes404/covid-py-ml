import unittest, mock, pandas as pd, json, requests
from test_data import test_case_json, test_casecount_df, test_testdata_json, test_testing_df, test_icu_16_json, test_icu_df
from test_data import test_casecasecount_fulltest_json, test_casecount_fulltest_df, test_testing_fulltest_json, test_testing_fulltest_df
from test_data import test_icu_16_fulltest_json, test_icu_16_fulltest_df, test_independent_df, test_model_data_df

# import the DataGetter class for testing
from covid_ml.data_ops import DataGetter

# make sure that any warnings trigger exceptions
# this was specifically put in place to make sure that strings in pandas dataframes
# are not inferred to be datetime when using the df1.equals(df2) approach to comparing dataframes
import warnings
warnings.filterwarnings('error')


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
    
    # integration test - does the input json match the expected output dataframe
    def test_integ_json_to_df_equal(self):
        # mock the requests.get() method to return a status code of 200 and test_case_json
        with mock.patch('covid_ml.data_ops.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = test_casecasecount_fulltest_json
            validation_obj = DataGetter()
            validation_obj.get_casecount_data()
        
        check_validation = validation_obj.casecount_df.equals(test_casecount_fulltest_df)
        self.assertEqual(check_validation, True, "DataGetter.get_casecount_data: expecting True")

    # integration test - does get_casecount_data() return True indicating success
    def test_integ_json_to_df_true(self):
        # mock the requests.get() method to return a status code of 200 and test_case_json
        with mock.patch('covid_ml.data_ops.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = test_casecasecount_fulltest_json
            validation_obj = DataGetter()
            check_validation = validation_obj.get_casecount_data()
        
        self.assertEqual(check_validation, True, "DataGetter.get_casecount_data: expecting True")
    
    # integration test - does get_casecount_data() return none indicating something went wrong
    def test_integ_json_to_df_none(self):
        # mock the requests.get() method to return a status code of 404
        with mock.patch('covid_ml.data_ops.requests.get') as mock_get:
            mock_get.return_value.status_code = 404
            mock_get.return_value.json.return_value = test_casecasecount_fulltest_json
            validation_obj = DataGetter()
            check_validation = validation_obj.get_casecount_data()
        
        self.assertEqual(check_validation, None, "DataGetter.get_casecount_data: expecting True")

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

    # integration test - does the input json match the expected output dataframe
    def test_integ_json_to_df_equal(self):
        # mock the requests.get() method to return a status code of 200 and test_testing_fulltest_json
        with mock.patch('covid_ml.data_ops.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = test_testing_fulltest_json
            validation_obj = DataGetter()
            validation_obj.get_testing_data()
        
        check_validation = validation_obj.testing_df.equals(test_testing_fulltest_df)
        self.assertEqual(check_validation, True, "DataGetter.get_testing_data: expecting True")

    # integration test - does get_testing_data() return True indicating success
    def test_integ_json_to_df_true(self):
        # mock the requests.get() method to return a status code of 200 and test_testing_fulltest_json
        with mock.patch('covid_ml.data_ops.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = test_testing_fulltest_json
            validation_obj = DataGetter()
            check_validation = validation_obj.get_testing_data()
        
        self.assertEqual(check_validation, True, "DataGetter.get_testing_data: expecting True")
    
    # integration test - does get_testing_data() return none indicating something went wrong
    def test_integ_json_to_df_none(self):
        # mock the requests.get() method to return a status code of 404
        with mock.patch('covid_ml.data_ops.requests.get') as mock_get:
            mock_get.return_value.status_code = 404
            mock_get.return_value.json.return_value = test_testing_fulltest_json
            validation_obj = DataGetter()
            check_validation = validation_obj.get_casecount_data()
        
        self.assertEqual(check_validation, None, "DataGetter.get_testing_data: expecting True")
    
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
        self.assertEqual(validation_object.icu_16_df.iloc[1]['offset_date'], pd.Timestamp(2021, 4, 13), "DataGetter.get_icu_16_data: Expecting '04/13/2021'")
    
    # are we catching an error response from get_api_data() 
    @mock.patch('covid_ml.data_ops.DataGetter.get_api_data',return_value=["error","connection error"]) # mock get_api_data() to return an error repsonse
    def test_unit_get_api_data_error(self, mock_get_api_data):
        validation_object = DataGetter()
        check_validation = validation_object.get_icu_16_data()
        self.assertEqual(check_validation, None, "DataGetter.get_icu_16_data: Expecting None")

    # integration test - does the input json match the expected output dataframe
    def test_integ_json_to_df_equal(self):
        # mock the requests.get() method to return a status code of 200 and test_icu_16_fulltest_json
        with mock.patch('covid_ml.data_ops.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = test_icu_16_fulltest_json
            validation_obj = DataGetter()
            validation_obj.get_icu_16_data()

        check_validation = validation_obj.icu_16_df.equals(test_icu_16_fulltest_df)
        self.assertEqual(check_validation, True, "DataGetter.get_icu_16_data: expecting True")

    # integration test - does get_icu_16_data() return True indicating success
    def test_integ_json_to_df_true(self):
        # mock the requests.get() method to return a status code of 200 and test_icu_16_fulltest_json
        with mock.patch('covid_ml.data_ops.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = test_icu_16_fulltest_json
            validation_obj = DataGetter()
            check_validation = validation_obj.get_icu_16_data()
        
        self.assertEqual(check_validation, True, "DataGetter.get_icu_16_data: expecting True")
    
    # integration test - does get_icu_16_data() return none indicating something went wrong
    def test_integ_json_to_df_none(self):
        # mock the requests.get() method to return a status code of 404 and test_icu_16_fulltest_json
        with mock.patch('covid_ml.data_ops.requests.get') as mock_get:
            mock_get.return_value.status_code = 404
            mock_get.return_value.json.return_value = test_icu_16_fulltest_json
            validation_obj = DataGetter()
            check_validation = validation_obj.get_icu_16_data()
        
        self.assertEqual(check_validation, None, "DataGetter.get_icu_16_data: expecting True")


# testing the combine_model_df() and smooth_df() methods
class TestDataGetterCombineModelDf(unittest.TestCase):

    # test that we get the model_data_df dataframe we expect based on the test dataframes provided
    def test_integ_model_data_df_equal(self):
        validation_obj = DataGetter()
        validation_obj.icu_16_df = test_icu_16_fulltest_df
        validation_obj.casecount_df = test_casecount_fulltest_df
        validation_obj.testing_df = test_testing_fulltest_df
        validation_obj.combine_model_df()
        check_validation = validation_obj.model_data_df.equals(test_model_data_df)

        self.assertEqual(check_validation, True, "DataGetter.combine_model_df: expecting True")

    # test that we get the independent_df dataframe we expect based on the test dataframes provided
    def test_integ_model_data_df_equal(self):
        validation_obj = DataGetter()
        validation_obj.icu_16_df = test_icu_16_fulltest_df
        validation_obj.casecount_df = test_casecount_fulltest_df
        validation_obj.testing_df = test_testing_fulltest_df
        validation_obj.combine_model_df()
        check_validation = validation_obj.independent_df.equals(test_independent_df)

        self.assertEqual(check_validation, True, "DataGetter.combine_model_df: expecting True")



if __name__ == "__main__":
    unittest.main()