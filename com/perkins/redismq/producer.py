"""
Created by PerkinsZhu on 2023/8/22 13:54
"""
# producer.py
"""
It sends a python dict (producer, some_id, count)
to REDIS STREAM (using the xadd method)

Usage:
  PRODUCER=Roger MESSAGES=10 python producer.py
"""

from os import environ
from redis import Redis
from uuid import uuid4
from time import sleep

stream_key = environ.get("STREAM", "jarless-1")
producer = environ.get("PRODUCER", "user-1")
MAX_MESSAGES = int(environ.get("MESSAGES", "2"))


stream_key = "111"

def connect_to_redis():
    hostname = "111"
    port = 6379
    pw = "111"

    r = Redis(hostname, port, password=pw,retry_on_timeout=True)
    return r


def send_data(redis_connection, max_messages):
    count = 0
    while count < max_messages:
        try:
            data = {
                "producer": producer,
                "some_id": uuid4().hex,  # Just some random data
                "count": count,
            }
            resp = redis_connection.xadd(stream_key, data)
            print(resp)
            count += 1

        except ConnectionError as e:
            print("ERROR REDIS CONNECTION: {}".format(e))

        sleep(0.5)


if __name__ == "__main__":
    connection = connect_to_redis()
    send_data(connection, MAX_MESSAGES)
