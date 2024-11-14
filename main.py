import json
import requests
import urllib.parse
import time
import datetime
import random
import os
import subprocess
from cache import cache

# Torのプロキシ設定
#proxies = {
#    'http': 'socks5h://127.0.0.1:9050',
#    'https': 'socks5h://127.0.0.1:9050'
#}
#apis = [r"https://inv.nadeko.net/", r"https://inv.nadekonw7plitnhuawu6ytjsl7jlglk2t6pyq6eftptmiv3dvqndwvyd.onion", r"https://nerdvpneaggggfdiurknszkbmhvjndks5z5k3g5yp4nhphflh3n3boad.onion", r"http://zzlsbhhfvwg3oh36tcvx4r7n6jrw7zibvyvfxqlodcwn3mfrvzuq.b32.i2p"]

max_api_wait_time = 3
max_time = 10
apis = [r"https://youtube.privacyplz.org/", r"https://inv.nadeko.net/"]
#, r"http://invidious.materialio.us/",r"http://invidious.perennialte.ch/",r"http://yewtu.be/",r"https://iv.datura.network/",r"https://invidious.private.coffee/",r"https://invidious.protokolla.fi/",r"https://invidious.perennialte.ch/",r"https://yt.cdaut.de/",r"https://invidious.materialio.us/",r"https://yewtu.be/",r"https://invidious.fdn.fr/",r"https://inv.tux.pizza/",r"https://invidious.privacyredirect.com/",r"https://invidious.drgns.space/",r"https://vid.puffyan.us",r"https://invidious.jing.rocks/",r"https://youtube.076.ne.jp/",r"https://vid.puffyan.us/",r"https://inv.riverside.rocks/",r"https://invidio.xamh.de/",r"https://y.com.sb/",r"https://invidious.sethforprivacy.com/",r"https://invidious.tiekoetter.com/",r"https://inv.bp.projectsegfau.lt/",r"https://inv.vern.cc/",r"https://invidious.nerdvpn.de/",r"https://inv.privacy.com.de/",r"https://invidious.rhyshl.live/",r"https://invidious.slipfox.xyz/",r"https://invidious.weblibre.org/",r"https://invidious.namazso.eu/",r"https://invidious.jing.rocks", r"https://proxied.yt/", r"https://invidious.nl/", r"https://invidious.rocks/", r"https://www.youtube.com/", r"https://m.youtube.com/" r"https://www.youtube.com/embed/", r"https://invidious.nerdvpn.de/", r"https://inv.nadeko.net/", r"https://invidious.jing.rocks/", r"https://googlevideo.com/videoplayback/", r"https://s.ytimg.com",r"https://i.ytimg.com", r"https://yt3.ggpht.com", r"https://invidious.ethibox.fr/"
#いれたければどうぞ
url = requests.get(r'https://raw.githubusercontent.com/mochidukiyukimi/yuki-youtube-instance/main/instance.txt').text.rstrip()
version = "1.0"

os.system("chmod 777 ./yukiverify")

# .onionおよび.i2pアドレスにリクエスト
#for api in apis:
#    try:
#        response = requests.get(api, proxies=proxies, timeout=max_time)
#        print(f"Response from {api}: {response.text}")
#    except requests.exceptions.RequestException as e:
#        print(f"Error with {api}: {e}")


apichannels = []
apicomments = []
[[apichannels.append(i),apicomments.append(i)] for i in apis]
class APItimeoutError(Exception):
    pass

def is_json(json_str):
    result = False
    try:
        json.loads(json_str)
        result = True
    except json.JSONDecodeError as jde:
        pass
    return result

def apirequest(url):
    global apis
    global max_time
    starttime = time.time()
    for api in apis:
        if  time.time() - starttime >= max_time -1:
            break
        try:
            res = requests.get(api+url,timeout=max_api_wait_time)
            if res.status_code == 200 and is_json(res.text):
                return res.text
            else:
                print(f"エラー:{api}")
                apis.append(api)
                apis.remove(api)
        except:
            print(f"タイムアウト:{api}")
            apis.append(api)
            apis.remove(api)
    raise APItimeoutError("APIがタイムアウトしました")

