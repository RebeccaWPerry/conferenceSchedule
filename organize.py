# Rebecca W. Perry
# Load saved session info and sort to use.


#very much care about day of the week and talks upcoming


import pickle
import csv
import urllib2

infile = open('unit_info.pkl','r')
unit_info = pickle.load(infile)
infile.close()

javaobject = "["

for i in range(0,len(unit_info)):

    if i ==0:
        javaobject += '{name: \''+unit_info[i][0]+'\', s: \''+unit_info[i][1]+'\'},\n'
    elif i == len(unit_info)-1:
        javaobject += '{name: \''+unit_info[i][0]+'\', s: \''+unit_info[i][1]+'\'}]\n'
    else:
        javaobject += '{name: \''+unit_info[i][0]+'\', s: \''+unit_info[i][1]+'\'},\n'

f = open('unit_info_java','w')
f.write(javaobject)
f.close()






infile = open('session_info.pkl','r')
session_info = pickle.load(infile)
infile.close()

print 'There are '+str(len(session_info))+' sessions.'

for i in range(0,len(session_info)):
    if len(session_info[i])==4:
        session_info[i].append('none')


#how many sponsoring units are there?
sponsors = set()

for i in range(0,len(session_info)):
    if len(session_info[i])==5:
        sponsors.add(session_info[i][4])

#how many sponsoring units are there?
sponsors = set()

for i in range(0,len(session_info)):
    if len(session_info[i])==5:
        for word in session_info[i][4].split():
            sponsors.add(word)

#I have one bad one in there that has a slash instead of a space between division names
#sponsors.remove('FIAP/DCOMP')

print 'There are '+str(len(sponsors))+' sponsors.'




#how many sessions by each sponsor on each day?
#also, add day to info
#many are cosponsored
topical = []

for s in sponsors:
    count = 0
    m = 0
    tu = 0
    w = 0
    th = 0
    f = 0

    for i in range(0,len(session_info)):
        if len(session_info[i])==5:
            for word in session_info[i][4].split():
                if word == s:
                    count += 1
                    sess = session_info[i][0]
                    if sess <'F': #a through e
                        m +=1
                        session_info[i].append('M')
                    if sess > 'E' and sess < 'L':
                        tu +=1
                        session_info[i].append('Tu')
                    if sess > 'K' and sess < 'S':
                        w +=1
                        session_info[i].append('W')
                    if sess > 'R' and sess < 'Y':
                        th +=1
                        session_info[i].append('Th')
                    if sess > 'X':
                        f +=1
                        session_info[i].append('F')
                
    topical.append([s, count, m, tu, w, th, f])

#time of day
#rows with all other session letters get removed
for i in range(0,len(session_info)):
    if session_info[i][0] in ['A','F','L','S','Y']:
        session_info[i].append('8') #8:00 am
    elif session_info[i][0] in ['B','G','M','T','Z']:
        session_info[i].append('11') #11:15 am
    elif session_info[i][0] in ['D','J','Q','W']:
        session_info[i].append('2') #2:30 pm
    else:
        session_info[i].append('OTHER') #other special session

#remove unneeded sessions
session_info = [s for s in session_info if s[-1]!='OTHER']


#what is the set of room numbers?
rooms = set()

for i in range(0,len(session_info)):
    rooms.add(session_info[i][3])

rooms = list(rooms)
rooms = sorted(rooms)

#write out as a csv
resultFile = open('rooms.csv','wb')
wr = csv.writer(resultFile)
wr.writerows([rooms])
resultFile.close()

print 'There are '+str(len(rooms)) +' rooms.'




#focus session or invited session?

for i in range(0,len(session_info)):
    if session_info[i][2][0:5] == 'Focus':
        session_info[i].append('focus')
        #cut focus session out of title
        session_info[i][2] = session_info[i][2][14:].strip()
    elif session_info[i][2][0:7] == 'Invited':
        session_info[i].append('invited')
        #cut invited session out of title
        session_info[i][2] = session_info[i][2][16:].strip()
    else:
        session_info[i].append('regular')

for s in sponsors:
    count = 0
    m = 0
    tu = 0
    w = 0
    th = 0
    f = 0

    #determine day of the week
    for i in range(0,len(session_info)):
        if len(session_info[i])==5:
            for word in session_info[i][4].split():
                if word == s:
                    count += 1
                    sess = session_info[i][0]
                    if sess <'F': #a through e
                        m +=1
                        session_info[i].append('M')
                    if sess > 'E' and sess < 'L':
                        tu +=1
                        session_info[i].append('Tu')
                    if sess > 'K' and sess < 'S':
                        w +=1
                        session_info[i].append('W')
                    if sess > 'R' and sess < 'Y':
                        th +=1
                        session_info[i].append('Th')
                    if sess > 'X':
                        f +=1
                        session_info[i].append('F')
                
    topical.append([s, count, m, tu, w, th, f])



