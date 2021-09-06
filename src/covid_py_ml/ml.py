from covid_ml.data_ops import DataGetter, PredictionChecker
import sys
from db_ops.db_ops import ModelDataAdder
from covid_ml.modeling import DataModeler

def ml_main():
    print("----- Starting machine learning routine ------")

    ### ------------------ GET THE DATA FROM THE API ------------------------ ###
    data_getter = DataGetter()

    check_casecount = data_getter.get_casecount_data()
    # if there is a problem, exit the application
    if check_casecount == None:
        print("Exit: Error -- Problem getting case count data")
        sys.exit(1)

    check_testing = data_getter.get_testing_data()
    # if there is a problem, exit the applicaation
    if check_testing == None:
        print("Exit: Error -- Problem getting testing data")
        sys.exit(1)

    check_icu_16 = data_getter.get_icu_16_data()
    # if there is a problem, exit the application
    if check_icu_16 == None:
        print("Exit: Error -- Problem getting icu top 16 data")
        sys.exit(1)

    # combine and transform the data we just fetched to get two data frames. One to use for building our regression model, and one with the independent variable data we need for predictions
    data_getter.combine_model_df()
    

    ### -----------  DO WE HAVE DATA THAT IS ELIGIBLE FOR PREDICTIONS? ---------------- ###
    # get the max prediction's date we have made so far
    prediction_checker = PredictionChecker()
    max_predict_date = prediction_checker.get_max_prediction_date()
    # a value of False being returned by get_max_prediction_date() means that our database does not exist yet.
    if max_predict_date == False:
        print("Exit: Error -- Your database was not setup correctly. Use db_setup.py to create the database before running ml.py")
        sys.exit(1)

    # determine the available independent data that we can use to make predictions, keeping in mind that we don't want to
    # repeat prediction dates, data must be > 5 days old to be used for a prediction, and we cannot make a prediction more than 19 days into the future
    predict_data_df = prediction_checker.get_prediction_data(max_predict_date, data_getter.independent_df)

    # if predict_data_df is None, then no data was found that is eligible to use for a prediction
    # otherwise, we should have a pandas data frame to work with
    if predict_data_df is None:
        print("Exit: No predictions to be made.")
        sys.exit(1)
    
    # if predict_data_df is False, then there wasn't any independent variable data recent enough
    # for us to use for a prediction. This might mean that while the api is returning data, it is
    # not providing updated/new data
    if predict_data_df is False:
        print("Exit: No recent independent variable data. Did we get updated data from the api?")
        sys.exit(1)


    ### -------------- BUILD THE MODEL ------------------ ###

    # get independent variable data from combined model dataframe
    x = data_getter.model_data_df[['casecount-mv-avg','pos-test-mv-avg']]
    # get the dependent variable data from the combined model dataframe
    y = data_getter.model_data_df[['icu-top16-hosp-total-util']]

    # intantiate the data modeler object based on the DataModeler class
    data_modeler = DataModeler()
    # create, fit, and score the model based on our data
    data_modeler.model_train(x,y)

    y_predict = data_modeler.predict(predict_data_df[['casecount-mv-avg','pos-test-mv-avg']])


    ### ------------------- ADD THE DATA TO THE DATABASE --------------------- ###
    # create an object to add the model information to the database
    data_adder = ModelDataAdder(model_date=prediction_checker.today_date,
                                model_score=data_modeler.model_score,
                                model_data=data_getter.model_data_df[['date','casecount-mv-avg','pos-test-mv-avg', 'icu-top16-hosp-total-util']],
                                icu_predictions=y_predict,
                                icu_prediction_dates=predict_data_df['predict-date'])

    # insert the data to the database
    data_adder.add_data()


if __name__ == "__main__":
    ml_main()


