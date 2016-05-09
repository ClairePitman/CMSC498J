import datetime
import time
#f = open('write1.csv','rb')
#fo = open('train.csv','wb')
f = open('train.csv','rb')
fo = open('trainabs.csv','wb')
# go through each line of the file
z=1
timestart=-100
for line in f:
	bits = line.split(',')
#	if z<10:
#		bits[0]='-1'
#	else:
#		bits[0]='1'
	bits[3]=str(abs(float(bits[3])))
	if z <0:
    	# change third column
		x = time.strptime(bits[2],'%H:%M:%S')
		if timestart<0:
			timestart=datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
		
		bits[2] = str(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()-timestart)
	    # join it back together and write it out
		fo.write( ','.join(bits) )
	z=z+1

f.close()
fo.close()