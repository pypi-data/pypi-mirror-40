#!/usr/bin/env python3

'''
@author: dz

Listen to all traffic on MQTT/UDP, pump updates to OpenHAB

Based on examples from https://github.com/openhab/openhab1-addons/wiki/Samples-REST

'''

# will work even if package is not installed
import sys
sys.path.append('..')
#sys.path.append('../mqttudp')

#import threading
import requests
#import time
import mqttudp.engine
import mqttudp.config as cfg

import mqttudp.openhab as openhab

cfg.setGroup('openhab-gate')


#OPENHAB_HOST="smart."
#OPENHAB_PORT="8080"
#OPENHAB_HOST = cfg.config.get('openhab-gate','host' )
#OPENHAB_PORT = cfg.config.get('openhab-gate','port' )


oh = openhab.RestIO()
oh.set_host( cfg.get('host' ) )
oh.set_port( cfg.get('port' ) )




#def broker_listen_thread(bclient):
#    bclient.loop_forever()
'''

def polling_header(atmos_id):
    """ Header for OpenHAB REST request - polling """
#    self.auth = base64.encodestring('%s:%s'%(self.username, self.password)).replace('\n', '')
    return {
#        "Authorization" : "Basic %s" % self.cmd.auth,
        "X-Atmosphere-Transport" : "long-polling",
        "X-Atmosphere-tracking-id" : atmos_id,
        "X-Atmosphere-Framework" : "1.0",
        "Accept" : "application/json"
        }

def basic_header():
    """ Header for OpenHAB REST request - standard """
#    self.auth = base64.encodestring('%s:%s'%(self.username, self.password)).replace('\n', '')
    return {
#            "Authorization" : "Basic %s" %self.auth,
            "Content-type": "text/plain"
           }



def post_command( key, value ):
    """ Post a command to OpenHAB - key is item, value is command """
    url = 'http://%s:%s/rest/items/%s'%(OPENHAB_HOST, OPENHAB_PORT, key)
    req = requests.post(url, data=value,
                            headers=basic_header())
    if (req.status_code != requests.codes.ok) and (req.status_code != 201):
        print( "Can't reach "+url+" code="+str(req.status_code)+", text '"+req.text+"'" )
        #req.raise_for_status()



def put_status( key, value ):
    """ Put a status update to OpenHAB  key is item, value is state """
    url = 'http://%s:%s/rest/items/%s/state'%(OPENHAB_HOST, OPENHAB_PORT, key)
    req = requests.put(url, data=value, headers=basic_header())
    if req.status_code != requests.codes.ok:
        print( "Can't reach "+url )
        #req.raise_for_status()     

'''

last = {}
def recv_packet_from_udp(ptype,topic,value,pflags,addr):
    if ptype != "publish":
        return
    if last.__contains__(topic) and last[topic] == value:
        return
    last[topic] = value
    print( topic+"="+value )
    #put_status(topic, value)
    oh.post_command(topic, value)


if __name__ == "__main__":
    print( "Will resend all the MQTT/UDP traffic to OpenHAB host " + cfg.get('host' ) )
    mqttudp.engine.listen(recv_packet_from_udp)
#    put_status( "PLK0_Va", "222" )











