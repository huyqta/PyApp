__author__ = 'qtahuy'

from flask import Flask, jsonify, request
import urllib

app = Flask(__name__)


def api_get_stream_from_url(url=None):
    ret_url = ""
    ret_url = urllib.urlopen(url)
    return ret_url