"""import matplotlib.pyplot as plt
plt.plot([1,2,1,10])
plt.ylabel('some numbers')
plt.savefig("app/static/pic.jpg",transparent = True)"""

import matplotlib.pyplot as plt
import sqlite3 as lite
import sys
import numpy as np
import matplotlib.pyplot as plt
import math

con = None
def distance(x1,y1,x2,y2):
    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return dist

def lpCal(observer_time,offset):
    regression = np.polyfit(observer_time, offset, 1)
    return regression
    
try:
    con1 = lite.connect('ublox1.db')   
    cur1 = con1.cursor()                  
    cur1.execute('SELECT * from Ticklog')
    data1 = cur1.fetchall()
    raw_data1 = np.array(data1)
    
    #con2 = lite.connect('ublock2.db')
    con2 = lite.connect('ublox2.db')
    cur2 = con2.cursor() 
    cur2.execute('SELECT * from Ticklog')
    data2 = cur2.fetchall()
    raw_data2 = np.array(data2)
    
    con3 = lite.connect('ublox3.db')
    cur3 = con3.cursor() 
    cur3.execute('SELECT * from Ticklog')
    data3 = cur3.fetchall()
    raw_data3 = np.array(data3)
    
    con4 = lite.connect('ublox4.db')
    cur4 = con4.cursor() 
    cur4.execute('SELECT * from Ticklog')
    data4 = cur4.fetchall()
    raw_data4 = np.array(data4)
    
except lite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    if con:
        con.close()

total = 300
samples = -1 * total  
lineslop = [0.,0.,0.,0.,0.] 
result =  [0., 0., 0., 0., 0.,]
    
#1st one
input_data1 = np.array((raw_data1[samples:,3].astype(np.int)*10,raw_data1[samples:,4].astype(np.int)))
array_data1 = np.transpose(input_data1)
observer_time1 = array_data1[:,1]-array_data1[0,1]
sender_time1= array_data1[:,0] - array_data1[0,0] 
offset1 = sender_time1 - observer_time1
sp1 = 1.*offset1
slop1 = np.divide (sp1[1:], observer_time1[1:])
lineslop[1] = sum (slop1[:]) / (total-1.)
result1 = lpCal(observer_time1,offset1)
result[1] = result1[0]

#2nd one
input_data2 = np.array((raw_data2[samples:,3].astype(np.int)*10,raw_data2[samples:,4].astype(np.int)))
array_data2 = np.transpose(input_data2)
observer_time2 = array_data2[:,1]-array_data2[0,1]
sender_time2= array_data2[:,0] - array_data2[0,0]   
offset2 = sender_time2 - observer_time2
sp2 = 1.*offset2
slop2 = np.divide (sp2[1:], observer_time2[1:])
lineslop[2] = sum (slop2[:]) / (total -1.)
result2 = lpCal(observer_time2,offset2)
result[2] = result2[0]

#3rd one
input_data3 = np.array((raw_data3[samples:,3].astype(np.int)*10,raw_data3[samples:,4].astype(np.int)))
array_data3 = np.transpose(input_data3)
observer_time3 = array_data3[:,1]-array_data3[0,1]
sender_time3= array_data3[:,0] - array_data3[0,0]    
offset3 = sender_time3 - observer_time3
sp3 = 1.*offset3
slop3 = np.divide (sp3[1:], observer_time3[1:])
lineslop[3] = sum (slop3[:]) / (total -1.)
result3 = lpCal(observer_time3,offset3)
result[3] = result3[0]

#4th one
input_data4 = np.array((raw_data4[samples:,3].astype(np.int)*10,raw_data4[samples:,4].astype(np.int)))
array_data4 = np.transpose(input_data4)
observer_time4 = array_data4[:,1]-array_data4[0,1]
sender_time4= array_data4[:,0] - array_data4[0,0]    
offset4 = sender_time4 - observer_time4
sp4 = 1.*offset4
slop4 = np.divide (sp4[1:], observer_time4[1:])
lineslop[4] = sum (slop4[:]) / (total -1.)
result4 = lpCal(observer_time4,offset4)
result[4] = result4[0]
#print "slop 4: ", lineslop4, result4

