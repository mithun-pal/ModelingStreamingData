"""
Receive text data from a data server 127.0.0.1:[port number], listening on a TCP socket.Takes in the same port number
as command line argument passed to server3.py script. Run server3.py before executing this script.

Split each line of text on comma(,) to give the proper schema structure.
Perform grouping and aggregation with watermark, on the data and displays the results on console.
It also uses checkpoint location for fault tolerance.
"""


import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import split, window

if __name__ == "__main__":
    port = int(sys.argv[1])
    host = '127.0.0.1'

    spark = SparkSession\
         .builder\
         .appName("SpeedTest")\
         .getOrCreate()

    lines = spark\
          .readStream\
          .format("socket")\
          .option("host", host)\
          .option("port", port)\
          .load()

    CSVdata = lines.select(split(lines.value, ",").getItem(0).alias("eventTime").cast("timestamp"),\
                           split(lines.value, ",").getItem(1).alias("speed").cast("int"),\
                           split(lines.value, ",").getItem(2).alias("deviceId"),\
                           )


    speedByDeviceAndTime = CSVdata\
                       .withWatermark("eventTime", "10 minutes")\
                       .groupBy("deviceId", window("eventTime", "2 minutes","2 minutes"))\
                       .avg("speed")


    query = speedByDeviceAndTime\
           .writeStream\
           .outputMode("update")\
           .option("truncate","false")\
           .option("checkpointlocation","hdfs://checkpoint/streaming/spark/overspeed_app")\
           .format("console")\
           .start()

    query.awaitTermination()
