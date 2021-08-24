import unittest, mock, pandas as pd

# import the DataGetter class for testing
from covid_ml.data_ops import DataGetter

# json for tests
test_case_json = { "01/01/2021" : {"casecount" : 1956, "casecountdate":"01/01/2021", "geoarea":"State of Utah", "retrieveddate" : "03/13/2021 11:00 AM"},
               "01/02/2021" : {"casecount" : 1845, "casecountdate":"01/02/2021", "geoarea":"State of Utah", "retrieveddate" : "02/03/2021 02:00 PM"} }

# testing the build_df() method
class TestDataGetterBuildDf(unittest.TestCase):

    # verify with test data
    def test_unit_valid_data(self):
        validation_obj = DataGetter()
        check_validation = validation_obj.build_df(test_case_json, "casecountdate")
        self.assertEqual(len(check_validation), 2, "DataGetter.build_df: expecting 2")
    
    # verify type error if not enough arguments are provided
    def test_unit_missing_arg(self):
        validation_obj = DataGetter()
        with self.assertRaises(TypeError):
            validation_obj.build_df("casecountdate")


# testing the get_casecount_data() method
class TestDataGetterGetCasecountData(unittest.TestCase):

    # pandas data frame for tests
    test_df = pd.DataFrame([[1956, "01/01/2021", "State of Utah", "03/13/2021 11:00 AM"], [1845, "01/02/2021", "State of Utah", "02/03/2021 02:00 PM"]], columns = ['casecount','casecountdate','geoarea', 'retrieveddate'])
    test_df['casecountdate'] = pd.to_datetime(test_df['casecountdate'])
    test_df = test_df.sort_values('casecountdate').reset_index(drop=True)


    # verify that the final data frame is the right number of columns (removed unwanted columns)
    @mock.patch('requests.get',return_value=test_case_json) # mock the request.get() method to return the the test json data
    @mock.patch('covid_ml.data_ops.DataGetter.build_df',return_value=test_df) # mock build_df() method to return the test pandas data frame
    def test_unit_remove_columns(self, mock_build_df, mock_requests_get):
        validation_object = DataGetter()
        validation_object.get_casecount_data()
        self.assertEqual(len(validation_object.casecount_df.columns), 2, "DataGetter.get_casecount_data: Expecting 2")

    # verify that the final data frame is sorted correctly
    @mock.patch('requests.get',return_value=test_case_json) # mock the request.get() method to return the the test json data
    def test_integ_correct_sort(self, mock_requests_get):
        validation_object = DataGetter()
        validation_object.get_casecount_data()
        # expecting 01/02/2021 to be in the second row (0 index) in the date column
        self.assertEqual(validation_object.casecount_df.iloc[1]['casecountdate'], pd.Timestamp(2021, 1, 2), "DataGetter.get_casecount_data: Expecting '01/02/2021'")
    
  



      