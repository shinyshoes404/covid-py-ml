from ml_config.ml_config import DbConfig, MlConfig
from db_ops.db_ops import DbChecker
import requests, pandas as pd, json, sqlite3
from datetime import datetime, timedelta


class DataGetter:
    
    def __init__(self):
        pass
    
    # method to get data from api  
    def get_api_data(self, url):
        # try a get request from the api
        try:
            response = requests.get(url)            
        # if the request cannot reach the destination server, we will get this
        except requests.exceptions.ConnectionError:
            return ["error","connection error"]
        
        # if the response status code is not 200, we have a problem
        if response.status_code != 200:
            return ["error", "response code {0}".format(response.status_code)]
        
        # try to pull the json from the repsonse content
        try:
            response_json = response.json()
        # if there is missing or malformed json in the reponse's content, we will get this
        except json.decoder.JSONDecodeError:
            return ["error","json error"]
        
        return ["json", response_json]


    # method to build out data frames from raw json
    def build_df(self,raw_json, date_col_name):
        new_dict = {"my_data" : []}

        # loop through the data in the raw_json and append each data point to the my_data object's array of objects
        for data_points in raw_json:
            new_dict['my_data'].append(raw_json[data_points])
        
        # create the data frame from the dictionary we made
        df = pd.json_normalize(new_dict, "my_data")
        # convert the date string in the data frame to a datetime data type
        df[date_col_name] = pd.to_datetime(df[date_col_name])

        # sort the data frame by date and reset the index, then return the dataframe
        return df.sort_values(date_col_name).reset_index(drop=True)

    def get_casecount_data(self):
        # fetch the raw response
        self.casecount_raw = self.get_api_data(MlConfig.conf_urls.get('casecounts'))

        # if there was an error while trying to get the data from the api, print an error for logging and return None
        if self.casecount_raw[0] == "error":
            # print for logging
            print("get_casecount_data() -- " + self.casecount_raw[0] + " -- " + self.casecount_raw[1])
            return None
           
        # create the data frame from the raw json
        self.casecount_df = self.build_df(self.casecount_raw[1], "casecountdate")        
        # only keep the columns we want
        self.casecount_df = self.casecount_df[['casecountdate','casecount']]  


        # return true to indicate everything worked
        return True
    
    def get_testing_data(self):
        # fetch the raw response
        self.testing_raw = self.get_api_data(MlConfig.conf_urls.get('testing'))

        # if there was an error while trying to get the data from the api, print an error for logging and return None
        if self.testing_raw[0] == "error":
            # print for logging
            print("get_testing_data() -- " + self.testing_raw[0] + " -- " + self.testing_raw[1])
            return None
             
        # create the data frame from the raw json
        self.testing_df = self.build_df(self.testing_raw[1], "testdate")
        #calculate the positive test rate
        self.testing_df['pos-test-rate'] = round(self.testing_df['peoplepositive']/self.testing_df['peopletested'],4)
        # only keep the columns we want
        self.testing_df = self.testing_df[['testdate','pos-test-rate']]

        # return true to indicate everything worked
        return True
    
    def get_icu_16_data(self):
        # fetch the raw response
        self.icu_16_raw = self.get_api_data(MlConfig.conf_urls.get('icu-top16'))

        # if there was an error while trying to get the data from the api, print an error for logging and return None
        if self.icu_16_raw[0] == "error":
            # print for logging
            print("get_icu_16_data() -- " + self.icu_16_raw[0] + " -- " + self.icu_16_raw[1])
            return None
             
        # create the data frame from the raw json
        self.icu_16_df = self.build_df(self.icu_16_raw[1], "date")
        # calculate offset date
        self.icu_16_df['offset_date'] = self.icu_16_df['date'] - pd.to_timedelta(MlConfig.icu_date_offset,unit='d')
        # only keep the columns we want
        self.icu_16_df = self.icu_16_df[['offset_date','icu-top16-hosp-total-util']]

        # return true to indicate everything worked
        return True

    
    def combine_model_df(self):
        # join the case count and testing data frames
        self.independent_df = pd.merge(self.casecount_df, self.testing_df, how="inner", left_on="casecountdate", right_on="testdate")
        # drop the extra date column and rename the other
        self.independent_df = self.independent_df.drop(labels=['testdate'], axis=1)
        # call the smooth_df method to smooth the data for our independent variables, this will add moving average columns to our independent_df
        self.smooth_df(MlConfig.mv_avg_days)

        # join the new model_data_df data frame with the icu 16 data
        self.model_data_df = pd.merge(self.independent_df, self.icu_16_df, how="inner", left_on="date", right_on="offset_date")
        # drop unneeded field
        self.model_data_df = self.model_data_df.drop(labels=['offset_date'], axis=1)

        

    def smooth_df(self,mv_avg_days=7):

        # smooth data for both the model and to use for predicting
        # Model data to smooth
        # get the list of dates from our combined data frame
        date_arry = pd.Series(self.independent_df['casecountdate']).tolist()
        # get moving average for test rate
        pos_avg_test_arry = pd.Series(self.independent_df['pos-test-rate']).rolling(mv_avg_days).mean().tolist()
        # get moving average for case count
        casecount_avg_arry = pd.Series(self.independent_df['casecount']).rolling(mv_avg_days).mean().tolist()

        # trim off the oldest mv_avg_days - 1 days of data, because they will not be able to calculate
        for i in range(0, mv_avg_days - 1):
            date_arry.pop(0)
            pos_avg_test_arry.pop(0)
            casecount_avg_arry.pop(0)
        
        # create a dictionary of our smooth data
        smooth_data = {'smooth_date' : date_arry,
                        'pos-test-mv-avg' : pos_avg_test_arry,
                        'casecount-mv-avg': casecount_avg_arry}
        # create a data frame of the smoothed data
        self.smooth_data_df = pd.DataFrame(smooth_data, columns=['smooth_date','casecount-mv-avg','pos-test-mv-avg'])
        # combine the smoothed data with the independent data frame
        self.independent_df = pd.merge(self.independent_df, self.smooth_data_df, how="inner", left_on="casecountdate", right_on="smooth_date")
        # drop the smooth date field from the combined data frame
        self.independent_df = self.independent_df.drop(labels=['smooth_date'], axis=1)
        # rename the date column of our independent data frame
        self.independent_df.rename(columns = {"casecountdate" : "date"}, inplace=True)


