import os, sqlite3

from ml_config.ml_config import DbConfig

class DbBuilder:
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
                                                                                        
            
            finally:
                # make sure the cursor and connection get closed
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()


def build_db():
    db_builder = DbBuilder()
    db_builder.create_db()


if __name__ == "__main__":
    build_db()