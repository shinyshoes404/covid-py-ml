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