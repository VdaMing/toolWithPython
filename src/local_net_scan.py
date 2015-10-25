#/usr/bin/python
#This software is used to scan local network http server, the default max thread number is 20

import socket
import struct
import httplib
import threading

class HttpThread(threading.Thread):
	'singe thread for http request'
	totalThreadNum = 0;
	def __init__(self, ip, ipPort, fo):
		threading.Thread.__init__(self);
		self.ip = ip;
		self.ipPort = ipPort;
		self.fo = fo;
		HttpThread.totalThreadNum += 1;

	def run(self):
		scanStart(self.ip, self.ipPort, self.fo);
		HttpThread.totalThreadNum -= 1;	

def scanStart(ip,ipPort,fo):
	"start scan the specified ip and port"
	portList=ipPort.split(",", ipPort.count(","));
	for port in portList :
		address = ip+":"+port;
		print "address = "+address;
		try : 	
			conn = httplib.HTTPConnection(ip, port, timeout=3);	
			conn.request("GET", "");
			res = conn.getresponse();
			print res.status;
			print res.reason;
			if res.status == 200 or res.status == 302 or res.status == 403 :
				fo.write(address+str(res.status)+res.reason+"\n");
		except :
			continue;	
		finally :	
			conn.close();

	return;

def main(): 
	startIpStr = raw_input("Enter the start ip address:");
	endIpStr = raw_input("Enter the end ip address:");
	ipPort = raw_input("Enter the http request port:");
	
	startIpList = startIpStr.split(".", 3);
	endIpList = endIpStr.split(".", 3);
	#ipCount = (int(endIpList[0])-int(startIpList[0]))*255*255*255+(int(endIpList[1])-int(startIpList[1]))*255*255 + (int(endIpList[2])-int(startIpList[2]))*255 + (int(endIpList[3])-int(startIpList[3])); 
	startIpInt = int(startIpList[0])*255*255*255 + int(startIpList[1])*255*255 + int(startIpList[2])*255 + int(startIpList[3]);
	endIpInt = int(endIpList[0])*255*255*255 + int(endIpList[1])*255*255 + int(endIpList[2])*255 + int(endIpList[3]);
	ipCount = endIpInt - startIpInt;
	print "start ip " + str(startIpInt);
	print "end ip " + str(endIpInt);
	print "count " + str(ipCount);
	i = 0;	
	fo = open("ip_scan.txt", "a+");
	while i <= ipCount+1 :	
		if HttpThread.totalThreadNum >= 20:
			continue;	
		i += 1;	
		ipaddressStr = str((startIpInt+i)/255/255/255) + "." + str((startIpInt+i)/255/255%255) + "." + str((startIpInt+i)/255%255) + "." + str((startIpInt+i)%255);
		myThread = HttpThread(ipaddressStr,ipPort,fo);
		myThread.start();	


	while HttpThread.totalThreadNum > 0:
		time.sleep(1);	
	fo.close();	
	return;

if __name__=='__main__':
	main();
