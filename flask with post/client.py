# %%
import sys
import requests

# %%


class MyRequest:
    scheme = 'http'
    hostname = 'localhost:5000'

    def post(self, path: str, body: dict) -> requests.Response:
        '''
        Send the post request to the server.

        :param path str: the path to the post request.
        :param body dict: the body of the post request.
        :returns response requests.Response: the response.
        '''
        url = f'{self.scheme}://{self.hostname}/{path}'
        response = requests.post(url, json=body)
        return response

    def post_event_stream(self, path: str):
        '''
        Connect to the stream endpoint and print messages.

        :param path str: the path to the stream endpoint.
        '''
        url = f'{self.scheme}://{self.hostname}/{path}'
        with requests.post(url, stream=True, json={}) as response:
            for line in response.iter_lines():
                if line:
                    print(f"Received Chunk: {line.decode('utf-8')}")


# %%
if __name__ == '__main__':
    # Make the request object.
    # Send the post request to the server.
    mr = MyRequest()

    body = {
        'key1': 'value1',
        'key2': 'value2'
    }

    resp = mr.post('echo-post', body)
    print(f'Status Code: {resp.status_code}')
    print(f'Response JSON: {resp.json()}')

    print("Stream starts, listening for messages...")
    mr.post_event_stream('demo-event-stream')
    sys.exit(0)
