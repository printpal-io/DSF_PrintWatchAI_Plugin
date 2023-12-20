import urllib3
#import aiohttp
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests

class MJPEG:
    def __init__(
            self,
            id : str = '',
            ip : str = ''
        ):
        self.id = id
        self.ip = ip
        self.byte_frame = None


    def snap_sync(self):
        try:
            r = requests.get(self.ip, timeout=5.0)
            if r.status_code == 200:
                self.byte_frame = r.content
                return r.content
            return str(r.status_code)
        except Exception as e:
            return str(e)
