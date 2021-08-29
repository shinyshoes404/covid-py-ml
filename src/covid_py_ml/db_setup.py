from db_ops.db_ops import DbBuilder

def build_db():
    db_builder = DbBuilder()
    db_builder.create_db()


if __name__ == "__main__":
    build_db()