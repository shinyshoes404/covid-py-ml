from covid_ml.data_ops import DataGetter
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




