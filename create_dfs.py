from covid_ml.data_ops import DataGetter
import pandas as pd

# data_getter = DataGetter()

# check_casecount = data_getter.get_casecount_data()


# check_testing = data_getter.get_testing_data()

# check_icu_16 = data_getter.get_icu_16_data()

# print(data_getter.casecount_df.tail(8))
# # print(data_getter.testing_df.tail(8))
# # print(data_getter.icu_16_df.tail(8))

# lis = []
# for index, rows in data_getter.casecount_df.tail(8).iterrows():
#     lis.append([rows['casecountdate'], rows['casecount']])

# print(lis)

test_casecount_built_df = pd.DataFrame([[pd.Timestamp('2021-08-22 00:00:00'), 644], 
                                        [pd.Timestamp('2021-08-23 00:00:00'), 1139], 
                                        [pd.Timestamp('2021-08-24 00:00:00'), 1579], 
                                        [pd.Timestamp('2021-08-25 00:00:00'), 1494], 
                                        [pd.Timestamp('2021-08-26 00:00:00'), 1296], 
                                        [pd.Timestamp('2021-08-27 00:00:00'),1604], 
                                        [pd.Timestamp('2021-08-28 00:00:00'), 1129], 
                                        [pd.Timestamp('2021-08-29 00:00:00'), 601]],
                                        columns=['casecountdate', 'casecount'])

print(test_casecount_built_df)