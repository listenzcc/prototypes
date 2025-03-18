# %%
import sys
import time
from flask import Flask, Response, request, jsonify

app = Flask(__name__)

# %%
# Routines


@app.route('/echo-post', methods=['POST'])
def _echo_post():
    '''Echo the data with status code of success.'''
    data = request.get_json()
    print(f"Received data: {data}")
    return jsonify({"status": "success", "data": data}), 200


@app.route('/demo-event-stream', methods=['POST'])
def _demo_event_stream():
    '''Send the stream to the caller.'''

    # It is the post request
    request.get_json()

    def eventStream():
        print('EventStream')
        for i in range(3):
            print(i)
            time.sleep(1)
            yield f"Date: {time.ctime()}\n\n"

    return Response(eventStream(), mimetype="text/event-stream")


# %%
if __name__ == "__main__":
    # Main entry point for debug.
    # Use run_wsgi.ps1 for production usage.
    host = 'localhost'
    port = 5000
    sys.exit(app.run(host=host, port=port, debug=True))
