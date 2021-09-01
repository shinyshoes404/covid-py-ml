import pandas as pd

# json for tests - represents raw case count json from api
test_case_json = { "01/01/2021" : {"casecount" : 1956, "casecountdate":"01/01/2021", "geoarea":"State of Utah", "retrieveddate" : "03/13/2021 11:00 AM"},
               "01/02/2021" : {"casecount" : 1845, "casecountdate":"01/02/2021", "geoarea":"State of Utah", "retrieveddate" : "02/03/2021 02:00 PM"} }

# pandas data frame for tests - represents what is expected from DataGetter.build_df() from the raw json above
test_casecount_df = pd.DataFrame([[1956, "01/01/2021", "State of Utah", "03/13/2021 11:00 AM"], 
                                 [1845, "01/02/2021", "State of Utah", "02/03/2021 02:00 PM"]], 
                                 columns = ['casecount','casecountdate','geoarea', 'retrieveddate'])
                                 
test_casecount_df['casecountdate'] = pd.to_datetime(test_casecount_df['casecountdate'])
test_casecount_df = test_casecount_df.sort_values('casecountdate').reset_index(drop=True)


# json to use for testing - represents raw testing json data from api
test_testdata_json = { "01/01/2021" : {"geoarea":"State of Utah", "peoplepositive": 1888, "peopletested" : 5967, "retrieveddate" :	"08/04/2021 02:01 PM", "testdate" :	"01/01/2021"},
                        "01/02/2021" : {"geoarea" :	"State of Utah", "peoplepositive" :1906, "peopletested":5627, "retrieveddate": "07/30/2021 02:01 PM", "testdate" :	"01/02/2021"}}

# pandas data frame for tests - represents what is expectd from DataGetter.build_df() from the raw json above
test_testing_df = pd.DataFrame([["State of Utah", 1888, 5967, "08/04/2021 02:01 PM", "01/01/2021"],
                                ["State of Utah", 1906, 5627, "07/30/2021 02:01 PM", "01/02/2021"]],
                                columns = ['geoarea','peoplepositive','peopletested', 'retrieveddate','testdate'])

test_testing_df['testdate'] = pd.to_datetime(test_testing_df['testdate'])
test_testing_df = test_testing_df.sort_values('testdate').reset_index(drop=True)


# json to use for testing - represents raw icu utilization data for the top 16 hospitals provided by the api
test_icu_16_json = { "01/01/2021" : {"date":"01/01/2021", "icu-top16-hosp-covid-util":0.32,"icu-top16-hosp-total-util":	0.85,"retrieveddate":"01/03/2021 01:00 PM"},
                    "01/02/2021" : {"date":	"01/02/2021","icu-top16-hosp-covid-util": 0.33, "icu-top16-hosp-total-util":0.86, "retrieveddate":"01/03/2021 01:00 PM"}}


# pandas data frame for tests - represents what is expected from DataGetter.build_df() from the raw json above
test_icu_df = pd.DataFrame([["01/01/2021", 0.32, 0.85,"01/03/2021 01:00 PM" ],
                            ["01/02/2021",0.33,0.86,"01/03/2021 01:00 PM"]],
                            columns = ['date','icu-top16-hosp-covid-util','icu-top16-hosp-total-util', 'retrieveddate'])

test_icu_df['date'] = pd.to_datetime(test_icu_df['date'])
test_icu_df = test_icu_df.sort_values('date').reset_index(drop=True)

