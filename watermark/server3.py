"""
Simple Socket server listening on [127.0.0.1]:[port number].
Takes in port number as command line argument.
When specifying port number it is recommended to use a number having atleast 4 digits to avoid conflict with
the port number of system processes, because the lower value port number are used by system processes.
It handles only one connection at a time.Sends out sample sensor data of vehicle speed consists of three fields delimited by comma(,).
Event Time for Some of the records are subtracted by certain unit to demonstrate the late arrival of data.
Each field represents evenTime, speed and deviceId respectively.
This script serves the data for watermark.py script to run.
"""


import sys
import random
import socket
import time
from datetime import datetime, timedelta

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
                mid_speed = round(random.uniform(40, 70), 3)
                high_speed = round(random.uniform(70, 150), 3)
                conn.sendall((str(datetime.now()) + "," + str(mid_speed) + ",current\n").encode())
                conn.sendall((str(datetime.now() - timedelta(minutes=20)) + "," + str(mid_speed) + ",late\n").encode())
                conn.sendall((str(datetime.now() - timedelta(hours=4)) + "," + str(high_speed) + ",expired\n").encode())

                time.sleep(4)
