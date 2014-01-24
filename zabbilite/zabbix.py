# encode=utf-8
import json
import urllib2

class Zabbix(object):
    
    auth = None

    def __init__(self,url="http://zabbix/api_jsonrpc.php"):
        self.url = url

    def request(self, data):
        data["jsonrpc"] = '2.0'
        data['auth'] = self.auth
        data = json.dumps(data)
        request = urllib2.Request(self.url, data, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        contents_str = contents.read()
        contens_dict = json.loads(contents_str)
        return contens_dict["result"]

        
    def login(self,username,password):
        self.auth = None
        result = self.request({'method':'user.authenticate',
                               'params':{'user':username, 'password':password},
                               'id': 1})
        self.auth = result

    def triger_get(self, output=["triggerid", "description", "priority", "lastchange"]):
        result = self.request({"method": "trigger.get",
                               "params": {
                                          "monitored":1,"expandData":1,
                                          "output":output,
                                          "filter":{"status":0, "value":1},
                                          },
                               'id':1
                               })
        return result
