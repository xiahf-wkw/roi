import random
import time
def create_random_id():
    return str(random.random()*10000000000000).replace(".","")[0:10]

def create_long_time():
    timestamp = (int(round(time.time())))
    return str(timestamp)