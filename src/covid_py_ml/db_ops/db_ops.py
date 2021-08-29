import os, sqlite3
from ml_config.ml_config import DbConfig, MlConfig

class DbChecker:
    def __init__(self):
        self.db_exists = self.check_for_db()
    
    def check_for_db(self):
        # look for db directory
        if os.path.isdir(DbConfig.db_dir):
            # look for db file
            if os.path.exists(DbConfig.db_path):
                return True
            # if no db file return None
            else:
                return None
        # if no db directory, make the directory and return none
        else:
            os.mkdir(DbConfig.db_dir)
            return None

class DbBuilder:
    def __init__(self):
        db_checker = DbChecker()
        self.db_exists = db_checker.db_exists
    
    
    def create_db(self):
        # if the database file does not exist, build out the database
        if self.db_exists == None:
            # creating the connection, automatically creates the file
            connection = sqlite3.connect(DbConfig.db_path)
            # create a cursor to interact with the database
            cursor = connection.cursor()

            # use a try finally block to make sure the database connection gets closed
            try:

                # create a table to house our the final data used to train our model for each prediction
                cursor.execute('''CREATE TABLE IF NOT EXISTS model_data (row_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                        model_id INTEGER NOT NULL,
                                                                        observation_date TEXT NOT NULL,
                                                                        casecount_mv_avg REAL NOT NULL,
                                                                        pos_test_mv_avg REAL NOT NULL,
                                                                        icu_top16_hosp_total_util REAL NOT NULL
                                                                        );''')
                
                # create a table to house our models
                cursor.execute('''CREATE TABLE IF NOT EXISTS models (model_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                        model_date TEXT NOT NULL,
                                                                        model_score REAL NOT NULL,
                                                                        model_poly_degree INTEGER NOT NULL,
                                                                        model_mv_avg_days INTEGER NOT NULL
                                                                        );''')

                # create a table to house our icu utilization prediction
                cursor.execute('''CREATE TABLE IF NOT EXISTS model_prediction (row_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                                model_id INTEGER NOT NULL,
                                                                                icu_16_prediction REAL NOT NULL,
                                                                                predict_date TEXT NOT NULL
                                                                                );''')
                # commit our changes                                                                                        
                connection.commit()
                
            finally:
                # make sure the cursor and connection get closed
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()


class ModelDataAdder:
    def __init__(self, model_date, model_score, model_data, icu_predictions, icu_prediction_dates):
        self.model_date = model_date
        self.model_score = model_score
        self.model_data = model_data
        self.icu_predictions = icu_predictions
        self.icu_prediction_dates = icu_prediction_dates
        

    def add_data(self):

        print("Attempting to insert data for model with date {0}".format(self.model_date.strftime("%Y-%m-%d")))

        ## -- build sql for model table -- ##
        self.sql_str_model = "INSERT INTO models (model_date, model_score, model_poly_degree, model_mv_avg_days) VALUES(:model_date, :model_score, :model_poly_degree, :model_mv_avg_days)"
        self.sql_dict_model = {"model_date" : self.model_date, "model_score" : self.model_score, "model_poly_degree" : MlConfig.poly_degree, "model_mv_avg_days" : MlConfig.mv_avg_days}
        
      
        ## -- build sql for model_prediction table -- #
        self.sql_str_predict = "INSERT INTO model_prediction (model_id, icu_16_prediction, predict_date) VALUES( ?, ?, ?);"
        

        ## -- build sql for model_data table -- #
        self.sql_str_model_data = "INSERT INTO model_data (model_id, observation_date, casecount_mv_avg, pos_test_mv_avg, icu_top16_hosp_total_util) VALUES(?, ?, ?, ?, ?);"

        ## -- we have to start the sql insert process to get the model_id (primary key of the first table we insert to)
        # we want the ability to roll back all transactions if we run into an error

        connection = sqlite3.connect(DbConfig.db_path)
        cursor = connection.cursor()

        try:
            ## -- INSERT MODEL -- ##
            # execute the sql to insert the model data into the table
            cursor.execute(self.sql_str_model, self.sql_dict_model)
            # capture the id of the model we just inserted to use as the model_id in the other tables
            self.model_id = cursor.lastrowid

            ## -- INSERT PREDICTIONS -- ##
            # build out our list of tuples to feed into the model_predition table INSERT statement. 
            # start with a list so we can easily append
            self.sql_tuple_predict = []           
            i = 0
            # iterate through the predictions and build out our tuples
            for prediction in self.icu_predictions:                
                self.sql_tuple_predict.append((self.model_id, prediction[0], self.icu_prediction_dates[i].to_pydatetime()))                
                i = i+1
                        
            # use the execute many function in case we have multiple predictions to add to the table
            cursor.executemany(self.sql_str_predict, self.sql_tuple_predict)

            ## -- INSERT MODEL DATA -- ##
            # capture the data used to build the model by inserting it into the model_data table

            # build out the tuple of tuples we need to insert all of the records
            # reset the temp_list and counter
            self.sql_tuple_model_data = []
            i = 0
            for dates in self.model_data['date']:
                self.sql_tuple_model_data.append((self.model_id, dates.to_pydatetime(), self.model_data['casecount-mv-avg'][i], self.model_data['pos-test-mv-avg'][i], self.model_data['icu-top16-hosp-total-util'][i]))
                i = i + 1
            # use the executemany function to insert the records
            cursor.executemany(self.sql_str_model_data, self.sql_tuple_model_data)
            
            # commit the changes now that everything has worked without an exception
            connection.commit()
            print("--- Success! Model data saved in the database for model_id: {0}  model_date: {1}  model_score: {2}  n={3}\n".format(self.model_id, self.model_date.strftime("%Y-%m-%d"), self.model_score, MlConfig.poly_degree))

        except Exception as e:
            connection.rollback()
            print(e)
            print("Error: Rolling back all database updates for model_id: {0}  model_date: {1}\n".format(self.model_id, self.model_date.strftime("%Y-%m-%d")))            

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()