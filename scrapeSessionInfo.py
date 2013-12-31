# November 19, 2013
# Rebecca W. Perry

import csv
import urllib2, csv
from numpy import zeros
import pickle


#currently scraping 2013 meeting info
downloaded_data  = urllib2.urlopen('http://meetings.aps.org/Meeting/MAR14/sessionindex2')
csv_data = csv.reader(downloaded_data)

sessions = []

i = 0
for row in csv_data:
    if len(row) > 0:
        print row
        if len(row) > 1:
            for i in range(1,len(row)):
                row[0] += row[i]
            print row
        if len(row[0]) >56:
            if row[0][-3:] == 'br>':
                junk, title = row[0].split(">",1)
                sessions.append(title[:-8])

session_info = []

for s in sessions:
    if s[0].isdigit():
        t = 'do nothing' #takes care of first odd session 1A
    else:
        if s[2].isdigit(): #deals with single digit and two digit numbers
            session_info.append([s[0],int(s[1:3]),s[5:]])
        else:
            session_info.append([s[0],int(s[1]),s[4:]])


#open up each link and add the sponsoring units and room number to session_info
for i in range(0,len(session_info)):
    #make URL's out of the session_info I've already collected
    address = 'http://meetings.aps.org/Meeting/MAR14/Session/'+session_info[i][0]+str(session_info[i][1])
    print address
    downloaded_data  = urllib2.urlopen(address)
    csv_data = csv.reader(downloaded_data)

    for row in csv_data:
        if len(row)>0:
            if len(row[0])>20: #candidate for row with room and sponsor info
                if len(row[-1].split('Room:'))==2:
                    session_info[i].append(row[-1].split('Room: <i>')[1].split('</i>')[0].lstrip())
                if row[0][15:25]=='Sponsoring':
                    session_info[i].append(row[0].split("<br")[0].split("Units: ")[1])
  

outfile = open('session_info.pkl','wb')
pickle.dump(session_info, outfile)
outfile.close()
