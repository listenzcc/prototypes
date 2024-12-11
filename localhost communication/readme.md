# Localhost communication prototype

The demo establishes server and client via the TCP connection.

## Client

The client handles the camera, and starts the cv2 image window to show it.
It also translates the frames to the server.

## Server

The server receives the frames and also starts the cv2 image window to show the stream.

## Usage

*Make sure* you start the server firstly and then start the client.
And the server and client are running in the *separated* terminals.

```shell

# 1st. In terminal 1. Start the server
python server.py

# 2nd. In terminal 2. Start the client
python client.py
```
