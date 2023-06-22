#from flask import Flask, jsonify
#import os

from flask import Flask, make_response,request
import requests
import os
app = Flask(__name__)
@app.route("/")
def credit():
    return "Made By AmmuBhai22"
@app.route("/token")
def token():
    url="http://tv.trexiptv.com/server/load.php?type=stb&action=handshake&token=&JsHttpRequest=1-xml"
    headers={"User-Agent":"Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3","X-User-Agent":"Model: MAG250; Link: WiFi","Referer":"http://tv.trexiptv.com/c/","Cookie":"mac=00:1A:79:5A:1C:B8; stb_lang=en; timezone=GMT","Accept":"*/*","Host":"tv.trexiptv.com","Connection":"Keep-Alive","Accept-Encoding":"gzip"}
    data=requests.get(url,headers=headers).json()
    return data["js"]["token"]


@app.route("/json")
def jso():
    url="http://tv.trexiptv.com/portal.php?type=itv&action=get_all_channels&force_ch_link_check=&JsHttpRequest=1-xml"
    token=requests.get(request.base_url.replace("/json","/token")).text
    headers={"User-Agent":"Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3","X-User-Agent":"Model: MAG250; Link: WiFi","Referer":"http://tv.trexiptv.com/c/","Cookie":"mac=00:1A:79:5A:1C:B8; stb_lang=en; timezone=GMT","Accept":"*/*","Host":"tv.trexiptv.com","Connection":"Keep-Alive","Accept-Encoding":"gzip","Authorization":"Bearer "+str(token)}
    data=requests.get(url,headers=headers).json()
    #fin={}
    js={"type": "list","headline": "Videos","template": {"tag": "Web","type": "separate","layout": "0,0,2,4","icon": "live-tv", "color": "msx-glass"}}
    dt=[]
    #for i in range(0,len(data)):
    for dota in data["js"]["data"]:
        if dota["tv_genre_id"]=="127":
            dt.append({"title":dota["name"],"playerLabel":dota["name"],"action":"video:plugin:http://msx.benzac.de/plugins/hls.html?url="+request.base_url.replace("/json","/m3u8/")+dota["cmd"].replace("ffmpeg ","").replace("?","piyush").replace("&","aman").replace("http://","http:/")})
        js["items"]=dt
    final=make_response(js)
    final.headers["Content-Type"] = "application/json; charset=utf-8"
    final.headers["Access-Control-Allow-Origin"]="*"
    final.headers["Access-Control-Allow-Headers"]="Origin, Content-Type, Accept"
    final.headers["Access-Control-Allow-Methods"]="GET, OPTIONS"
    return final

@app.route("/m3u8/<path:link>")
def playlist(link):
    req=requests.get( link.replace("aman","&").replace("piyush","?").replace("extension=ts","extension=m3u8").replace(".com:80",".com").replace("http:/","http://").replace("&.m3u8",""))#
    link=req.url.split("/live/")[0].replace("http://","http:/")#
    data=req.text.replace("/hls/","/hls/"+link+"/hls/")#
    #lank=link.strip("/")
    #return data.replace("/hls/",f"/hls/{link[7:27]}/hls/")
    final=make_response(data)
    final.headers["Content-Type"] = "application/vnd.apple.mpegurl"
    final.headers["Access-Control-Allow-Origin"]="*"
    final.headers["Access-Control-Allow-Headers"]="Origin, Content-Type, Accept"
    final.headers["Access-Control-Allow-Methods"]="GET, OPTIONS"
    return final

@app.route("/hls/<path:ts>")
def tss(ts):
    ts=ts.replace("http:/","http://")#
    final=make_response(requests.get(ts).content)#yahan text nhi content dete hai kyunki text mei utf-8 encided ts atta hai aur work nhi krta yehi Maine toffee nei Kiya tha 
    final.headers["Content-Type"] = "application/octet-stream"#
    final.headers["Access-Control-Allow-Origin"]="*"
    final.headers["Access-Control-Allow-Headers"]="Origin, Content-Type, Accept"
    final.headers["Access-Control-Allow-Methods"]="GET, OPTIONS"
    return final

@app.route("/m3u")
def m3u():
	url="http://tv.trexiptv.com/portal.php?type=itv&action=get_all_channels&force_ch_link_check=&JsHttpRequest=1-xml"
	tok=requests.get(request.base_url.replace("/json","/token")).text
	headers={"User-Agent":"Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3","X-User-Agent":"Model: MAG250; Link: WiFi","Referer":"http://tv.trexiptv.com/c/","Cookie":"mac=00:1A:79:5A:1C:B8; stb_lang=en; timezone=GMT","Accept":"*/*","Host":"tv.trexiptv.com","Connection":"Keep-Alive","Accept-Encoding":"gzip","Authorization":"Bearer "+str(tok)}
	data=requests.get(url,headers=headers).json()
	final="#EXTM3U"
	"""
	for i in data["js"]["data"]:
	   		if i["tv_genre_id"]=="127":
	   			final=final+"\n#EXTINF:-1,"+i["name"]++request.base_url.replace("/m3u","/m3u8/")+dota["cmd"].replace("ffmpeg ","").replace("?","piyush").replace("&","aman").replace("http://","http:/")"""
	return final
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
