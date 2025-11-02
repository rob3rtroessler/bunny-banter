import os
from flask import Flask, jsonify, render_template, send_from_directory
import logging
from databricks import sql

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

    connection = sql.connect(
                            server_hostname = "dbc-7690628f-7dcc.cloud.databricks.com",
                            http_path = "/sql/1.0/warehouses/68465fc5226f9e55",
                            access_token = "dapi61a56a7892441acd0ec726b0a75cab7a")

    cursor = connection.cursor()
    query = "select * from google_drive.emails_sent"
    cursor.execute(query)
    df = cursor.fetchall_arrow().to_pandas()
    data = df.to_dict(orient='records')
    return jsonify(data)
    cursor.close()
    connection.close()

# ... (Running the app part - host and port setup) ...
if __name__ == '__main__':
    host = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_RUN_PORT", 8080))
    print(f"Flask app starting on {host}:{port}")
    flask_app.run(debug=True, host=host, port=port)



# import pandas as pd
# from flask import Flask, jsonify, render_template, send_from_directory
# from databricks.sdk.core import Config

# import logging
# import os
# from databricks import sql # Assuming you still want to fetch from a SQL Warehouse for production data

# # Suppress Werkzeug logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)



# cfg = Config() # Set the DATABRICKS_HOST environment variable when running locally








# # from databricks.sdk.core import Config

# # client_id = os.getenv('DATABRICKS_CLIENT_ID')
# # client_secret = os.getenv('DATABRICKS_CLIENT_SECRET')

# # cfg = Config()

# # conn = sql.connect(
# #     server_hostname=cfg.host,
# #     http_path="<your-warehouse-http-path>",
# #     credentials_provider=lambda: cfg.authenticate,
# # )




# # Initialize Flask app
# # IMPORTANT: When running on Databricks, ensure paths are relative to where the app is executed
# # or use absolute paths for static/templates if necessary (e.g., from DBFS)
# # For simplicity, assuming 'static' and 'templates' are relative to app.py
# flask_app = Flask(__name__,
#                   static_folder='static',
#                   template_folder='templates') # If you had Jinja2 templates

# # --- Databricks Connection Details (if fetching from SQL Warehouse) ---
# # These would still need to be securely configured, e.g., via environment variables
# # set in the Databricks environment or secrets.
# DATABRICKS_HOST = os.environ.get("DATABRICKS_HOST")
# DATABRICKS_HTTP_PATH = os.environ.get("DATABRICKS_HTTP_PATH")
# DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN")


# server_hostname=cfg.host,
# http_path='https://argus-flask-295280278921608.aws.databricksapps.com'

# # ,
# # credentials_provider=lambda: cfg.authenticate

# # --- Routes ---

# # Route to serve the main HTML page
# @flask_app.route('/')
# def serve_index():
#     # Flask will automatically look for 'index.html' in the 'static' folder
#     # because static_folder='static' was specified during Flask app initialization.
#     # Alternatively, if you put index.html in 'templates', you would use render_template('index.html')
#     return send_from_directory(flask_app.static_folder, 'index.html')

# # Route for your D3.js data API
# @flask_app.route('/api/data')
# def get_data():
#     try:
#         # Example: Fetching from an in-memory DataFrame (for simple demo)
#         # For real data, connect to Databricks SQL Warehouse as previously discussed
#         # Or, query a Delta table directly using Spark if app runs in a Databricks Notebook/Job
#         chart_data = pd.DataFrame({
#             'category': ['A', 'B', 'C', 'D', 'E'],
#             'value': [100, 150, 200, 120, 180]
#         })
#         data = chart_data.to_dict(orient='records')



#         cfg = Config()

#         # conn = sql.connect(
#         #     server_hostname=cfg.host,
#         #     http_path="/sql/1.0/warehouses/68465fc5226f9e55",
#         #     credentials_provider=lambda: cfg.authenticate,
#         # )

#         # query = "select * from google_drive.emails_sent"

#         # with conn.cursor() as cursor:
#         #     cursor.execute(query)
#         #     df = cursor.fetchall_arrow().to_pandas()
#         #     data = df.to_dict(orient='records')
#         #     return jsonify(data)

#         # conn.close()

#         my_data = {
#             "host" : DATABRICKS_HOST,
#             "http_path" : "/sql/1.0/warehouses/68465fc5226f9e55",
#             "token" : DATABRICKS_TOKEN,
#             "client_id": os.getenv('DATABRICKS_CLIENT_ID'),
#             "client_secret": os.getenv('DATABRICKS_CLIENT_SECRET'),
#             "server_hostname": cfg.host,
#         }
#         return jsonify(my_data)
    

#         # --- OR ---
#         # Fetch data from Databricks SQL Warehouse:
#         if DATABRICKS_HOST and DATABRICKS_HTTP_PATH and DATABRICKS_TOKEN:
#             with sql.connect(
#                 server_hostname=DATABRICKS_HOST,
#                 http_path=DATABRICKS_HTTP_PATH,
#                 access_token=DATABRICKS_TOKEN
#             ) as connection:
#                 with connection.cursor() as cursor:
#                     cursor.execute("select * from google_drive.emails_sent")
#                     result = cursor.fetchall()
#                     data = [{"category": row[0], "value": row[1]} for row in result]
#         else:
#             # Fallback or error if Databricks connection details are missing
#             return jsonify({"error": "Databricks connection not configured{DATABRICKS_HOST}, {DATABRICKS_HTTP_PATH}, {DATABRICKS_TOKEN}"}), 500

#         return jsonify(data)
#     except Exception as e:
#         print(f"Error fetching data: {e}")
#         return jsonify(
#             {
#                 "error": "Failed to fetch data", 
#                 "details": str(e)
#             }), 500

# # --- Running the App ---
# # This part is crucial for how Databricks will run your app.
# # When deployed as a Lakehouse App, Databricks provides the port and host.
# if __name__ == '__main__':
#     # Use environment variables provided by Databricks for the host/port
#     host = os.environ.get("FLASK_RUN_HOST", "0.0.0.0") # Default to 0.0.0.0 for container/VM exposure
#     port = int(os.environ.get("FLASK_RUN_PORT", 8080)) # Use a common port or one specified by DB

#     print(f"Flask app starting on {host}:{port}")
#     flask_app.run(debug=True, host=host, port=port)


# # import pandas as pd
# # from flask import Flask
# # import logging

# # log = logging.getLogger('werkzeug')
# # log.setLevel(logging.ERROR)

# # flask_app = Flask(__name__)

# # @flask_app.route('/')
# # def hello_world():
# #     chart_data = pd.DataFrame({'Apps': [x for x in range(30)],
# #                                'Fun with data': [2 ** x for x in range(30)]})
# #     return f'<h1>Hello, World!</h1> {chart_data.to_html(index=False)}'

# # if __name__ == '__main__':
# #     flask_app.run(debug=True)
