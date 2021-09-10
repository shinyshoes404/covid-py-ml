# covid-py-ml

## Overview

covid-py-ml is a machine learning application used to predict the ICU utilization for the top 16 hospitals in Utah by analyzing data provided by the Utah COVID Tracker API. This application also provides a rest API to access the models and predictions it generates. You can find documentation for the Utah COVID Tracker API at https://utahcovidtrack.com/developer/api-docs.  
  
Once covid-py-ml docker image is built and running as a container, it will send a request to the Utah COVID Tracker API at 15 minutes past the hour, every hour, to check for new data. If new data is returned, covid-py-ml will rebuild its predictive model and make a prediction of ICU capacity for the top 16 hospitals two weeks from the current date. The first time the routine runs, two weeks of daily predictions are generated. The state of Utah typically publishes new data once per day between Noon and 2 PM Mountain Time.
  
covid-py-ml uses scikit-learn's LinearRegression model to build multiple linear and polynomial regression models based on the environment variables provided at container runtime. The 7 day moving averages of COVID case count and positive test rates for the entire State of Utah are used as the independent variables for the model.  
    
Sqlite is utilized to store data for this appllication. In the `docker run` and `docker compose` commands below, docker volumes are created and mapped for persitent storage of the Sqlite database file and application log files.

Becuase of the Delta variant, a linear model (MOCEL_N=1) using data after 5/1/2021 (CUTOFF_DATE=2021-05-01) seems to generate the most accurate predictions.  

NOTE: This project is just for fun and learning. It should NOT, in any way, be considered medical or scientific advice.

## Requirements

 - OS: Windows or Linux
 - Python 3.8 or 3.9
 - Docker
 - Docker Compose (optional)

## Quick start guide

### Build the docker image

 - Clone this project using git
 - Move into the root of this project
 - Run `docker build -t covid-py-ml:latest .`

### Start the container

#### Docker run
  
`docker run -itd -e CUTOFF_DATE=2021-05-01 -e MODEL_N=1 --name covid_py_ml -v covid_py_ml_db:/home/covidml/python_apps/apps/data -v covid_py_ml_logs:/home/covidml/covid_py_ml_logs -p 0.0.0.0:8080:8080 covid-py-ml:latest`  
 
 - Notice the two optional environment variables listed in the command above
   - CUTOFF_DATE is the oldest observation date that will be used to build the regression model
   - MODEL_N is the polynomial degree that will be used for the regression model (MODEL_N=1 indicates a linear model)
   -  If no environment variables are provided, then all available data will be used and a linear model will be created.

#### Docker compose

If docker compose is installed you can run `docker-compose up -d`.  

 - In the docker-compose.yml file, you will notice the `environment:` section
    - CUTOFF_DATE is the oldest observation date that will be used to build the regression model
    - MODEL_N is the polynomial degree that will be used for the regression model (MODEL_N=1 indicates a linear model)
    -  If no environment variables are provided, then all available data will be used and a linear model will be created.

#### Accessing the container

 - Either command above will start the covid-py-ml image as a container
 - It will take about 3 minutes for the container to fully spin up
 - Two persistent docker volumes will be mapped to store the logs and Sqlite database file
 - The API will be available on port 8080
    - `http://localhost:8080/ml/api/models` -- provides a list of all models built to date
    - `http://localhost:8080/ml/api/predictions` -- provides a list of all predictions made to date by the application
    - `http://localhost:8080/ml/api/model-data/<model id>` -- provides the data used to create the model with the model id provided in place of `<model id>`

## Dev and Test

### Installing for Dev and Test

 - Clone this repository using git
 - Move into the root of this project
 - Activate your python virtual environment
 - Install the covid-py-ml packages and dependencies with `pip install -e .[dev]`
    - setup.py is used with `pip install` when installing for development to enable the test modules located in `src/tests/` to run
    - The requirements.txt file is used when building the docker image

### Testing 

If you make any changes to the source code, you should verify everthing is working by running the unit tests and integreation tests in the project. To do that, use __coverage__ and __unittest__ to run test cases and measure code coverage for just the code written for this project.  

`coverage run --source=src/covid_py_ml -m unittest discover -v -s src/tests`  
  
Run `coverage report` to see a report of the amount of code covered by the tests that just ran.

