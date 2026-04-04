import requests
import urllib.parse as up
import sys
import subprocess

def _dlm3u8(url,session=None,log=sys.stdout):
        if not session:
                session=requests.Session()
        resdata=bytes()
        res=session.get(url)
        for line in res.text.split("\n"):
                if not line:    #skip empty
                        continue
                if line[0]=="#":    #skip comment
                        continue
                vurl=up.urljoin(url,line)
                if log:
                        print("vurl",vurl,file=log)
                if ".m3u8" in vurl:    #dl m3u8
                        resdata+=_dlm3u8(vurl,session=session)
                elif ".ts" in vurl:    #dl ts
                        res=session.get(vurl)
                        resdata+=res.content
        return resdata

def dlm3u8(url,fname):
        # ffmpegのダウンロード最適化: 再接続オプションを追加して途切れを防止する
        command = f'ffmpeg -y -reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 300 -i "{url}" "{fname}"'
        subprocess.call(command, shell=True)