def apichannelrequest(url):
    global apichannels
    global max_time
    starttime = time.time()
    for api in apichannels:
        if  time.time() - starttime >= max_time -1:
            break
        try:
            res = requests.get(api+url,timeout=max_api_wait_time)
            if res.status_code == 200 and is_json(res.text):
                return res.text
            else:
                print(f"エラー:{api}")
                apichannels.append(api)
                apichannels.remove(api)
        except:
            print(f"タイムアウト:{api}")
            apichannels.append(api)
            apichannels.remove(api)
    raise APItimeoutError("APIがタイムアウトしました")

def apicommentsrequest(url):
    global apicomments
    global max_time
    starttime = time.time()
    for api in apicomments:
        if  time.time() - starttime >= max_time -1:
            break
        try:
            res = requests.get(api+url,timeout=max_api_wait_time)
            if res.status_code == 200 and is_json(res.text):
                return res.text
            else:
                print(f"エラー:{api}")
                apicomments.append(api)
                apicomments.remove(api)
        except:
            print(f"タイムアウト:{api}")
            apicomments.append(api)
            apicomments.remove(api)
    raise APItimeoutError("APIがタイムアウトしました")


def get_info(request):
    global version
    return json.dumps([version,os.environ.get('RENDER_EXTERNAL_URL'),str(request.scope["headers"]),str(request.scope['router'])[39:-2]])

def get_data(videoid):
    global logs
    t = json.loads(apirequest(r"api/v1/videos/"+ urllib.parse.quote(videoid)))
    return [{"id":i["videoId"],"title":i["title"],"authorId":i["authorId"],"author":i["author"]} for i in t["recommendedVideos"]],list(reversed([i["url"] for i in t["formatStreams"]]))[:2],t["descriptionHtml"].replace("\n","<br>"),t["title"],t["authorId"],t["author"],t["authorThumbnails"][-1]["url"]

def get_search(q,page):
    global logs
    t = json.loads(apirequest(fr"api/v1/search?q={urllib.parse.quote(q)}&page={page}&hl=jp"))
    def load_search(i):
        if i["type"] == "video":
            return {"title":i["title"],"id":i["videoId"],"authorId":i["authorId"],"author":i["author"],"length":str(datetime.timedelta(seconds=i["lengthSeconds"])),"published":i["publishedText"],"type":"video"}
        elif i["type"] == "playlist":
            return {"title":i["title"],"id":i["playlistId"],"thumbnail":i["videos"][0]["videoId"],"count":i["videoCount"],"type":"playlist"}
        else:
            if i["authorThumbnails"][-1]["url"].startswith("https"):
                return {"author":i["author"],"id":i["authorId"],"thumbnail":i["authorThumbnails"][-1]["url"],"type":"channel"}
            else:
                return {"author":i["author"],"id":i["authorId"],"thumbnail":r"https://"+i["authorThumbnails"][-1]["url"],"type":"channel"}
    return [load_search(i) for i in t]

def get_channel(channelid):
    global apichannels
    t = json.loads(apichannelrequest(r"api/v1/channels/"+ urllib.parse.quote(channelid)))
    if t["latestVideos"] == []:
        print("APIがチャンネルを返しませんでした")
        apichannels.append(apichannels[0])
        apichannels.remove(apichannels[0])
        raise APItimeoutError("APIがチャンネルを返しませんでした")
    return [[{"title":i["title"],"id":i["videoId"],"authorId":t["authorId"],"author":t["author"],"published":i["publishedText"],"type":"video"} for i in t["latestVideos"]],{"channelname":t["author"],"channelicon":t["authorThumbnails"][-1]["url"],"channelprofile":t["descriptionHtml"]}]

def get_playlist(listid,page):
    t = json.loads(apirequest(r"/api/v1/playlists/"+ urllib.parse.quote(listid)+"?page="+urllib.parse.quote(page)))["videos"]
    return [{"title":i["title"],"id":i["videoId"],"authorId":i["authorId"],"author":i["author"],"type":"video"} for i in t]

