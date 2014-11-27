'''
Created on Apr 3, 2013

@author: tunnelshade
'''
import urllib.request
import urllib.parse
import gzip
from lib.parser import Google_Results_Parser, Google_Json_Parser
import time

#===============================================================================
# A class which has methods for direct search of search through API. Both the
# search methods have error catching ability for time-out and service unavailable
# error. Gzip compression is used so as to reduce data usage.
#===============================================================================
class Search_Google():
    def __init__(self, domain, search_words,  limit, proxy=None, proxy_username='', proxy_password=''):
        self.domain = domain
        if proxy is not None:
            self.proxy = proxy
            proxy_handler = urllib.request.ProxyHandler(proxy)
            proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
            proxy_auth_handler.add_password(None, 'https://www.google.com/', proxy_username, proxy_password)
            self.opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
        else:
            self.opener = urllib.request.build_opener()
        self.opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11'),
                                  ('Accept-Encoding','gzip')]
        self.url = 'https://www.google.com/search?hl=en&meta=&output=search'
        self.search_phrase = '&q=site:' + domain
        for keyword in search_words:
            self.search_phrase = self.search_phrase + '%20' + urllib.parse.quote(keyword,safe=':')
        self.url += self.search_phrase
        self.limit = limit
        self.url_list = []
    #=======================================================================
    # A method which starts searching from given result number and runs till
    # the limit is exceeded or the search results get exhausted. The search
    # is done directly without any JSON. Google_Results_Parser is called.
    #=======================================================================
    def search(self, start):
        for start in range(0,self.limit,10):
            self.url += '&start=' + str(start)
            try:
                data = self.opener.open(self.url)
                data = gzip.decompress(data.readall())
                data = data.decode('ascii','ignore')
                temp_list = Google_Results_Parser(data)
                if len(temp_list) != 0:
                    self.url_list += temp_list
                else:
                    break
            except urllib.error.HTTPError as e:
                if e == 'HTTP Error 503: Service Unavailable':
                    print("[!] Going to sleep for 1 minute to prevent lockout")
                    time.sleep(60)

            except urllib.error.URLError as e:
                print("[!] Proxy server "+str(self.proxy)+" appears down")
        return self.url_list
    #===========================================================================
    # A method which starts searching from given result number and runs till
    # the limit is exceeded or the search results get exhausted. Here search is
    # done using JSON (Google CSE). If you wish to use your own CX and API-KEY
    # , then replace the values in the first two lines. Google_Json_Parser called
    #===========================================================================
    def search_api(self,start):
        self.url_api = 'https://www.googleapis.com/customsearch/v1?hl=en&cx=006870906752541368823:e2em1hbfmfe'
        self.url_api += '&key=AIzaSyC8aj1lOsNjg087WSxnIEYuxtGpBmtGjjE'
        self.url_api += self.search_phrase
        for start in range(0,self.limit,10):
            self.url += '&start=' + str(start)
            try:
                data = self.opener.open(self.url_api)
                data = gzip.decompress(data.readall())
                data = data.decode('ascii','ignore')
                temp_list = Google_Json_Parser(data)
                if len(temp_list) != 0:
                    self.url_list += temp_list
                else:
                    break
            except urllib.error.HTTPError as e:
                if e == 'HTTP Error 503: Service Unavailable':
                    print("[!] Going to sleep for 1 minute to prevent lockout")
                    time.sleep(60)

            except urllib.error.URLError as e:
                print("[!] Proxy server "+str(self.proxy)+" appears down")
        return self.url_list
