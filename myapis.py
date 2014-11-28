__author__ = 'qtahuy'

from flask import Flask, jsonify, request
import urllib2
import re

app = Flask(__name__)


def api_get_stream_from_url(url=None):
    try:
        resp = urllib2.urlopen(url)
        contents = resp.read()
        if url.find("xemphimso.com") > -1:
            matchObj = re.search("(file: ').*(',type)", contents)
            if matchObj:
                last_url = matchObj.group().replace("file: '", "").replace("',type", "")
                return last_url

        elif url.find("www.tivi24h.com") > -1:
            matchObj = re.search("(var responseText = ).*(;)", contents)
            if matchObj:
                last_url = matchObj.group().replace('var responseText = "', '').replace('";', '')
                return last_url

        elif url.find("tv.tivi24h.com") > -1:
            matchObj = re.search("(var responseText = ).*(;)", contents)
            if matchObj:
                last_url = matchObj.group().replace('file: "', '').replace('",image:', '').replace('";', '')
                return last_url

            matchObj = re.search("(var responseText = ).*(;)", contents)
            if matchObj:
                last_url = matchObj.group().replace('file: "', '').replace('",image:', '').replace('";', '')
                return last_url

        elif url.find("tivi360") > -1:
            matchObj = re.search("(var responseText = ).*(;)", contents)
            if matchObj:
                last_url = matchObj.group().replace('var responseText = "', '').replace('";', '')
                return last_url

        elif url.find("htvonline") > -1:
            matchObj = re.search('(file: ").*(",)', contents)
            if matchObj:
                last_url = matchObj.group().replace('file: "', '').replace('",', '')
                return last_url

        return contents
    except urllib2.HTTPError, error:
        contents = error.read()
        return contents