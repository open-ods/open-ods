import os

from app import app

if __name__ == "__main__":
    # Check for an environment variable for the listening port, and use 5000 if not available
    port = int(os.environ.get("PORT", 5000))

    # Lists all routing rules registered on the Flask app
    for rule in app.url_map.iter_rules():
        print(rule)

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
