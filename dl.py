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

# def dlm3u8(url,fname):
#         data=_dlm3u8(url)
#         if not data:
#                 return False
#         with open(fname,"wb") as f:
#                 f.write(data)

def dlm3u8(url,fname):
        command = 'ffmpeg -i '+url+' '+fname
        subprocess.call(command, shell=True)
        # data=_dlm3u8(url)
        # if not data:
        #         return False
        # with open(fname,"wb") as f:
        #         f.write(data)
