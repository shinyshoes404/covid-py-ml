from db_ops.db_ops import DbBuilder
# run this python script to build out the sqlite database for the first time
# if the database file already exits, no database creation or CREATE TABLE queries will be run
def build_db():
    db_builder = DbBuilder()
    db_builder.create_db()


if __name__ == "__main__":
    build_db()