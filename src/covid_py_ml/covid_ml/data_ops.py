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