def get_comments(videoid):
    t = json.loads(apicommentsrequest(r"api/v1/comments/"+ urllib.parse.quote(videoid)+"?hl=jp"))["comments"]
    return [{"author":i["author"],"authoricon":i["authorThumbnails"][-1]["url"],"authorid":i["authorId"],"body":i["contentHtml"].replace("\n","<br>")} for i in t]

def get_replies(videoid,key):
    t = json.loads(apicommentsrequest(fr"api/v1/comments/{videoid}?hmac_key={key}&hl=jp&format=html"))["contentHtml"]

def get_level(word):
    for i1 in range(1,13):
        with open(f'Level{i1}.txt', 'r', encoding='UTF-8', newline='\n') as f:
            if word in [i2.rstrip("\r\n") for i2 in f.readlines()]:
                return i1
    return 0




from fastapi import FastAPI, Depends
from fastapi import Response,Cookie,Request
from fastapi.responses import HTMLResponse,PlainTextResponse
from fastapi.responses import RedirectResponse as redirect
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Union
from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/css", StaticFiles(directory="./css"), name="static")
app.mount("/word", StaticFiles(directory="./blog", html=True), name="static")
app.mount("/privacy", StaticFiles(directory="./privacy", html=True), name="static")
app.mount("/", StaticFiles(directory="./pass", html=True), name="static")
app.mount("/contact", StaticFiles(directory="./contact", html=True), name="static")
app.mount("/sitemap", StaticFiles(directory="./sitemap", html=True), name="static")
app.mount("/use", StaticFiles(directory="./use", html=True), name="static")
app.mount("/invidious", StaticFiles(directory="./invidious", html=True), name="static")
app.mount("/requestform", StaticFiles(directory="./requestform", html=True), name="static")
app.add_middleware(GZipMiddleware, minimum_size=1000)
from fastapi.templating import Jinja2Templates
template = Jinja2Templates(directory='templates').TemplateResponse






@app.get("/home", response_class=HTMLResponse)
def home(response: Response,request: Request,yuki: Union[str] = Cookie(None)):
    if check_cokie(yuki):
        response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
        return template("home.html",{"request": request})
    print(check_cokie(yuki))
    return redirect("/")

