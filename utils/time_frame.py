from enum import Enum


class TimeFrame(Enum):
    DAILY = 'daily'
    HOURLY = 'hourly'

    def __str__(self):
        return self.value
