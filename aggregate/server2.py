"""
Simple Socket server listening on [127.0.0.1]:[port number].
Takes in port number as command line argument.
When specifying port number it is recommended to use a number having atleast 4 digits to avoid conflict with
the port number of system processes, because the lower value port number are used by system processes.
It handles only one connection at a time.Sends out sample sensor data of vehicle speed consists of three fields delimited
by comma(,).Each field represents eventTime, speed and deviceId respectively.
This script serves the data for aggregate.py script to run.
"""


import sys
import random
import socket
import time
from datetime import datetime

if __name__ == "__main__":
    port = int(sys.argv[1])
    host = '127.0.0.1'

    print("Starting server")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print("connected by ", addr)
            while True:
                low = f"{random.uniform(10, 30):.5f}"
                mid = f"{random.uniform(30, 60):.5f}"
                high = f"{random.uniform(60, 90):.5f}"
                top = f"{random.uniform(90, 150):.5f}"
                conn.sendall((",".join([str(datetime.now()), low, f"sensor{random.randint(1, 10)}", "\n"])).encode())
                conn.sendall((",".join([str(datetime.now()), mid, f"sensor{random.randint(1, 10)}", "\n"])).encode())
                conn.sendall((",".join([str(datetime.now()), high, f"sensor{random.randint(1, 10)}", "\n"])).encode())
                conn.sendall((",".join([str(datetime.now()), top, f"sensor{random.randint(1, 10)}", "\n"])).encode())

                time.sleep(4)
