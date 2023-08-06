import datetime
import numpy as np 
import pandas as pd 
import pytz
from utils import constants
from queue import Queue,Empty

class EventEngine(object):
    def __init__(self):
        self.__queue=Queue()
        self.__isactive=False


    def get(self)->Event:
        return self.__queue.get(block=False)

    def put(self,event:Event):
        self.__queue.put(event)
    
    def is_empty(self):
        return self.__queue.empty()