observer_time = [[], observer_time1, observer_time2, observer_time3, observer_time4]
offset = [[], offset1, offset2, offset3, offset4]

Id = int(input ("Please input the ID number to check? "))
ID = str(Id)
conT = lite.connect('test.db')
curT = conT.cursor() 
curT.execute('SELECT ID, CTick, STick from Ticklog WHERE ID=?', ID)
dataT = curT.fetchall()
test_dataT = np.array(dataT)
    
#input_dataT is the test data and is to be validated and do the % of similarity check
input_dataT = np.array ((test_dataT[samples:,1].astype(np.int)*10,test_dataT[samples:,2].astype(np.int)))
array_dataT = np.transpose (input_dataT)
#take line 1 slop as the fingerprint object to compare. Normalized data
observer_timeT = array_dataT[:,1] - array_dataT[0,1]
sender_timeT = array_dataT[:,0] - array_dataT[0,0]
offsetT = sender_timeT - observer_timeT
spT = 1. * offsetT
slopT = np.divide (spT[1:], observer_timeT[1:])
lineslopT = sum (slopT[:]) / (total - 1.)
resultT = lpCal(observer_timeT,offsetT)
print "slop T: ", lineslopT, resultT

#mng = plt.get_current_fig_manager()
#mng.full_screen_toggle()
maxdif = 0 ;
eachdif = [0. , 0. ,0. ,0. ,0.]
result_range = len(result)
#for i in range(1, result_range):
# angle difference shows the similiarity. 90degree diffence is defined as absoultely different
for i in range(1, result_range):
    difference = (1. - abs(math.atan(resultT[0])*10000000. - math.atan(result[i])*10000000.)/90.)*100.
    if (difference < 0.): difference = 0.
    print " similarity by y = ax+b for ID ", i," is ", difference, "%"
    eachdif[i] = difference;
    if(maxdif < difference): 
        maxdif = difference; 
        maxID = i;

"""
Drawing
"""  
plt.figure(figsize=(8,5))
plt.plot(observer_time[1], offset[1], 'b.', label='ID 1',markersize = 4)
plt.plot(observer_time[2], offset[2], 'g.', label='ID 2',markersize = 4)
plt.plot(observer_time[3], offset[3], 'y.', label='ID 3',markersize = 4)
plt.plot(observer_time[4], offset[4], 'k.', label='ID 4',markersize = 4)
plt.plot(observer_timeT, offsetT, 'r.', label='test',markersize = 10)
plt.xlabel('observer_time TIME(usec)')
plt.ylabel('OFFSET(usec)')
plt.legend(loc='lower left')
plt.title ('Similarity against ID %d'%maxID + ' is %d %%'%maxdif, fontsize=24)
plt.show()

f ,axarr = plt.subplots(2,2)
axarr[0,0].plot(observer_time[1], offset[1], 'b.', label='ID 1')
axarr[0,0].set_title('Similarity against ID %d'%1 + ' is %d %%'%eachdif[1], fontsize=16)
axarr[0,0].plot(observer_timeT, offsetT, 'r.', label='test',markersize = 10)
axarr[0,0].legend(loc='lower left')
                        
axarr[0,1].plot(observer_time[2], offset[2], 'b.', label='ID 2')
axarr[0,1].set_title('Similarity against ID %d'%2 + ' is %d %%'%eachdif[2], fontsize=16)
axarr[0,1].plot(observer_timeT, offsetT, 'r.', label='test',markersize = 10) 
axarr[0,1].legend(loc='lower left')   
    
axarr[1,0].plot(observer_time[3], offset[3], 'b.', label='ID 3')
axarr[1,0].set_title('Similarity against ID %d'%3 + ' is %d %%'%eachdif[3], fontsize=16)
axarr[1,0].plot(observer_timeT, offsetT, 'r.', label='test',markersize = 10)
axarr[1,0].legend(loc='lower left')
                        
axarr[1,1].plot(observer_time[4], offset[4], 'b.', label='ID 4')
axarr[1,1].set_title('Similarity against ID %d'%4 + ' is %d %%'%eachdif[4], fontsize=16)
axarr[1,1].plot(observer_timeT, offsetT, 'r.', label='test',markersize = 10)
axarr[1,1].legend(loc='lower left')
