# November 19, 2013
# Rebecca W. Perry

import urllib2, csv, pickle
from numpy import zeros
import time

start = time.time()

#the APS units are not specifically sensitive to the year
downloaded_data  = urllib2.urlopen('http://www.aps.org/membership/units/')
csv_data = csv.reader(downloaded_data)


divisions = []
divisions.append(['Atomic, Molecular & Optical Physics','DAMOP']) #gets missed below

for row in csv_data:
    if len(row)==1: # MISSES THE FIRST ONE THAT HAS TWO ELEMENTS FOR SOME REASON
        if len(row[0]) > 24:
            if row[-1][-6:] == '<br />' and row[0][0:3].strip() == '<a':
                #print row
                name, abbreviation = row[-1].split(' (', 1)
                divisions.append([name.split('>')[1], abbreviation.split(')')[0]])

print 'There are '+str(len(divisions))+ ' units'

alldivisions = [x[1] for x in divisions]
end = time.time()

print 'Time: '+ str(end-start)

#write out the array of names and abbreviations
outfile = open('unit_info.pkl','wb')
pickle.dump(divisions, outfile)
outfile.close()
