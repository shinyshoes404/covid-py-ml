from covid_ml.data_ops import DataGetter, PredictionChecker
import sys

from ml_config.ml_config import MlConfig


data_getter = DataGetter()

check_casecount = data_getter.get_casecount_data()
# if there is a problem, exit the application
if check_casecount == None:
    sys.exit("Error: Problem getting case count data")

check_testing = data_getter.get_testing_data()
# if there is a problem, exit the applicaation
if check_testing == None:
    sys.exit("Error: Problem getting testing data")

check_icu_16 = data_getter.get_icu_16_data()
# if there is a problem, exit the application
if check_icu_16 == None:
    sys.exit("Error: Problem getting icu top 16 data")

# combine the data we just fetched
data_getter.combine_model_df()

print(data_getter.independent_df.tail(10))
print(data_getter.model_data_df.tail(10))

# get the max prediction's date we have made so far
prediction_checker = PredictionChecker()
max_predict_date = prediction_checker.get_max_prediction_date()
if max_predict_date == False:
    sys.exit("Error: Your database was not setup correctly. Use db_setup.py to create the database before running ml.py")

# determine the available independent data that we can use to make predictions, keeping in mind that we don't want to
# repeat prediction dates, data must be > 5 days old to be used for a prediction, and we cannot make a prediction more than 19 days into the future
prediction_data = prediction_checker.get_prediction_data(max_predict_date, data_getter.independent_df)





