__author__ = 'qtahuy'

import threading
import time
from flask import jsonify
from model import tvpk_model
from entity import channel


class ThreadingBackground(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        while True:
            print(self.GetAllTVChannel())
            time.sleep(3600)

    def GetAllTVChannel(self):
        listChannel = []
        channel_fetch = tvpk_model.SelectDB("channels")
        for chn in channel_fetch:
            listChannel.append(channel.Channel(channel_fetch[0], channel_fetch[1], channel_fetch[2], channel_fetch[3],
                                               channel_fetch[4], channel_fetch[5]))
        return listChannel
