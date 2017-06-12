# OpenODS

## Continuous Integration
Builds are handled by Travis CI at [https://travis-ci.org/mattstibbs/open-ods](https://travis-ci.org/open-ods/open-ods)

[![Build Status](https://travis-ci.org/open-ods/open-ods.svg?branch=develop)](https://travis-ci.org/mattstibbs/open-ods) develop

[![Build Status](https://travis-ci.org/open-ods/open-ods.svg?branch=master)](https://travis-ci.org/mattstibbs/open-ods) master

Chat with us on Gitter! https://gitter.im/open-ods/open-ods

## Data
The current Postgres database dump is v014 and can be downloaded from https://s3.amazonaws.com/openods-assets/database_backups/openods_014.dump

## About the project

### Pre-requisites
#### Needed
* Python 3.6+
* Virtualenv `pip install -g virtualenv`
* PostgreSQL ([Postgres.app](http://postgresapp.com) is good for OSX development)

#### Optional
* [Heroku Toolbelt](https://toolbelt.heroku.com) - Helpful if you're going to use Heroku to host OpenODS
* [Download Docker](https://www.docker.com/) (Useful if you intend to use Docker!)

### Getting Started

1. Clone this repository to your local machine

    ```bash
    $ git clone https://github.com/mattstibbs/open-ods.git
    ```
  
  
2. In the terminal, navigate to the newly cloned repository on your machine

    ```bash
    $ cd ~/Source/open-ods
    ```


3. Create a Python3 Virtualenv

    ```bash
    $ virtualenv -p python3 openods
    ```

    Check that python3 is installed properly by running `python` and checking the version number displayed.

    ```bash
    $ python
    ```
    ```
    Python 3.6.1 (default, Apr  4 2017, 09:40:21)
    [GCC 4.2.1 Compatible Apple LLVM 8.1.0 (clang-802.0.38)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>>
    ```



4. Activate the virtualenv

    ```bash
    $ source env/bin/activate
    ```


5. Install libmemcached (for caching using [flask-heroku-cacheify](http://rdegges.github.io/flask-heroku-cacheify/))

    On OSX, you can use homebrew to easily install libMemcached

    ```bash
    $ brew install libmemcached
    ```

    _If you're using another OS you will have to refer to appropriate instructions for your OS._


6. Install the project dependencies from the `requirements-dev.txt` file.

    ```bash
    $ pip install -r requirements-dev.txt
    ```

    _Note: `requirements-dev.txt` contains a list of all dependencies including
    those needed during the development process._

    _When deploying to production, you would use the `requirements.txt` file to install dependencies._

7. Now follow this guide to import the OpenODS data into your local
database instance:

    [Importing OpenODS data to your PostgreSQL instance](docs/importing_to_postgres.md)

8. Assuming all steps have completed successfully, you should be able to
test that you can run OpenODS using the built-in Flask development server.

    From the project root, run:

    ```bash
    $ python run.py
    ```

    ```
    Database URL: postgresql://openods:openods@localhost:5432/openods
    Cache Timeout: 30
    APP Hostname: http://localhost:5000/api
    API Path: /api
    DEBUG: False

    * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
    ```

## Docker
To get an instance of OpenODS running in Docker, [follow this README](Docker/README.md)

## Source Data Attribution
Organisation Data Service, Health and Social Care Information Centre, licenced under the Open Government Licence v2.0  - Open Government Licence

More information on the Organisation Data Service can be found [on the HSCIC website](http://systems.hscic.gov.uk/data/ods)

## License
This project is licensed under GNU GPL v3.

Copyright (c) 2017 Matt Stibbs and Tony Yates

See [LICENSE.md](LICENSE.md).
