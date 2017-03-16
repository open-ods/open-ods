import os
import pprint
pp = pprint.PrettyPrinter(indent=4)

from app import app

if __name__ == "__main__":
    # Check for an environment variable for the listening port, and use 5000 if not available
    port = int(os.environ.get("PORT", 5000))

    print(str.format("Database URL: {0}", app.config["DATABASE_URL"]))
    print(str.format("Cache Timeout: {0}", app.config["CACHE_TIMEOUT"]))
    print(str.format("App Hostname: {0}", app.config["APP_HOSTNAME"]))
    print(str.format("App User: {0}", app.config["API_USER"]))
    print(str.format("App Password: {0}", app.config["API_PASS"]))
    print(str.format("API URL: {0}", app.config["API_URL"]))

    rules_list = []
    # Lists all routing rules registered on the Flask app
    for rule in app.url_map.iter_rules():
        rules_list.append(rule)
    print("Rules List:")
    pp.pprint(rules_list)

    app.run(
        host="0.0.0.0",
        port=port,
        debug=app.config["DEBUG"]
    )
