import os
import pprint

from app import app

pp = pprint.PrettyPrinter(indent=4)

if __name__ == "__main__":
    print(str.format("Database URL: {0}", app.config["DATABASE_URL"]))
    print(str.format("Cache Timeout: {0}", app.config["CACHE_TIMEOUT"]))
    print(str.format("App Hostname: {0}", app.config["APP_HOSTNAME"]))
    print(str.format("App User: {0}", app.config["API_USER"]))
    print(str.format("App Password: {0}", app.config["API_PASS"]))
    print(str.format("API URL: {0}", app.config["API_URL"]))
    print(str.format("DEBUG: {0}", app.config["DEBUG"]))

    # Lists all routing rules registered on the Flask app
    rules_list = []
    for rule in app.url_map.iter_rules():
        rules_list.append(rule)
    print("Rules List:")
    pp.pprint(rules_list)

    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