# json to use for full integeration testing - represents raw case count json from api
test_casecasecount_fulltest_json = {
    "08/22/2021":{"casecount":100,"casecountdate":"08/22/2021","geoarea":"State of Utah","retrieveddate":"08/24/2021 01:00 PM"},
    "08/23/2021":{"casecount":114,"casecountdate":"08/23/2021","geoarea":"State of Utah","retrieveddate":"08/30/2021 02:00 PM"},
    "08/24/2021":{"casecount":128,"casecountdate":"08/24/2021","geoarea":"State of Utah","retrieveddate":"08/27/2021 02:00 PM"},
    "08/25/2021":{"casecount":135,"casecountdate":"08/25/2021","geoarea":"State of Utah","retrieveddate":"08/30/2021 02:00 PM"},
    "08/26/2021":{"casecount":142,"casecountdate":"08/26/2021","geoarea":"State of Utah","retrieveddate":"08/30/2021 02:00 PM"},
    "08/27/2021":{"casecount":156,"casecountdate":"08/27/2021","geoarea":"State of Utah","retrieveddate":"08/31/2021 02:00 PM"},
    "08/28/2021":{"casecount":163,"casecountdate":"08/28/2021","geoarea":"State of Utah","retrieveddate":"08/31/2021 02:00 PM"},
    "08/29/2021":{"casecount":170,"casecountdate":"08/29/2021","geoarea":"State of Utah","retrieveddate":"08/31/2021 02:00 PM"}
    }


# sample dataframe of case count data - represents what is expected from DataGetter.get_casecount_date()
test_casecount_fulltest_df = pd.DataFrame([[pd.Timestamp('2021-08-22 00:00:00'), 100], 
                                            [pd.Timestamp('2021-08-23 00:00:00'), 114], 
                                            [pd.Timestamp('2021-08-24 00:00:00'), 128], 
                                            [pd.Timestamp('2021-08-25 00:00:00'), 135], 
                                            [pd.Timestamp('2021-08-26 00:00:00'), 142], 
                                            [pd.Timestamp('2021-08-27 00:00:00'), 156], 
                                            [pd.Timestamp('2021-08-28 00:00:00'), 163], 
                                            [pd.Timestamp('2021-08-29 00:00:00'), 170]],
                                            columns=['casecountdate', 'casecount'])

# json to use for full integeration testing - represents raw test data json from api
test_testing_fulltest_json = {
    "08/22/2021":{"geoarea":"State of Utah","peoplepositive":500,"peopletested":1000,"retrieveddate":"08/31/2021 02:01 PM","testdate":"08/22/2021"},
    "08/23/2021":{"geoarea":"State of Utah","peoplepositive":500,"peopletested":1000,"retrieveddate":"08/31/2021 02:01 PM","testdate":"08/23/2021"},
    "08/24/2021":{"geoarea":"State of Utah","peoplepositive":500,"peopletested":1000,"retrieveddate":"08/31/2021 02:01 PM","testdate":"08/24/2021"},
    "08/25/2021":{"geoarea":"State of Utah","peoplepositive":500,"peopletested":1000,"retrieveddate":"08/31/2021 02:01 PM","testdate":"08/25/2021"},
    "08/26/2021":{"geoarea":"State of Utah","peoplepositive":500,"peopletested":1000,"retrieveddate":"08/31/2021 02:01 PM","testdate":"08/26/2021"},
    "08/27/2021":{"geoarea":"State of Utah","peoplepositive":500,"peopletested":1000,"retrieveddate":"08/31/2021 02:01 PM","testdate":"08/27/2021"},
    "08/28/2021":{"geoarea":"State of Utah","peoplepositive":500,"peopletested":1000,"retrieveddate":"08/31/2021 02:01 PM","testdate":"08/28/2021"},
    "08/29/2021":{"geoarea":"State of Utah","peoplepositive":570,"peopletested":1000,"retrieveddate":"08/31/2021 02:01 PM","testdate":"08/29/2021"}
    }

# sample dataframe of case count data - represents what is expected from DataGetter.get_testing_date()
test_testing_fulltest_df = pd.DataFrame([[pd.Timestamp('2021-08-22 00:00:00'), 0.5], 
                                            [pd.Timestamp('2021-08-23 00:00:00'), 0.5], 
                                            [pd.Timestamp('2021-08-24 00:00:00'), 0.5], 
                                            [pd.Timestamp('2021-08-25 00:00:00'), 0.5], 
                                            [pd.Timestamp('2021-08-26 00:00:00'), 0.5], 
                                            [pd.Timestamp('2021-08-27 00:00:00'), 0.5], 
                                            [pd.Timestamp('2021-08-28 00:00:00'), 0.5], 
                                            [pd.Timestamp('2021-08-29 00:00:00'), 0.57]],
                                            columns=['testdate', 'pos-test-rate'])

