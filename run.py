import os
import pprint

from openods import app

pp = pprint.PrettyPrinter(indent=4)

if __name__ == "__main__":
    print(str.format("Database URL: {0}", app.config["DATABASE_URL"]))
    print(str.format("Cache Timeout: {0}", app.config["CACHE_TIMEOUT"]))
    print(str.format("APP Hostname: {0}", app.config["APP_HOSTNAME"]))
    print(str.format("API Path: {0}", app.config["API_PATH"]))
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
