# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 19:27:55 2013

@author: tunnelshade
"""
import sqlite3
import codecs

conn = sqlite3.connect('database.db')
c = conn.cursor()
"""
c.execute('create table AnV(dork text PRIMARY KEY, score real)') # Advisories & Vulnerabilities
c.execute('create table EM(dork text PRIMARY KEY, score real)')  # Error Messages
c.execute('create table FCI(dork text PRIMARY KEY, score real)') # Files with Info
c.execute('create table FH(dork text PRIMARY KEY, score real)')  # Footholds
c.execute('create table VD(dork text PRIMARY KEY, score real)')  # Vulnerability Data
c.execute('create table LP(dork text PRIMARY KEY, score real)')  # Login Portals
c.execute('create table SD(dork text PRIMARY KEY, score real)')  # Sensitive Directories
c.execute('create table VF(dork text PRIMARY KEY, score real)')  # Vulnerable files
c.execute('create table VOD(dork text PRIMARY KEY, score real)') # Various Online Devices
c.execute('create table WSD(dork text PRIMARY KEY, score real)') # Web Server Detection
c.execute('create table VS(dork text PRIMARY KEY, score real)') # Vulnerable Server Detection
c.execute('create table WS(dork text PRIMARY KEY, score real)') # Web Services
c.execute('create table AP(dork text PRIMARY KEY, score real)') # Admin Panel
c.execute('create table OT(dork text PRIMARY KEY, score real)') # Other Stuff
"""
conv = {'Advisories and Vulnerabilities':'AnV',
        'Error Messages':'EM',
        'Files containing juicy info':'FCI',
        'Files containing passwords':'FCI',
        'Files containing usernames':'FCI',
        'Footholds':'FH',
        'Network or vulnerability data':'VD',
        'Pages containing login portals':'LP',
        'Sensitive Directories':'SD',
        'Sensitive Online Shopping Info':'SD',
        'Various Online Devices':'VOD',
        'Vulnerable Files':'VF',
        'Vulnerable Servers':'VS',
        'Web Server Detection':'WSD',
        'WebServices':'WS',
        'Administrative':'AP'}

f = codecs.open('18mar.txt', 'r', 'utf-8')
counter = 0
same = 0
for line in f.readlines():
    line = line.split(';;')
    line[-1] = line[-1].rstrip('\n')
    line[-1] = line[-1].replace("'",'')
    if line[-1] != ' ' and len(line) > 1:
        try:
            c.execute("insert into " + conv[line[-2]] +" values ('"+ line[2] +"',0)")
        except sqlite3.IntegrityError:
            same += 1
        except KeyError:
            c.execute("insert into OT values ('"+ line[2] +"',0)")

    counter += 1
print('[*] same = '+str(same))
print('[*] Total = '+str(counter))
conn.commit()
c.close()
f.close()