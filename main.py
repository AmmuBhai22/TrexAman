from flask import Flask, make_response,request
import requests,time,hashlib,hmac,json
from uuid import uuid4
import base64 as base
app = Flask(__name__)
@app.route("/")
def index():
	return "Hi Ho Ho"
@app.route("/auth/<string:um>")
def getAuth(um):
    includeST=True
    persona=False
    if um=="t":
    	includeUM=True
    elif um=="f":
    	includeUM=False
    else:
    	return "Fail"
    	exit()
    _AKAMAI_ENCRYPTION_KEY = b'\x05\xfc\x1a\x01\xca\xc9\x4b\xc4\x12\xfc\x53\x12\x07\x75\xf9\xee'
    if persona:
        _AKAMAI_ENCRYPTION_KEY = b"\xa0\xaa\x8b\xcf\x9d\xd5\x8e\xc6\xe3\xb5\x7d\x9b\x4e\x5a\x00\x80\xb1\x45\x0d\xf7\x43\x6c\xfa\x22\xdd\x5c\xff\xdf\xea\x8e\x12\x52"
    st = int(time.time())

    um = '/um/v3' if includeUM else ''
    exp = st + 6000
    auth = 'st=%d~exp=%d~acl=%s/*' % (st, exp,
                                      um) if includeST else 'exp=%d~acl=/*' % exp
    auth += '~hmac=' + hmac.new(_AKAMAI_ENCRYPTION_KEY,
                                auth.encode(), hashlib.sha256).hexdigest()
    return auth
@app.route("/token/<string:dev>")
def guestToken(dev):
    auth=requests.get(request.base_url.replace(f"/token/{dev}","/auth/t")).text
    hdr = {
        'hotstarauth': auth,
        'x-hs-platform': 'firetv',
        'x-country-code': "91",
        'x-hs-appversion': '7.42.0',
        'x-request-id': str(dev),
        'x-hs-device-id': str(dev),
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46'
    }
    data = {
        "device_ids": [{"id": str(dev), "type": "device_id"}],
        "device_meta": {"network_operator": "4g - 4.6 - 50", "os_name": "Windows", "os_version": "10"}
    }
    data = json.dumps(data)

    # data = json.dumps(
    #    {"device_ids": [{"id": str(uuid4()), "type": "device_id"}]}).encode()

    resp = requests.post("https://api.hotstar.com/um/v3/users",
                         data=data, headers=hdr,proxies={"https":"117.251.103.186:8080"}).text

    return resp
@app.route("/headers/<string:dev>/<string:sto>")
def headers(dev,sto):
	includeST=False
	auth=requests.get(request.base_url.replace(f"/headers/{dev}/{sto}","/auth/"+sto)).text
	if auth=="Fail":
		return auth
		exit()
	top=requests.get(request.base_url.replace(f"/headers/{dev}/{sto}","/token/"+dev)).text
	headers = {
            "hotstarauth": auth,
            "x-hs-platform": "firetv",
            "x-hs-appversion": "7.41.0",
            "content-type": "application/json",
            "x-country-code": "IN",
            "x-platform-code": "PCTV",
            "x-hs-usertoken": top,
            "x-hs-request-id": dev,
            "user-agent": "Hotstar;in.startv.hotstar/3.3.0 (Android/8.1.0)",
            # Mozilla/5.0 (Linux; Android 7.0; Redmi Note 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36}
        }
	return headers
@app.route("/param/<string:deviceId>")
def param(deviceId):
	return {
            "device-id": deviceId,
            # "desired-config": "audio_channel:stereo|container:fmp4|dynamic_range:sdr|encryption:%s|ladder:phone|package:dash|resolution:fhd|%svideo_codec:h264" % (encryption, subTag or "")
            "desired-config": "ads:non_ssai|audio_channel:stereo|container:ts|dvr:short|dynamic_range:sdr|encryption:plain|ladder:web|language:hin|package:hls|resolution:fhd|video_codec:h264"
        }
@app.route("/play/<string:con>")
def play(con):
	API_BASE_URL = "https://api.hotstar.com"
	url=API_BASE_URL+"/play/v4/playback/content/"+str(base.b64decode(con))
	dev=str(uuid4())
	head={}
	#head=requests.get(request.base_url.replace(f"/play{con}",f"/headers/{dev}/f")).text
	data = '{"os_name":"Android","os_version":"7.0","app_name":"android","app_version":"7.41.0","platform":"firetv","platform_version":"7.6.0.0","client_capabilities":{"ads":["non_ssai"],"audio_channel":["stereo"],"dvr":["short"],"package":["dash","hls"],"dynamic_range":["sdr"],"video_codec":["h264"],"encryption":["widevine"],"ladder":["phone"],"container":["fmp4","ts"],"resolution":["fhd","hd","sd"]},"drm_parameters":{"widevine_security_level":["SW_SECURE_DECODE","SW_SECURE_CRYPTO"],"hdcp_version":["HDCP_NO_DIGITAL_OUTPUT"]},"resolution":"auto"}'
	par=requests.get(request.base_url.replace(f"/play{con}",f"/param/{dev}"),params={"https":"117.251.103.186:8080"}).text
	data=requests.post(url,headers=head,data=data,params=par)
	return data.json()
app.run()
