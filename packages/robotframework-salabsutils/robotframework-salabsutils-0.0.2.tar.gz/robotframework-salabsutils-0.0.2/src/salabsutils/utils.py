from base_class import DynamicRobotApiClass
from robot.api.deco import keyword
from furl import furl
from http.cookies import SimpleCookie


class SalabsUtils(DynamicRobotApiClass):
    def __init__(self):
        pass

    @keyword("Add Basic Authentication To Url")
    def add_authentication(self, url, l, p):
        data = furl(url)
        data.username = l
        data.password = p
        return data.tostr()

    @keyword
    def split_url_to_host_and_path(self, url):
        data = furl(url)
        return { 'base': str(data.copy().remove(path=True)), 'path':
                str(data.path)}

    @keyword
    def cookies_to_dict(self, cookies):
        ret = {}
        cookie = SimpleCookie()
        cookie.load(cookies)
        for key, morsel in cookie.keys():
            ret[key] = morsel.value
        return ret
