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
                Version-1.2  Made by tunnelshade
        tunnelshade[at]gmail.com <=> www.tunnelshade.in
        
================================================================""")

project_root = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description="A tool that can be used for passive recon using google dorks",
                                epilog = "Ex:- python thedumpster.py -l 10 -ghdb tunnelshade.in")


parser.add_argument("domain", help="Root domain of the infrastructure")
parser.add_argument("-l","--limit", default=2, help="Number of results/dork (default=2)")
parser.add_argument("-ghdb","--ghdb", help="Flag to use GHDB",action="store_true")
parser.add_argument("-ap","--adminpage",help="Flag to search for admin panels",action="store_true")
parser.add_argument("-a","--add", help="Extra Search terms to be included(Separate using comma)")
parser.add_argument("-r","--rem", help="sites to be excluded from search results(Separate using comma)")
parser.add_argument("-ws","--websearch",help="To enable the use of google's search directly",action="store_true")

args, unknown = parser.parse_known_args()

if __name__ == '__main__':
    
    #===========================================================================
    # Code to read proxies from config file and populate proxies list,which will
    # be used for building opener in Google_Search class
    #===========================================================================
    proxies = []
    f = open(os.path.join(project_root,'config'),'r')
    for line in f.readlines():
        line = str(line).rstrip('\n')
        proxies.append({'http':'http://'+line,'https':'https://'+line})
    f.close()
    
    # This dorks list will be populated either by ghdb or adminpage.db or both
    dorks = []
    #===========================================================================
    # If ghdb flag is set in params, then this block executes providing user to 
    # select type of dorks to use from ghdb.db. The select statement is executed
    # here and "dorks" list is populated using those results
    #===========================================================================
    if args.ghdb == True:
        print("""
[1] AnV => Advisories & Vulnerabilities
[2] EM  => Error Messages
[3] FCI => Files with Info
[4] FH  => Footholds
[5] VD  => Vulnerable Data
[6] LP  => Login Portals
[7] SD  => Sensitive Directories
[8] VF  => Vulnerable files
[9] VOD => Various Online Devices
[10] WSD => Web Server Detection
[11] VS  => Vulnerable Server Detection
[12] WS  => Web Services
[13] OT  => Other Stuff
================================================================""")
        ghdb_dic = {1:'AnV',2:'EM',3:'FCI',4:'FH',5:'VD',6:'LP',7:'SD',8:'VF',9:'VOD',10:'WSD',11:'VS',12:'WS',13:'OT'}
        key = input("\nPlease select the type of dorks(Enter number only) > ")
        conn = sqlite3.connect(os.path.join(project_root, 'database/ghdb.db'))
        c = conn.cursor()
        c.execute("select dork from "+ghdb_dic[int(key)])
        for row in c:
            dorks.append(row[0])
        conn.commit()
        c.close()   
    #===========================================================================
    # If admin page finding flag is provided then this block executes providing
    # user to select the possible backend of the sites & corresponding dorks are
    # fetched from db and dorks list is populated.
    #===========================================================================
    if args.adminpage == True:
        conn = sqlite3.connect(os.path.join(project_root, 'database/adminpage.db'))
        c = conn.cursor()
        platforms = ['php','asp','cfm','js','cgi','brf']
        for i in range(0,len(platforms)):
            print("["+str(i)+"] "+platforms[i])
        print("Please select appropriate platform")
        code = input("\n> ")
        c.execute("select dork from "+platforms[int(code)])
        for row in c:
            dorks.append(row[0])
        conn.commit()
        c.close()       
    #==========================================================================
    # Info about domain, limit and number of proxies are printed to console
    #==========================================================================
    print('\n[+] Domain      => '+ str(args.domain))
    print('[+] Limit/Dork  => '+str(args.limit))
    print('[+] Proxies     => '+str(len(proxies)))    
    #==========================================================================
    # If extra search parameters are provided then this code block executes
    # & populates the search_words list.(The separator is ',' (comma))
    #==========================================================================
    search_words = []
    if args.add != None:
        for phrases in args.add.split(','):
            search_words.append(phrases)
        print('[+] Extra       => '+str(search_words))
    #==========================================================================
    # If sites are provided which are to be excluded, excl_sites list is 
    # populated using comma as separator & adding '-' at the beginning of site
    #==========================================================================
    excl_sites = []    
    if args.rem != None:
        for site in args.rem.split(','):
            excl_sites.append('-'+str(site))
        print('[+] Excluded    => '+str(excl_sites))
    # A try to catch keyboard interrupt and to print the till then obtained urls.
    # Whenever search must be performed, it depends on ws flag whether it will be
    # done using JSON or direct web search
    try:
        #========================================================================
        # The main program starts here. First robots.txt files are searched for
        # given domain, and printed to console as these urls contains the excluded
        # urls by google bot
        #========================================================================
        robots_list = []
        print('\n[+] Getting the robots.txt file links present !!!')
        num = random.randrange(1,len(proxies),1)
        # site:domain inurl:robots.txt filetype:txt intext:disallow
        obj = Search_Google(args.domain, excl_sites + ['inurl:robots.txt','intext:disallow','filetype:txt'] , 20 , proxies[num])
        if args.websearch:
            robots_list += obj.search(0)
        else:
            robots_list += obj.search_api(0)
        for url in robots_list:
            print('[*] '+url)
        print('\n')
        #=========================================================================
        # The search starts here, using dorks list populated by ghdb||adminpage.db
        #=========================================================================
        url_list = []            
        counter = 1
        for dork in dorks:
            # Randomly a number is selected from the available number of proxies
            num = random.randrange(0,len(proxies),1)
            print('[+] Going through '+str(num)+' for request '+str(counter))
            obj = Search_Google(args.domain, excl_sites +[dork]+search_words , int(args.limit) , proxies[num])
            if args.websearch:
                url_list += obj.search(0)
            else:
                url_list += obj.search_api(0)
            counter += 1
    # Ctrl + C is caught so that obtained urls can be displayed
    except KeyboardInterrupt:
        print("\n[*] Ok dude, Shutting the sh'it' down \n")
    finally:
        for url in url_list:
            print('[*] '+url)
        print('[*] Check it out')