#slicing into list-- list comprehension:

monday = sum([x[1] for x in topical])
tuesday = sum([x[2] for x in topical])
wednesday = sum([x[3] for x in topical])
thursday = sum([x[4] for x in topical])
friday = sum([x[5] for x in topical])

print topical

#how many sessions on each day?

d = [0]*5

for s in session_info:
    sess = s[0]
    if sess <'F': #a through e
        d[0] +=1
    if sess > 'E' and sess < 'L':
        d[1] +=1
    if sess > 'L' and sess < 'T':
        d[2] +=1
    if sess > 'S' and sess < 'Y':
        d[3] +=1
    if sess > 'X':
        d[4] +=1

print 'There are '+str(sum(d))+' sessions for which I know the day.'
print d



#FORMAT
#Currently have:
#session letter, session number, title, room, sponsor, day, time, kind

#want:
#{title:'Interesting Talks 1', sponsor: 'Atomic, Molecular & Optical Physics',
#                            day:"M",time:8, room: "301",kind:"focus"},

javaobject = "["

for i in range(0,len(session_info)):
    #print i

    t = session_info[i][2]
    c = session_info[i][0]+str(session_info[i][1])

    if i ==0:
        javaobject += '{"code": \"'+c+'\","title": \"'+t+'\", "sponsor": \"'+session_info[i][4]+'\", "day": \"'+session_info[i][5]+'\", "time": '+session_info[i][6]+', "room": \"'+session_info[i][3]+'\", "kind": \"'+session_info[i][7]+'\"},\n'
    elif i == len(session_info)-1:
        javaobject += '{"code": \"'+c+'\","title": \"'+t+'\", "sponsor": \"'+session_info[i][4]+'\", "day": \"'+session_info[i][5]+'\", "time": '+session_info[i][6]+', "room": \"'+session_info[i][3]+'\", "kind": \"'+session_info[i][7]+'\"}]'
    else:
        javaobject += '{"code": \"'+c+'\", "title": \"'+t+'\", "sponsor": \"'+session_info[i][4]+'\", "day": \"'+session_info[i][5]+'\", "time": '+session_info[i][6]+', "room": \"'+session_info[i][3]+'\", "kind": \"'+session_info[i][7]+'\"},\n'

f = open('session_info_java','w')
f.write(javaobject)
f.close()


#currently scraping 2013 meeting info
downloaded_data  = urllib2.urlopen('http://www.aps.org/membership/units/')
csv_data = csv.reader(downloaded_data)


divisions = []

divisions.append(['Atomic, Molecular & Optical Physics','DAMOP'])

for row in csv_data:
    if len(row)==1: # MISSES THE FIRST ONE THAT HAS TWO ELEMENTS FOR SOME REASON
        if len(row[0]) > 24:
            if row[-1][-6:] == '<br />' and row[0][0:3].strip() == '<a':
                #print row
                name, abbreviation = row[-1].split(' (', 1)
                divisions.append([name.split('>')[1], abbreviation.split(')')[0]])

print 'There are '+str(len(divisions))+ ' units'

#divisions # all possible divisions and their long name
#sponsors # just the sponsors actually sponsoring stuff in the meeting

a = []
for i in divisions:
    if len( set([i[1]]).intersection(sponsors) ) >0:
        a.append(i)

a.append(['Committee on Minorities','COM'])
a.append(['Shock Compression of Condensed Matter','GSCCM'])
a.append(['Society of Physics Students','SPS'])
a.append(['American Physical Society','APS'])
a.append(['National Science Foundation','NSF'])
a.append(['no sponsor',''])
a.append(['Invited Session',''])
a.append(['Focus Session',''])
# missing 6: com, gsccm, sps, aps, nsf, none


javaobject = "["

for i in range(0,len(a)):

    t = a[i][1]
    c = a[i][0]

    if i ==0:
        javaobject += '{name: \''+c+'\', s: \''+t+'\', isToggled: false},\n'
    elif i == len(a)-1:
        javaobject += '{name: \''+c+'\', s: \''+t+'\', isToggled: false}]'
    else:
        javaobject += '{name: \''+c+'\', s: \''+t+'\', isToggled: false},\n'

f = open('sponsor_info_java','w')
f.write(javaobject)
f.close()



