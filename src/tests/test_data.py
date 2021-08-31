import pandas as pd

# json for tests
test_case_json = { "01/01/2021" : {"casecount" : 1956, "casecountdate":"01/01/2021", "geoarea":"State of Utah", "retrieveddate" : "03/13/2021 11:00 AM"},
               "01/02/2021" : {"casecount" : 1845, "casecountdate":"01/02/2021", "geoarea":"State of Utah", "retrieveddate" : "02/03/2021 02:00 PM"} }

# pandas data frame for tests
test_casecount_df = pd.DataFrame([[1956, "01/01/2021", "State of Utah", "03/13/2021 11:00 AM"], 
                                 [1845, "01/02/2021", "State of Utah", "02/03/2021 02:00 PM"]], 
                                 columns = ['casecount','casecountdate','geoarea', 'retrieveddate'])
                                 
test_casecount_df['casecountdate'] = pd.to_datetime(test_casecount_df['casecountdate'])
test_casecount_df = test_casecount_df.sort_values('casecountdate').reset_index(drop=True)


# json to use for testing
test_testdata_json = { "01/01/2021" : {"geoarea":"State of Utah", "peoplepositive": 1888, "peopletested" : 5967, "retrieveddate" :	"08/04/2021 02:01 PM", "testdate" :	"01/01/2021"},
                        "01/02/2021" : {"geoarea" :	"State of Utah", "peoplepositive" :1906, "peopletested":5627, "retrieveddate": "07/30/2021 02:01 PM", "testdate" :	"01/02/2021"}}

# pandas data frame for tests
test_testing_df = pd.DataFrame([["State of Utah", 1888, 5967, "08/04/2021 02:01 PM", "01/01/2021"],
                                ["State of Utah", 1906, 5627, "07/30/2021 02:01 PM", "01/02/2021"]],
                                columns = ['geoarea','peoplepositive','peopletested', 'retrieveddate','testdate'])

test_testing_df['testdate'] = pd.to_datetime(test_testing_df['testdate'])
test_testing_df = test_testing_df.sort_values('testdate').reset_index(drop=True)


# json to use for testing
test_icu_16_json = { "01/01/2021" : {"date":"01/01/2021", "icu-top16-hosp-covid-util":0.32,"icu-top16-hosp-total-util":	0.85,"retrieveddate":"01/03/2021 01:00 PM"},
                    "01/02/2021" : {"date":	"01/02/2021","icu-top16-hosp-covid-util": 0.33, "icu-top16-hosp-total-util":0.86, "retrieveddate":"01/03/2021 01:00 PM"}}


# pandas data frame for tests
test_icu_df = pd.DataFrame([["01/01/2021", 0.32, 0.85,"01/03/2021 01:00 PM" ],
                            ["01/02/2021",0.33,0.86,"01/03/2021 01:00 PM"]],
                            columns = ['date','icu-top16-hosp-covid-util','icu-top16-hosp-total-util', 'retrieveddate'])

test_icu_df['date'] = pd.to_datetime(test_icu_df['date'])
test_icu_df = test_icu_df.sort_values('date').reset_index(drop=True)


# sample build dataframe of case count
test_casecount_built_df = pd.DataFrame([[pd.Timestamp('2021-08-22 00:00:00'), 644], 
                                        [pd.Timestamp('2021-08-23 00:00:00'), 1139], 
                                        [pd.Timestamp('2021-08-24 00:00:00'), 1579], 
                                        [pd.Timestamp('2021-08-25 00:00:00'), 1494], 
                                        [pd.Timestamp('2021-08-26 00:00:00'), 1296], 
                                        [pd.Timestamp('2021-08-27 00:00:00'),1604], 
                                        [pd.Timestamp('2021-08-28 00:00:00'), 1129], 
                                        [pd.Timestamp('2021-08-29 00:00:00'), 601]],
                                        columns=['casecountdate', 'casecount'])