test_icu_16_fulltest_json = {
    "09/10/2021":{"date":"09/10/2021","icu-top16-hosp-covid-util":0.05,"icu-top16-hosp-total-util":0.74,"retrieveddate":"05/13/2021 11:01 AM"},
    "09/11/2021":{"date":"09/11/2021","icu-top16-hosp-covid-util":0.14,"icu-top16-hosp-total-util":0.66,"retrieveddate":"11/22/2020 05:00 PM"},
    "09/12/2021":{"date":"09/12/2021","icu-top16-hosp-covid-util":0.11,"icu-top16-hosp-total-util":0.75,"retrieveddate":"05/14/2021 01:01 PM"},
    "09/13/2021":{"date":"09/13/2021","icu-top16-hosp-covid-util":0.16,"icu-top16-hosp-total-util":0.61,"retrieveddate":"11/22/2020 05:00 PM"},
    "09/14/2021":{"date":"09/14/2021","icu-top16-hosp-covid-util":0.09,"icu-top16-hosp-total-util":0.73,"retrieveddate":"05/14/2021 01:01 PM"},
    "09/15/2021":{"date":"09/15/2021","icu-top16-hosp-covid-util":0.15,"icu-top16-hosp-total-util":0.6,"retrieveddate":"11/22/2020 05:00 PM"},
    "09/16/2021":{"date":"09/16/2021","icu-top16-hosp-covid-util":0.1,"icu-top16-hosp-total-util":0.74,"retrieveddate":"05/15/2021 11:01 AM"},
    "09/17/2021":{"date":"09/17/2021","icu-top16-hosp-covid-util":0.14,"icu-top16-hosp-total-util":0.66,"retrieveddate":"11/22/2020 05:00 PM"},
    }

# sample dataframe of case count data - represents what is expected from DataGetter.get_icu_16_date()
test_icu_16_fulltest_df = pd.DataFrame([[pd.Timestamp('2021-08-22 00:00:00'), .74], 
                                            [pd.Timestamp('2021-08-23 00:00:00'), .66], 
                                            [pd.Timestamp('2021-08-24 00:00:00'), .75], 
                                            [pd.Timestamp('2021-08-25 00:00:00'), .61], 
                                            [pd.Timestamp('2021-08-26 00:00:00'), .73], 
                                            [pd.Timestamp('2021-08-27 00:00:00'), .6], 
                                            [pd.Timestamp('2021-08-28 00:00:00'), .74], 
                                            [pd.Timestamp('2021-08-29 00:00:00'), .66]],
                                            columns=['offset_date', 'icu-top16-hosp-total-util'])

# sample independent_df based on fulltest_json above
test_independent_df = pd.DataFrame([[pd.Timestamp('2021-08-28 00:00:00'),163, 0.5, 134.0, 0.5], 
                                    [pd.Timestamp('2021-08-29 00:00:00'),170, 0.57, 144.0 , 0.51]],
                                    columns=['date','casecount','pos-test-rate','casecount-mv-avg','pos-test-mv-avg'])

# sample model_data_df based on fulltest_json above
test_model_data_df = pd.DataFrame([[pd.Timestamp('2021-08-28 00:00:00'),163, 0.5, 134.0, 0.5, .74], 
                                    [pd.Timestamp('2021-08-29 00:00:00'),170, 0.57, 144.0 , 0.51, .66]],
                                    columns=['date','casecount','pos-test-rate','casecount-mv-avg','pos-test-mv-avg','icu-top16-hosp-total-util'])