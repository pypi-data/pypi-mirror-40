import requests, socket
from collections import Counter 

Endpoints = [
    "https://myexternalip.com/raw",
    "https://icanhazip.com/",
    "http://ifconfig.io/ip",
    "http://checkip.amazonaws.com/",
    "http://ident.me/",
    "http://whatismyip.akamai.com/",
    "http://tnx.nl/ip",
    "http://myip.dnsomatic.com/",
    "http://diagnostic.opendns.com/myip",
    ]

class Client():

    def __init__(self, consensus=False):
        self.consensus = consensus

    def external_ip(self):

        if self.consensus == False:

            for endpoint in Endpoints:
                try:
                    result = requests.get(endpoint)
                    external_ip = result.content.decode('utf-8')
                    external_ip = external_ip.replace('\n', '')
                    break
                except:
                    pass
            return external_ip

        if self.consensus == True:
            ips = []
            for endpoint in Endpoints:
                try:
                    result = requests.get(endpoint)
                    external_ip = result.content.decode('utf-8')
                    external_ip = external_ip.replace('\n', '')
                    ips.append(str(external_ip))
                except:
                    pass
            counter = Counter(ips)
            return counter.most_common()[0][0]
            

    def local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return False

