#coding:utf-8

import requests
import urllib.parse

class Winney(object):

    def __init__(self, host, port=80, protocol="http"):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.domain = "{}://{}".format(protocol, host)
        if port and port != 80:
            self.domain = self.domain+":"+str(port)
        self.RESULT_FORMATS = ["json", "unicode", "bytes"]
        self.result = None
    
    def _bind_func_url(self, url, method):
        def req(data=None, json=None, files=None):
            return self.request(method, url, data, json, files)
        return req
    
    def add_url(self, method, uri, function_name):
        method = method.upper()
        function_name = function_name.lower()
        url = urllib.parse.urljoin(self.domain, uri)
        setattr(self, function_name, self._bind_func_url(url, method))
    
    def request(self, method, url, data=None, json=None, files=None):
        if method.upper() == "GET":
            return self.get(url, data)
        if method.upper() == "POST":
            return self.post(url, data=data, json=json, files=files)

    def get(self, url, params=None):
        assert url
        assert (not params or isinstance(params, dict))
        self.result = requests.get(url, params=params)
    
    def post(self, url, data=None, json=None, files=None):
        assert url
        assert (not data or isinstance(data, dict))
        assert (not json or isinstance(json, dict))
        self.result = requests.post(url, data=data, json=json, files=files)
    
    def put(self, url, data=None):
        assert url
        assert (not data or isinstance(data, dict))
        self.result = requests.put(url, data)
    
    def get_json(self):
        assert self.result
        if self.result.ok:
            return self.result.json
        raise Exception("Error, http status code = {}".format(self.result.status_code))
    
    def get_unicode(self):
        assert self.result
        if self.result.ok:
            return self.result.text
        raise Exception("Error, http status code = {}".format(self.result.status_code))
    
    def get_bytes(self):
        assert self.result
        if self.result.ok:
            return self.result.content
        raise Exception("Error, http status code = {}".format(self.result.status_code))
    
    @property
    def ok(self):
        return self.result.ok


if __name__ == "__main__":
    wy = Winney(host="www.baidu.com")
    wy.add_url(method="get", uri="/", function_name="download")
    wy.download()
    t = wy.get_bytes()
    print(t)