@app.get('/watch', response_class=HTMLResponse)
def video(v:str,response: Response,request: Request,yuki: Union[str] = Cookie(None),proxy: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return redirect("/")
    response.set_cookie(key="yuki", value="True",max_age=7*24*60*60)
    videoid = v
    t = get_data(videoid)
    response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
    return template('video.html', {"request": request,"videoid":videoid,"videourls":t[1],"res":t[0],"description":t[2],"videotitle":t[3],"authorid":t[4],"authoricon":t[6],"author":t[5],"proxy":proxy})

@app.get("/search", response_class=HTMLResponse,)
def search(q:str,response: Response,request: Request,page:Union[int,None]=1,yuki: Union[str] = Cookie(None),proxy: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return redirect("/")
    response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
    return template("search.html", {"request": request,"results":get_search(q,page),"word":q,"next":f"/search?q={q}&page={page + 1}","proxy":proxy})

@app.get("/hashtag/{tag}")
def search(tag:str,response: Response,request: Request,page:Union[int,None]=1,yuki: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return redirect("/")
    return redirect(f"/search?q={tag}")


@app.get("/channel/{channelid}", response_class=HTMLResponse)
def channel(channelid:str,response: Response,request: Request,yuki: Union[str] = Cookie(None),proxy: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return redirect("/")
    response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
    t = get_channel(channelid)
    return template("channel.html", {"request": request,"results":t[0],"channelname":t[1]["channelname"],"channelicon":t[1]["channelicon"],"channelprofile":t[1]["channelprofile"],"proxy":proxy})

@app.get("/answer", response_class=HTMLResponse)
def set_cokie(q:str):
    t = get_level(q)
    if t > 5:
        return f"level{t}\n推測を推奨する"
    elif t == 0:
        return "level12以上\nほぼ推測必須"
    return f"level{t}\n覚えておきたいレベル"

@app.get("/playlist", response_class=HTMLResponse)
def playlist(list:str,response: Response,request: Request,page:Union[int,None]=1,yuki: Union[str] = Cookie(None),proxy: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return redirect("/")
    response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
    return template("search.html", {"request": request,"results":get_playlist(list,str(page)),"word":"","next":f"/playlist?list={list}","proxy":proxy})

@app.get("/info", response_class=HTMLResponse)
def viewlist(response: Response,request: Request,yuki: Union[str] = Cookie(None)):
    global apis,apichannels,apicomments
    if not(check_cokie(yuki)):
        return redirect("/")
    response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
    return template("info.html",{"request": request,"Youtube_API":apis[0],"Channel_API":apichannels[0],"Comments_API":apicomments[0]})

@app.get("/suggest")
def suggest(keyword:str):
    return [i[0] for i in json.loads(requests.get(r"http://www.google.com/complete/search?client=youtube&hl=ja&ds=yt&q="+urllib.parse.quote(keyword)).text[19:-1])[1]]

@app.get("/comments")
def comments(request: Request,v:str):
    return template("comments.html",{"request": request,"comments":get_comments(v)})

@app.get("/thumbnail")
def thumbnail(v:str):
    return Response(content = requests.get(fr"https://img.youtube.com/vi/{v}/0.jpg").content,media_type=r"image/jpeg")

@app.get("/bbs",response_class=HTMLResponse)
def view_bbs(request: Request,name: Union[str, None] = "",seed:Union[str,None]="",channel:Union[str,None]="main",verify:Union[str,None]="false",yuki: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return redirect("/")
    res = HTMLResponse(requests.get(fr"{url}bbs?name={urllib.parse.quote(name)}&seed={urllib.parse.quote(seed)}&channel={urllib.parse.quote(channel)}&verify={urllib.parse.quote(verify)}",cookies={"yuki":"True"}).text)
    return res

@cache(seconds=5)
def bbsapi_cached(verify,channel):
    return requests.get(fr"{url}bbs/api?t={urllib.parse.quote(str(int(time.time()*1000)))}&verify={urllib.parse.quote(verify)}&channel={urllib.parse.quote(channel)}",cookies={"yuki":"True"}).text

@app.get("/bbs/api",response_class=HTMLResponse)
def view_bbs(request: Request,t: str,channel:Union[str,None]="main",verify: Union[str,None] = "false"):
    print(fr"{url}bbs/api?t={urllib.parse.quote(t)}&verify={urllib.parse.quote(verify)}&channel={urllib.parse.quote(channel)}")
    return bbsapi_cached(verify,channel)

@app.get("/bbs/result")
def write_bbs(request: Request,name: str = "",message: str = "",seed:Union[str,None] = "",channel:Union[str,None]="main",verify:Union[str,None]="false",yuki: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return redirect("/")
    t = requests.get(fr"{url}bbs/result?name={urllib.parse.quote(name)}&message={urllib.parse.quote(message)}&seed={urllib.parse.quote(seed)}&channel={urllib.parse.quote(channel)}&verify={urllib.parse.quote(verify)}&info={urllib.parse.quote(get_info(request))}&serververify={get_verifycode()}",cookies={"yuki":"True"}, allow_redirects=False)
    if t.status_code != 307:
        return HTMLResponse(t.text)
    return redirect(f"/bbs?name={urllib.parse.quote(name)}&seed={urllib.parse.quote(seed)}&channel={urllib.parse.quote(channel)}&verify={urllib.parse.quote(verify)}")

@cache(seconds=30)
def how_cached():
    return requests.get(fr"{url}bbs/how").text

@app.get("/bbs/how",response_class=PlainTextResponse)
def view_commonds(request: Request,yuki: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return redirect("/")
    return how_cached()

@app.get("/load_instance")
def home():
    global url
    url = requests.get(r'https://raw.githubusercontent.com/mochidukiyukimi/yuki-youtube-instance/main/instance.txt').text.rstrip()


@app.exception_handler(500)
def page(request: Request,__):
    return template("APIwait.html",{"request": request},status_code=500)

@app.exception_handler(APItimeoutError)
def APIwait(request: Request,exception: APItimeoutError):
    return template("APIwait.html",{"request": request},status_code=500)







#import requests

#API_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiOTFlMjllMmJjMDk1N2Y3M2JjMjBkZTA0MDhkMGFiOTlhYjg1NzQ2ZjNhZmQzNmRiNjBjNzViMDNhZmJjZWM5NDQ5NDIwNTk4YjQ2MWM5NzUiLCJpYXQiOjE3Mjg4NTcwMjIuNTUwNzMxLCJuYmYiOjE3Mjg4NTcwMjIuNTUwNzMzLCJleHAiOjQ4ODQ1MzA2MjIuNTQ1NjI0LCJzdWIiOiI2ODkxODQ1MiIsInNjb3BlcyI6W119.oxtkBhW0eJcRxBKKkPV70EE-tDFBtFY6Pb6xHWrWaR4HM_27iXFEfUftosumRFqRvwn_A6cVfIIoPk3218upcv7yoPlW4-arhQg26XDoR2LZcuEMCFuMkaoUZtyMNY5GmT5_1p0qmIk3eCBTwidc7FqucO_LbhlLwQF0__e64Aoe83oC0Pdh6II4TuWsLEOMstzlaolRbVdt2FNomkjru7_14jp-yjcUqiaHU4YkZiX25cG465ZfCcHb3gSxEadNwPF8ou4v8hI5-HL9IrQ0PHnmTByCEE-JEMY4AhT-fGlXgJ71xm0RQELj8NQpPe4pjhpBILgVcOInOmK2RSib948LjyION8rbKbffTfcOsyhyNFzO7lYGoLA5rJrnLl5Um2QDmzwbHgmtQjXzy9xkliAyf6rTaThlCxAfahm0uCmTMttJ_75rsKihzIUVRtW_PhibY0AAExihhVHIiAPi8oZHUdRZqhOkt7uZTr9P-NfNNHc4eG1eF1nvg2Tx1XQ0oOLUDVrIgxxEx1eD8NC5dowqRls2W_tuSgj6vBMw6A-vM8vMLc0ZXY0aBn0DfqSdK9-iDURa2P15eUTKteQHc9yZ2lxX93CwPyfXfhJZBjo8-0L29orlLaDBauwq0_wN9-crd5fNFdJ52mH9izBjRVY157fcYcb5qPmDq86K_xY'

#def compress_video(video_url):
    # CloudConvert APIを使って動画を圧縮する
   # process_url = 'https://api.cloudconvert.com/v2/jobs'
    #headers = {
        #'Authorization': f'Bearer {API_KEY}',
        #'Content-Type': 'application/json'
    #}

    #data = {
        #"tasks": {
            #'import-my-file': {
                #"operation": 'import/url',
                #"url": video_url
           # },
       #     'convert-my-file': {
        #        "operation": 'convert',
       #         "input": 'import-my-file',
        #        "output_format": 'mp4',
          #      "video_codec": 'h264',
           #     "audio_codec": 'aac',
           #     "quality": '30',
            #    "width": 1280
          #  },
          #  'export-my-file': {
          #      "operation": 'export/url',
           #     "input": 'convert-my-file'
          #  }
       # }
   # }

    # CloudConvertのジョブ作成
   # response = requests.post(process_url, headers=headers, json=data)
   # job_info = response.json()

    # 圧縮された動画のダウンロードリンクを取得
  #  for task in job_info['data']['tasks']:
      #  if task['name'] == 'export-my-file':
          #  download_link = task['result']['files'][0]['url']
   #         return download_link

   # return None

# 動画URLを指定
#video_url = videourls[0]
#compressed_video_url = compress_video(video_url)
#print('圧縮された動画のダウンロードリンク:', compressed_video_url)