class PredictionChecker:
    def __init__(self):
        # verify that the database exists
        db_checker = DbChecker()
        self.check_db = db_checker.db_exists

    def get_max_prediction_date(self):
        # Does a database file exist?
        if self.check_db == None:
            # if not, return False and stop looking for a prediction date
            return False

        # get the max prediction date that we have so far from the database
        conn = sqlite3.connect(DbConfig.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT MAX(predict_date) as furthest_predict FROM model_prediction;")
            max_predict_date = cursor.fetchone()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        
        # if we don't have any predictions, return None
        if max_predict_date == (None,):
            return None
        else:
            # return the max date as date object with date and time (at midnight)
            return datetime.strptime(max_predict_date[0], "%Y-%m-%d %H:%M:%S")
    
    # max_predict is expected to be a date object with no time or None
    def get_prediction_data(self, max_predict_date, independent_df):
        # figure out what days you can predict
        # only data from independent_df that is > 4 days old (from today) and < 19 days older than today (assuming that icu_date_offset is set to 19 in ml_config.MlConfig)
        # It takes 5 days for case count and test data collected to stabilize and mature, data needs to be at least 6 days old to use
        # Our model attempts to predict icu utilization 19 days from the independent variable data used to predict it. The farthest back we can go is 19 days
        # in order to predict today's (published tomorrow) icu utilization level

        # get today's date (based on this machine's timezone), keeping datetime format, but trimming off hours, min, sec, milisec for easier date math and comparison
        self.today_date = datetime.strptime(datetime.today().date().strftime("%Y-%m-%d"),"%Y-%m-%d")

        # determine the lower bound that should be used when searching for eligible independent variable data by date
        # if no predictions have been made yet (None), then use today - 19 days as the lower bound for our independent variable data
        if max_predict_date == None:
            self.low_bound_ind_data_date = self.today_date - timedelta(days=MlConfig.icu_date_offset)
        else:
            # otherwise, use the greater of today - 19 days and max prediction date - 19 days
            if max_predict_date - timedelta(days=19) < self.today_date - timedelta(days=MlConfig.icu_date_offset):
                self.low_bound_ind_data_date = self.today_date - timedelta(days=MlConfig.icu_date_offset)
            else:
                self.low_bound_ind_data_date = max_predict_date - timedelta(days=MlConfig.icu_date_offset)
        
        # the upper bound for our independent variable data search by date will be today - 4 days (assuming data_days_to_mature is set to that in MlConfig )
        self.upper_bound_ind_data_date = self.today_date - timedelta(days=MlConfig.data_days_to_mature)
        
        # if the upper bound and lower bound are only one day apart, then we already have the most current prediction, return None
        if self.low_bound_ind_data_date == self.upper_bound_ind_data_date - pd.to_timedelta(1, unit='d'):
            return None

        # if not, find all of the data that can be used to make a prediction
        prediction_data_df = independent_df[(independent_df['date'] > self.low_bound_ind_data_date) & (independent_df['date'] < self.upper_bound_ind_data_date)]
        
        # this next section came about to deal with two inconsistent issues with Pandas. Something about truth value being ambiguous, and copying a slice.
        # after filtering the data down to what I needed, I am just creating arrays from the filtered data, and building a new dataframe so I can calculate the predict-date
        prediction_data_date = pd.Series(prediction_data_df['date']).tolist()
        prediction_data_cascount = pd.Series(prediction_data_df['casecount-mv-avg']).tolist()
        prediction_data_testrate = pd.Series(prediction_data_df['pos-test-mv-avg']).tolist()
        prediction_data = {'date' : prediction_data_date,
                            'casecount-mv-avg': prediction_data_cascount,
                            'pos-test-mv-avg' : prediction_data_testrate        
                            }
        
        final_pred_df = pd.DataFrame(prediction_data, columns=['date','casecount-mv-avg','pos-test-mv-avg'])
        final_pred_df['predict-date'] = final_pred_df['date'] + pd.to_timedelta(MlConfig.icu_date_offset,unit='d')
       
        return final_pred_df
        
        



     






