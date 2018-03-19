# coding: utf-8

# This little project is hosted at: <https://gist.github.com/seccodingguy>
# Copyright 2018 Mark Wireman [wiremanm at gmail dot com]
# License: GPL <http://www.gnu.org/copyleft/gpl.html>

import requests
import time
import sys 
import os.path
import smtplib
import time
import ConfigParser
import subprocess
import datetime
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

from email.mime.text import MIMEText

"List of free ip services"
"http://icanhazip.com/"
"http://checkip.dyndns.org/"
"https://freegeoip.net/json/"
"http://www.telize.com/ip"
"http://ip-api.com/json"
"http://curlmyip.com/"
"http://ipinfo.io/ip"

#Global variables
ipFile="/tmp/ip.log"
timeout = 10

class Service:
  url=""
  def request(self): return requests.get(self.url, timeout = timeout)

class Icanhazip(Service):
  name="icanhazip"
  url="http://icanhazip.com/"
  def ip(self): return self.request().text.strip()

class Freegeoip(Service):
  name="freegeoip"
  url="https://freegeoip.net/json/"
  def ip(self): return self.request().json()["ip"]

class Telize(Service):
  name="telize"
  url="http://www.telize.com/ip"
  def ip(self): return self.request().text.strip()

class IpApi(Service):
  name="ip-api"
  url="http://ip-api.com/json"
  def ip(self): return self.request().json()["query"]

class Ifconfig(Service):
  name="ifconfig.me"
  url="http://ifconfig.me/all.json"
  def ip(self): return self.request().json()["ip_addr"]

def updateConfigFile(oldip,newip):
   found = 0
   s = 'PLACHOLDER'
   currentTime = str(datetime.datetime.now())
   config = ConfigParser.RawConfigParser()
   config.read('ipchange_config.conf')
   
   baseconfname = config.get('OpenVPN','clientdir') + '/' + config.get('OpenVPN','baseconfigname')
   baseconftemplate = config.get('OpenVPN','baseconfigtemplate')
   backupName = baseconfname + '.bak'
   cmdRmv = 'rm ' + backupName
   cmd = 'cp ' + baseconfname + ' ' + backupName
   cmdClientFile = 'sh ' + config.get('OpenVPN','clientdir') + '/' + config.get('OpenVPN','ovpnscriptname')
   
   print 'Checking if IP Address has changed in the base configuration file.'
   
   with open(baseconfname,'r') as f :
     s = f.read()
     if oldip in s :
       found = 1

   if found :
     print 'Old IP Address ' + oldip + ' found in base configuration file.'
     print 'Beginning process to replace ' + oldip + ' with ' + newip + '.'
     subprocess.call(cmdRmv,shell=True)
     subprocess.call(cmd,shell=True)
     with open(baseconfname,'r') as f :
       s = s.replace(oldip,newip)
     with open(baseconfname,'w') as f :
       f.write(s)
     subprocess.Popen(['bash',config.get('OpenVPN','ovpnscriptname'),'client1'])
     print 'Finished updating ' + baseconfname + ' with new ip address.'
     print 'Finished creating Client OVPN file.'

def sendIPAddr(oldip,newip):
  config = ConfigParser.RawConfigParser()
  config.read('ipchange_config.conf')
  toAddr = config.get('SMTP','sendto')
  smtpSvc = config.get('SMTP','service')
  smtpPort = config.getint('SMTP','port')

  print 'Sending email using ' + config.get('SMTP','service')
  server = smtplib.SMTP(smtpSvc,smtpPort)
  debugLvl = config.getint('SMTP','debuglevel')

  if debugLvl > 0 :
    server.set_debuglevel(debugLvl)

  server.starttls()

  server.login(config.get('SMTP','username'),config.get('SMTP','password'))
  msg = MIMEMultipart()
  msg['From']=config.get('SMTP','username')
  msg['To']=toAddr
  msg['Subject']='IP Addr Changed'
  msg.attach(MIMEText(newip))
  print 'Attached MIMEText ' + msg.as_string()

  f = config.get('OpenVPN','ovpnfile')

  with open(f, "rb") as fil:
    part = MIMEApplication(fil.read(),Name=basename(f))
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
    msg.attach(part)
    print 'Attached file ' + basename(f)

  server.sendmail(config.get('SMTP','username'),toAddr,msg.as_string())
  server.quit()
  print 'Email sent successfully!'

def request_ip():
  #List of services
  #services = [Icanhazip(), Freegeoip(), Telize(), IpApi(), Ifconfig() ]
  services = [IpApi()]
  for i in range(len(services)):
    
    service = services[i]
    try:
      start = time.time()
      print "* Requesting current ip with '{}'".format(service.name)
      ip = service.ip()
      print "* Request took {} seconds ".format(int(time.time() - start))
      return ip
    except Exception as error:
      print "* Exception when requesting ip using '{}': {} ".format(service.name, error )
      
  error = "Non available services, add more services or increase the timeout (services = {}, timeout = {}) ".format(len(services), timeout)
  raise RuntimeError(error)

def current_ip():
  return open(ipFile,"r").readlines()[0]

def save_ip(oldip,newip):
  updateConfigFile(oldip,newip)
  sendIPAddr(oldip,newip)
  f = open(ipFile, 'w')
  f.write(str(newip))

  
#Main
if os.path.isfile(ipFile) : #File exists
  request_ip = request_ip()  
  current_ip = current_ip()

  if request_ip != current_ip:
    save_ip(current_ip,request_ip)
    print "* IP has changed from {} to {}".format(current_ip, request_ip)
#TODO Add in code that will update the VPN Client config, create the Client VPN file and send the file
#along with the new IP address
    sys.exit(1)
  else :
    print "* IP is still the same: {}".format(current_ip)

else: 
  request_ip = request_ip()
  save_ip(request_ip,request_ip)
  print "* This is the first time to run the ip_change script, I will create a file in {} to store your current address: {} ".format(ipFile, request_ip)

  time.sleep(1800)
  
#Test
"""
services = [Icanhazip(), Freegeoip(), Telize(), IpApi(), Ifconfig() ]
for i in range(len(services)):
  service = services[i]
  print "{} ip result: {} ".format(service.name, service.ip() )
"""
