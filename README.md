# covid-py-ml

Machine learning application to predict the ICU utilization for the top 16 hospitals in Utah by analyzing data provided by the COVID Tracker suite of services.

## Badge dashboard
dev test coverage 
[![pipeline status](https://git.swilsycloud.com/%{project_path}/badges/dev/coverage.svg)](https://git.swilsycloud.com/%{project_path}/badges/dev)

## Dev and Test

### Testing

Use __coverage__ and __unittest__ to run test cases and measure code coverage for just the code written for this project.  

`coverage run --source=src/covid_py_ml -m unittest discover -v -s src/tests`