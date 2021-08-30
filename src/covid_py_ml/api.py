from flask import Flask, make_response
from flask_cors import CORS
from db_ops.db_ops import ModelDataGetter

app = Flask(__name__)
# allow cross origin resource sharing
CORS(app)


@app.route("/ml/api/models", methods=['GET'])
def get_models():
    model_data_getter = ModelDataGetter()

    # if the db_exists property is None, then no database was ever created
    if model_data_getter.db_exists == None:
        return make_response("Database is missing", 200)
    
    # attempt to get the data
    response_payload = model_data_getter.get_models()

    # if false is returned, then an exception was experienced while trying to query the database
    if response_payload == False:
        return make_response("Internal database error", 500)
    
    # if None is returned, then no data was present in the database
    if response_payload == None:
        return make_response("No data for prediction models", 200)
    
    # otherwise, send back the dictionary (will automatically convert to json) we have
    return make_response(response_payload, 200)    

@app.route("/ml/api/predictions", methods=['GET'])
def get_predictions():
    model_data_getter = ModelDataGetter()

    # if the db_exists property is None, then no database was ever created
    if model_data_getter.db_exists == None:
        return make_response("Database is missing", 200)
    
    # attempt to get the data
    response_payload = model_data_getter.get_predictions()

    # if false is returned, then an exception was experienced while trying to query the database
    if response_payload == False:
        return make_response("Internal database error", 500)
    
    # if None is returned, then no data was present in the database
    if response_payload == None:
        return make_response("No data for prediction models", 200)
    
    # otherwise, send back the dictionary (will automatically convert to json) we have
    return make_response(response_payload, 200)    

@app.route("/ml/api/model-data/<int:model_id>", methods=['GET'])
def get_model_data(model_id):
    model_data_getter = ModelDataGetter()

    # if the db_exists property is None, then no database was ever created
    if model_data_getter.db_exists == None:
        return make_response("Database is missing", 200)
    
    # attempt to get the data
    response_payload = model_data_getter.get_model_data(model_id)

    # if false is returned, then an exception was experienced while trying to query the database
    if response_payload == False:
        return make_response("Internal database error", 500)
    
    # if None is returned, then no data was present in the database
    if response_payload == None:
        return make_response("No model data", 200)
    
    # otherwise, send back the dictionary (will automatically convert to json) we have
    return make_response(response_payload, 200)   


if __name__ == "__main__":
    app.run(debug=True)
