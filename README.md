# covid-py-ml

Machine learning application to predict the ICU utilization for the top 16 hospitals in Utah by analyzing data provided by the COVID Tracker suite of services.

## Code coverage

[![coverage](https://git.swilsycloud.com/covid_tracker/apps/covid-py-ml/badges/dev/coverage.svg)](https://git.swilsycloud.com/covid_tracker/apps/covid-py-ml/badges/dev)
dev test coverage   
&nbsp;  
  

## Dev and Test

### Testing 

Use __coverage__ and __unittest__ to run test cases and measure code coverage for just the code written for this project.  

`coverage run --source=src/covid_py_ml -m unittest discover -v -s src/tests`

## Starting the container

### Docker run
`docker run -itd -e CUTOFF_DATE=2021-04-01 -e MODEL_N=3 --name covid_py_ml -v covid_py_ml_db:/home/covidml/python_apps/apps/data -v covid_py_ml_logs:/home/covidml/covid_py_ml_logs -p 0.0.0.0:8080:8080 covid-py-ml:latest`

### Docker Compose
