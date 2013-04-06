'''
Created on Apr 5, 2013

@author: tunnelshade
'''
from pyquery import PyQuery as pq
import json
#===============================================================================
# This function takes in ascii decoded data and using pyquery searches for
# appropriate classes & ids and extracts the urls which populate url_list. 
#===============================================================================
def Google_Results_Parser(data):
    data = pq(data)
    data = data("#rso").find(".g")
    url_list = []
    for i in range(0,len(data)):
        data[i] = pq(data[i]).find(".l").attr("href")
        if data[i] != None:
            url_list.append(data[i])
    return url_list
#===============================================================================
# This function takes in ascii decoded data which is in json format and then 
# parses it for search results number and then parses the results
#===============================================================================
def Google_Json_Parser(data):
    data = json.loads(data)
    number = int(data['queries']['request'][0]['totalResults'])
    url_list = []
    if number != 0:
        data = data['items']
        for result in data:
            url_list.append(result['link'])
    return url_list