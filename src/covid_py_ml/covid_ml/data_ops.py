from ml_config.ml_config import MlConfig
import requests, pandas as pd


class DataGetter:
    
    def __init__(self):
        pass

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
        # fetch the raw json
        self.casecount_raw = requests.get(MlConfig.conf_urls.get('casecounts'))
        # create the data frame from the raw json
        self.casecount_df = self.build_df(self.casecount_raw, "casecountdate")
        # remove the columns we don't want
        self.casecount_df = self.casecount_df.drop(labels=['geoarea','retrieveddate'],axis=1)




