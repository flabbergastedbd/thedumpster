'''
Created on Apr 5, 2013

@author: tunnelshade
'''
from pyquery import PyQuery as pq

def Google_Results_Parser(data):
    data = pq(data)
    data = data("#rso").find(".g")
    url_list = []
    for i in range(0,len(data)):
        data[i] = pq(data[i]).find(".l").attr("href")
        if data[i] != None:
            url_list.append(data[i])

    return url_list