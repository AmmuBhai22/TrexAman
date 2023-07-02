from flask import Flask, make_response,request
#import requests,time,hashlib,hmac,json
#from uuid import uuid4
import pycurl
#import base64 as base
app = Flask(__name__)
def reqcurl(username, password, host, port, target_url='http://api.ipify.org/'):
    buffer = BytesIO()
    c = pycurl.Curl()

    c.setopt(pycurl.CAINFO, certifi.where())

    # set proxy-insecure
    c.setopt(c.PROXY_SSL_VERIFYHOST, 0)
    c.setopt(c.PROXY_SSL_VERIFYPEER, 0)

    # set headers
    c.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:8.0) Gecko/20100101 Firefox/8.0')

    # set proxy
    c.setopt(pycurl.PROXY, f"http://{host}:{port}")

    # proxy auth
    c.setopt(pycurl.PROXYUSERNAME, username)

    # set proxy type = "HTTPS"
    #c.setopt(pycurl.PROXYTYPE, 2)

    # target url
    c.setopt(c.URL, target_url)

    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    return body






@app.route("/")
def index():
  response = reqcurl("", "", "117.251.103.186", "8080").decode()
  return response

app.run()
