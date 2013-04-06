=================================
|		thedumpster 1.1         |
|	  Made by tunnelshade       |
|	 tunnelshade@gmail.com      |
=================================

What is this?
-------------

thedumpster is a tool which does passive recon using google and its dorks against a particular domain. Currently it has
feature to allow optional commands. The database making script is also shipped with the remaining scripts. It uses a config
file containing proxies in a given format, so as to avoid bot detection.

How to use
------------

First fill the config file with proxies (atleast 3). The format is given there.

No auth                             => proxyip:port
If basic auth exists for proxy then => username:password@proxyip:port

PS - Only one proxy per line

Dependencies:
------------
Python - 3.3
PyQuery - https://pypi.python.org/pypi/pyquery

TODO:
----
* Adding support for using theharvester domain results
* Pastebin & Pastie search using emails for any password dumps
* Adding larger number of dorks
* Better division of dorks

Comments? Bugs? requests?
------------------------
tunnelshade@gmail.com

Thanks:
-------
Christian Martorella -  theHarvester
Gael Pasgrimaud - PyQuery
Larry Page and Sergey Brin - Google :P

Changelog
---------

v 1.1
-----
* Google JSON/ATOM Search added and made default
* Google websearch is optional
