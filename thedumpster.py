import argparse
import random
import sqlite3
from lib.googlesearch import Search_Google
import os

print("""
================================================================
  _   _                _                           _            
 | | | |              | |                         | |           
 | |_| |__   ___    __| |_   _ _ __ ___  _ __  ___| |_ ___ _ __ 
 | __| '_ \ / _ \  / _` | | | | '_ ` _ \| '_ \/ __| __/ _ \ '__|
 | |_| | | |  __/ | (_| | |_| | | | | | | |_) \__ \ ||  __/ |   
  \__|_| |_|\___|  \__,_|\__,_|_| |_| |_| .__/|___/\__\___|_|   
                                        | |                     
                                        |_|                     
                Version-1.1  Made by tunnelshade
        tunnelshade[at]gmail.com <=> www.tunnelshade.in
        
================================================================
[*]type => what it contains
[*] AnV => Advisories & Vulnerabilities
[*] EM  => Error Messages
[*] FCI => Files with Info
[*] FH  => Footholds
[*] VD  => Vulnerable Data
[*] LP  => Login Portals
[*] SD  => Sensitive Directories
[*] VF  => Vulnerable files
[*] VOD => Various Online Devices
[*] WSD => Web Server Detection
[*] VS  => Vulnerable Server Detection
[*] WS  => Web Services
[*] AP  => Admin Panel
[*] OT  => Other Stuff
================================================================""")

project_root = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description="A tool that can be used for passive recon using google dorks",
                                epilog = "Ex:- python thedumpster.py -l 10 tunnelshade.in AnV")


parser.add_argument("domain", help="Root domain of the infrastructure")
parser.add_argument("-l","--limit", default=10, help="Number of results to be returned in each section")
parser.add_argument("-t","--type", help="Type of dorks to use")
parser.add_argument("-a","--add", help="Additional custom search words")
parser.add_argument("-ws","--websearch",help="To enable the use of google's search directly",action="store_true")


args, unknown = parser.parse_known_args()

url_list = []
proxies = []

if __name__ == '__main__':
    
    dorks = ['']
    if args.type != None:
        conn = sqlite3.connect(os.path.join(project_root, 'database/ghdb.db'))
        c = conn.cursor()
        c.execute("select dork from "+str(args.type))
        for row in c:
            dorks.append(row[0])
        conn.commit()
        c.close()
    
    if args.add != None:
        search_words = [args.add]
        print('[+] Extra       => '+str(args.add)+'\n')
    else:
        search_words = []
        
    f = open(os.path.join(project_root,'config'),'r')
    for line in f.readlines():
        line = str(line).rstrip('\n')
        proxies.append({'http':'http://'+line,'https':'https://'+line})
    f.close()
    
    print('\n[+] Domain      => '+ str(args.domain))
    print('[+] Limit/Dork  => '+str(args.limit))
    print('[+] Dorks       => '+str(args.type) if args.type != None else '[+] Dorks       => No Dorks')
    print('[+] Proxies     => '+str(len(proxies))+'\n')

        
    try:
        counter = 1
        for dork in dorks:
            num = random.randrange(0,len(proxies),1)
            print('[+] Going through '+str(num)+' for request '+str(counter))
            obj = Search_Google(args.domain, [dork]+search_words , int(args.limit) , proxies[num])
            if args.websearch:
                url_list += obj.search(0)
            else:
                url_list += obj.search_api(0)
            counter += 1
    except KeyboardInterrupt:
        print("\n[*] Ok dude, Shutting the sh'it' down \n")
    finally:
        for url in url_list:
            print('[*] '+url)
        print('[*] Check it out')
