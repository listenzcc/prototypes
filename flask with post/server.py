# %%
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)
# %%
# Routines


@app.route('/echo-post', methods=['POST'])
def _echo_post():
    '''Echo the data with status code of success.'''
    data = request.get_json()
    print(f"Received data: {data}")
    return jsonify({"status": "success", "data": data}), 200


# %%
if __name__ == "__main__":
    # Main entry point for debug.
    # Use run_wsgi.ps1 for production usage.
    host = 'localhost'
    port = 5000
    sys.exit(app.run(host=host, port=port, debug=True))
