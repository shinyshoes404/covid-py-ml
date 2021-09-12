from setuptools import setup

with open("README.md", "r") as fh:
    readme_long_description = fh.read()

setup(
    name='covid-py-ml',
    version='0.1.5',    
    description="A machine learning application to predict the ICU utilization for the top 16 hospitals in Utah by analyzing data provided by the Utah COVID Tracker API.",
    long_description=readme_long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/shinyshoes404/covid-py-ml',
    author='shinyshoes',
    author_email='shinyshoes404@protonmail.com',
    license='MIT License',
    packages=['covid_ml','ml_config','db_ops'],
    package_dir={'':'src/covid_py_ml'},
    install_requires=[
        'requests', 'pandas', 'scikit-learn', 'flask', 'flask-cors'
    ],

    extras_require={
        # To install requirements for dev work use 'pip install -e .[dev]'
        'dev': ['coverage', 'mock'],
        # To install requirements for exploring the source code and visualizing the predcition data use 'pip install -e .[explore]'
        'explore' : ['coverage', 'mock', 'jupyter']
    },

    python_requires = '>=3.8.*,!=3.10.*',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows'           
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)
