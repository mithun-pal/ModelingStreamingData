"""
Receive text data from a data server 127.0.0.1:[port number], listening on a TCP socket.Takes in the same port number
as command line argument passed to server1.py script. Run server1.py before executing this script.

Splits each line of text on comma(,) to give the proper schema structure and displays the fields on console.
"""


import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import split

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

    selectAndFilter = CSVdata.select("eventTime", "speed").where("speed > 60")

    query = selectAndFilter\
          .writeStream\
          .outputMode("append")\
          .format("console")\
          .option("truncate", "false")\
          .start()

    query.awaitTermination()
