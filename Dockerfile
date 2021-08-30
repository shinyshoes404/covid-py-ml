# syntax = docker/dockerfile:1.0-experimental
### NOTE: The comment line above is critical. It allows for the user of Docker Buildkit to inject secrets in the image at build time ###
# to build docker image
# $ export DOCKER_BUILDKIT=1
# $ docker build -t git.swilsycloud.com:5050/covid_tracker/apps/covid-py-ml:v0.1.x  .

# use the base ubuntu image to start
FROM ubuntu:20.04



#### ---- ARGS AND ENVS FOR BUILD ---- ####

### - ENVS - ###

# default user
ENV USERNAME=covidml
# set the python applications root directory
ENV PY_ROOT_DIR=/home/${USERNAME}/python_apps
# set the directory to store your python application
ENV PY_APP_DIR=${PY_ROOT_DIR}/apps
# set the directory for virtual environments
ENV PY_VIRTUAL_DIR=${PY_ROOT_DIR}/virtual_envs
# set the name of the virtual environment
ENV VIRTUAL_ENV=${PY_VIRTUAL_DIR}/venv_ml
# set database directory
ENV DB_DIR=${PY_APP_DIR}/data
# set log directory
ENV LOG_DIR=/home/${USERNAME}/covid_py_ml_logs
# set the timezone info
ENV TZ=America/Chicago


#### ---- BASIC SYSTEM SETUP ---- ####

# check for updates 
# then upgrade the base packages
# set timezone
# Set the locale
# install tzdata package (to make timezone work)
# install nano
# disable root user
# create our default user
RUN  apt-get update && \
    apt-get upgrade -y && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt-get install locales -y && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    apt-get install tzdata -y && \
    apt-get install nano -y && \
    passwd -l root &&\
    $(useradd -s /bin/bash -m ${USERNAME})

# setting local ENV variables
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8


#### ---- PYTHON ---- ####

# create directory for virtual envirionment
# create directory for python app
# create the data directory
# install pip3
# install virtualenv
# create virtual environment 
# activate virtual environment
# use pip to install gunicorn (for api)
RUN mkdir -p "$PY_VIRTUAL_DIR" && \
    mkdir "$PY_APP_DIR" && \
    mkdir ${DB_DIR} && \
    apt-get install python3-pip -y && \
    apt-get install python3-virtualenv -y && \
    virtualenv -p python3.8 "$VIRTUAL_ENV" && \
    . "$VIRTUAL_ENV/bin/activate" && \
    pip install gunicorn


COPY requirements.txt ${PY_APP_DIR}/

# move into the root of the project directory
# activate the virtual environment
# install the required dependencies
RUN cd ${PY_APP_DIR} && \
    . ${VIRTUAL_ENV}/bin/activate && \
    pip install -r requirements.txt && \
    rm requirements.txt

# copy the covid_py app into the container
COPY src/covid_py_ml ${PY_APP_DIR}/covid_py_ml
COPY run_db_setup.sh /home/${USERNAME}/
COPY run_ml.sh /home/${USERNAME}/
COPY run_api.sh /home/${USERNAME}/

#### --- WHAT TO DO WHEN THE CONTAINER STARTS --- ####

#  change ownership recursively of USERNAME home directory to make sure USERNAME has privileges to files copied into image
#  change ownership recursively of python application directory to that USERNAME has privileges to fiels copied into image
#  start the bash script to run python app
ENTRYPOINT chown -R ${USERNAME}:${USERNAME} /home/${USERNAME} && \
    chown -R ${USERNAME}:${USERNAME} ${PY_ROOT_DIR} && \
    su ${USERNAME} -c "/bin/bash /home/${USERNAME}/run_db_setup.sh" && \
    su ${USERNAME} -c "/bin/bash /home/${USERNAME}/run_api.sh" && \
    su ${USERNAME} -c "/bin/bash /home/${USERNAME}/run_ml.sh"
    