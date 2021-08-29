import os, sqlite3
from sqlite3.dbapi2 import connect

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
    def __init__(self, model_date, model_score, model_x_data, model_y_data, icu_predictions):
        self.model_date = model_date
        self.model_score = model_score
        self.model_x_data = model_x_data
        self.model_y_ydata = model_y_data
        self.icu_predictions = icu_predictions

    def add_model(self):
        sql_str = "INSERT INTO models (model_date, model_score, model_poly_degree, model_mv_avg_days) VALUES(:model_date, :model_score, :model_poly_degree, :model_mv_avg_days)"
        sql_dict = {"model_date" : self.model_date, "model_score" : self.model_score, "model_poly_degree" : MlConfig.poly_degree, "model_mv_avg_days" : MlConfig.mv_avg_days}
        
        connection = sqlite3.connect(DbConfig.db_path)
        cursor = connection.cursor()

        try:
            cursor.execute(sql_str, sql_dict)
            connection.commit()
            self.model_id = cursor.lastrowid
        
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

            

