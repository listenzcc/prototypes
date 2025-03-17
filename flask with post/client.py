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
    sys.exit(0)
