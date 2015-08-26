#!/usr/bin/python
#####################################################################
# This work by Uncorked Studios is licensed under a 
# Creative Commons Attribution-ShareAlike 4.0 International License.
#####################################################################
import requests
import json
import explorerhat
import time
import datetime
import signal
import sys

# blue blinky for heartbeat
explorerhat.light.blue.pulse(.5,.5,.5,.5)

# configuration constansts
# Robin access token
_ACCESSTOKEN = <YOUR_ROBIN_ACCESS_TOKEN>
# Space ID from Robin
_SPACEID = <YOUR_ROBIN_SPACE_ID>
# interval, in seconds, to check the Robin API for room presence
_INTERVAL = 60 

# tells program to terminate
done = False

def reportOut(text):
  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  print st + ": " + text

def signal_handler(signal, frame):
    """Handles SIGTERM and gracefully exits"""
    reportOut("Got SIGTERM")  
    done = True
    sys.exit(0)
    
def mainLoop():
  done = False

  while not done:
    if 6 < datetime.datetime.now().hour < 18:
      try:  
        r = s.get('https://api.robinpowered.com/v1.0/spaces/' + str(_SPACEID))

        if r.status_code == requests.codes['\o/']:
          if r.json()['data']['current_event']:
          reportOut("Meeting found - light on")
          explorerhat.output.one.on() 
          else:
          explorerhat.output.one.off() 
        else:
          reportOut(r.json()['meta']['message'])
      except requests.exceptions.ConnectTimeout as e:
        reportOut("Server connection timed out")  
      except requests.exceptions.ReadTimeout as e:
        reportOut("Read timed out")
      except requests.exceptions.HTTPError as e:
        reportOut("HTTP error from server: " + e.message)
      except:
        reportOut("Other exception caught")
    else:
      explorerhat.output.one.off()    
    
    time.sleep(_INTERVAL) 

# setup HTTP session for the Robin API
s = requests.Session()
s.headers.update({'Authorization':'Access-Token ' + str(_ACCESSTOKEN)})

"""Upstart issues a SIGTERM when it stops this job. We need to handle it gracefully to set down the ExplorerHAT card"""
signal.signal(signal.SIGTERM, signal_handler)

mainLoop()