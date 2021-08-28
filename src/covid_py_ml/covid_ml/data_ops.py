from ml_config.ml_config import MlConfig
import requests, pandas as pd, json


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


