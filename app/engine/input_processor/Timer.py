import time

class Timer:
    def __init__(self):
        self.__last_timestamp = int(time.time() * 1000)
        self.__delta_time = 0

    def tick(self):
        current_timestamp = int(time.time() * 1000)
        self.__delta_time = current_timestamp - self.__last_timestamp
        self.__last_timestamp = current_timestamp

    @property
    def delta_time(self):
        return self.__delta_time

    @property
    def last_timestamp(self):
        return self.__last_timestamp

    @staticmethod
    def current_timestamp():
        return int(time.time() * 1000)
