# open-ods

## Source Data
### Attribution
Organisation Data Service, Health and Social Care Information Centre, licenced under the Open Government Licence v2.0  - Open Government Licence

## Getting Started

### Pre-requisite Steps
* Install Python 3.4+
* Install Virtualenv
* Install PostgreSQL ([Postgres.app](http://postgresapp.com) is good for OSX development)
* Install lib
* Install Heroku Toolbelt

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
