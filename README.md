# open-ods

**This is an unofficial personal project making use of open data and is unrelated to the NHS and associated organisations**

**The data is regularly changing and so there is absolutely no guarantee on stability or accuracy.**

### Source Data Attribution
Organisation Data Service, Health and Social Care Information Centre, licenced under the Open Government Licence v2.0  - Open Government Licence

More information on the Organisation Data Service can be found [on the HSCIC website](http://systems.hscic.gov.uk/data/ods)


## Getting Started

### Pre-requisites
* Python 3.4+
* Virtualenv `pip install -g virtualenv`
* PostgreSQL ([Postgres.app](http://postgresapp.com) is good for OSX development)
* [Heroku Toolbelt](https://toolbelt.heroku.com) (Not mandatory but helpful if you're going to interact with Heroku)

### Steps

1. Clone this repository to your local machine

    ```bash
    git clone https://github.com/mattstibbs/open-ods.git
    ```
  
  
2. In the terminal, navigate to the directory of the repository e.g.

    ```bash
    cd ~/Source/open-ods
    ```


3. Create a Python3 Virtualenv

    ```bash
    virtualenv -p python3 env
    ```

    Check that python3 is installed properly by running `python` and checking the version.



4. Activate the virtualenv

    ```bash
    source env/bin/activate
    ```


5. Install libmemcached (for caching using [flask-heroku-cacheify](http://rdegges.github.io/flask-heroku-cacheify/))

    ```bash
    brew install libmemcached
    ```


6. Do a pip install

    ```bash
    pip install -r requirements.txt
    ```


7. Now go import the ODS data into your OpenODS database -> [Instructions for importing the ODS data into your PostgreSQL database](docs/data_import.md)
