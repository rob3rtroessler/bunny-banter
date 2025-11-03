import os
from flask import Flask, jsonify, render_template, send_from_directory
import logging
from databricks import sql
from databricks.sdk.core import Config

# Suppress Werkzeug logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

flask_app = Flask(__name__,
                  static_folder='static',
                  template_folder='templates')

# --- Databricks Connection Details for OAuth ---
# These MUST be securely configured as environment variables
# in the environment where your Flask app is running (e.g., in the Databricks Lakehouse App config,
# or for local testing, set in your terminal/IDE run configuration).
DATABRICKS_HOST = os.environ.get("DATABRICKS_HOST")
DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/68465fc5226f9e55" # os.environ.get("DATABRICKS_HTTP_PATH") # e.g., /sql/1.0/warehouses/xxxxxx
DATABRICKS_CLIENT_ID = os.environ.get("DATABRICKS_CLIENT_ID")       # Application (client) ID of your Service Principal
DATABRICKS_CLIENT_SECRET = os.environ.get("DATABRICKS_CLIENT_SECRET") # Secret Value for your Service Principal

# --- Routes ---

@flask_app.route('/')
def serve_index():
    return send_from_directory(flask_app.static_folder, 'index.html')

@flask_app.route('/api/data')
def get_data():
    # Prepare credentials info to send to client
    credentials_info = {
        "host": "dbc-7690628f-7dcc.cloud.databricks.com",
        "http_path": "/sql/1.0/warehouses/68465fc5226f9e55",
        "client_id": DATABRICKS_CLIENT_ID,
        "client_secret": DATABRICKS_CLIENT_SECRET,
        "databricks_host_env": DATABRICKS_HOST
    }
    
    # Create Config with OAuth credentials (service principal)
    cfg = Config(
        host="dbc-7690628f-7dcc.cloud.databricks.com",
        client_id=DATABRICKS_CLIENT_ID,
        client_secret=DATABRICKS_CLIENT_SECRET
    )
    
    # Use credentials_provider for OAuth authentication
    connection = sql.connect(
        server_hostname="dbc-7690628f-7dcc.cloud.databricks.com",
        http_path="/sql/1.0/warehouses/68465fc5226f9e55",
        credentials_provider=lambda: cfg.authenticate()
    )

    cursor = connection.cursor()
    query = "select * from google_drive.emails_sent"
    cursor.execute(query)
    df = cursor.fetchall_arrow().to_pandas()
    data = df.to_dict(orient='records')
    cursor.close()
    connection.close()
    
    # Return both credentials and data
    return jsonify({
        "credentials": credentials_info,
        "data": data
    })

# ... (Running the app part - host and port setup) ...
if __name__ == '__main__':
    host = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_RUN_PORT", 8080))
    print(f"Flask app starting on {host}:{port}")
    flask_app.run(debug=True, host=host, port=port)