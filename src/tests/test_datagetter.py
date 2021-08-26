import unittest, mock, pandas as pd, json, requests

# import the DataGetter class for testing
from covid_ml.data_ops import DataGetter

# json for tests
test_case_json = { "01/01/2021" : {"casecount" : 1956, "casecountdate":"01/01/2021", "geoarea":"State of Utah", "retrieveddate" : "03/13/2021 11:00 AM"},
               "01/02/2021" : {"casecount" : 1845, "casecountdate":"01/02/2021", "geoarea":"State of Utah", "retrieveddate" : "02/03/2021 02:00 PM"} }

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


    # pandas data frame for tests
    test_df = pd.DataFrame([[1956, "01/01/2021", "State of Utah", "03/13/2021 11:00 AM"], [1845, "01/02/2021", "State of Utah", "02/03/2021 02:00 PM"]], columns = ['casecount','casecountdate','geoarea', 'retrieveddate'])
    test_df['casecountdate'] = pd.to_datetime(test_df['casecountdate'])
    test_df = test_df.sort_values('casecountdate').reset_index(drop=True)


    # Are we getting the right size data frame (only keeping the columns we want)
    @mock.patch('covid_ml.data_ops.DataGetter.get_api_data',return_value=["json",test_case_json]) # mock the method to return the the test json data
    @mock.patch('covid_ml.data_ops.DataGetter.build_df',return_value=test_df) # mock build_df() method to return the test pandas data frame
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
    # json to use for testing
    test_testdata_json = { "01/01/2021" : {"geoarea":"State of Utah", "peoplepositive": 1888, "peopletested" : 5967, "retrieveddate" :	"08/04/2021 02:01 PM", "testdate" :	"01/01/2021"},
                            "01/02/2021" : {"geoarea" :	"State of Utah", "peoplepositive" :1906, "peopletested":5627, "retrieveddate": "07/30/2021 02:01 PM", "testdate" :	"01/02/2021"}}

    # pandas data frame for tests
    test_df = pd.DataFrame([["State of Utah", 1888, 5967, "08/04/2021 02:01 PM", "01/01/2021"],
            ["State of Utah", 1906, 5627, "07/30/2021 02:01 PM", "01/02/2021"]],
            columns = ['geoarea','peoplepositive','peopletested', 'retrieveddate','testdate'])
    test_df['testdate'] = pd.to_datetime(test_df['testdate'])
    test_df = test_df.sort_values('testdate').reset_index(drop=True)


    # Are we getting the right size data frame (only keeping the columns we want)
    @mock.patch('covid_ml.data_ops.DataGetter.get_api_data',return_value=["json",test_testdata_json]) # mock the method to return the the test json data
    @mock.patch('covid_ml.data_ops.DataGetter.build_df',return_value=test_df) # mock build_df() method to return the test pandas data frame
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
    # json to use for testing
    test_icu_16_json = { "01/01/2021" : {"date":"01/01/2021", "icu-top16-hosp-covid-util":0.32,"icu-top16-hosp-total-util":	0.85,"retrieveddate":"01/03/2021 01:00 PM"},
                        "01/02/2021" : {"date":	"01/02/2021","icu-top16-hosp-covid-util": 0.33, "icu-top16-hosp-total-util":0.86, "retrieveddate":"01/03/2021 01:00 PM"}}

    # pandas data frame for tests
    test_df = pd.DataFrame([["01/01/2021", 0.32, 0.85,"01/03/2021 01:00 PM" ],
            ["01/02/2021",0.33,0.86,"01/03/2021 01:00 PM"]],
            columns = ['date','icu-top16-hosp-covid-util','icu-top16-hosp-total-util', 'retrieveddate'])
    test_df['date'] = pd.to_datetime(test_df['date'])
    test_df = test_df.sort_values('date').reset_index(drop=True)


    # Are we getting the right size data frame (only keeping the columns we want)
    @mock.patch('covid_ml.data_ops.DataGetter.get_api_data',return_value=["json",test_icu_16_json]) # mock the method to return the the test json data
    @mock.patch('covid_ml.data_ops.DataGetter.build_df',return_value=test_df) # mock build_df() method to return the test pandas data frame
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



if __name__ == "__main__":
        unittest.main()