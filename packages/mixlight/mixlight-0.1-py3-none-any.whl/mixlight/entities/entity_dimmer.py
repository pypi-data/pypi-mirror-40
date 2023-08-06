

import logging

PREFIX = 'hass'
PLATFORM = 'light'

TOPIC_CONFIG = "hass/%s/%s/config"
PAYLOAD_CONFIG = '{"name": "%s", "unique_id": "%s.%s", "command_topic": "hass/%s/%s/set", "schema": "json", "brightness": "true" }'

TOPIC_STATE = "hass/%s/%s/state"
PAYLOAD_STATE = '{ "brightness": %s, "state": "%s" }'

TOPIC_SET = "hass/%s/%s/set"


class entity_Dimmer():

  def __init__(self, id, addr, name, type, linker):
    self.id = id
    self.addr = addr
    self.name = name
    self.linker = linker
    self.brightness = 255

  def create(self):
    if self.linker.client is None:
      return
    payload = PAYLOAD_CONFIG % (self.name, PLATFORM, self.id, PLATFORM, self.id)
    rc = self.linker.client.publish(TOPIC_CONFIG % (PLATFORM, self.id), payload, 1, True)
    rc.wait_for_publish()
    self.linker.client.will_set(TOPIC_CONFIG % (PLATFORM, self.id), None, 1, True)
    self.linker.client.subscribe(TOPIC_SET % (PLATFORM, self.id))
    print (self.id, ' CREATE: ', payload)
    self.write()
    
  def delete(self):
    if self.linker.client is None:
      return
    self.linker.client.unsubscribe(TOPIC_SET % (PLATFORM, self.id))
    rc = self.linker.client.publish(TOPIC_CONFIG % (PLATFORM, self.id), None, 1, True)
    rc.wait_for_publish()
    print (self.id, ' DELETE: ')
    
  def get(self):
    return self.linker.output.get(self.addr)  
    
  def set(self, *data):
    self.linker.output.set(self.addr, data[0])
    self.write()
    
  def read(self, topic, values):
    if topic == (TOPIC_SET % (PLATFORM, self.id)):    
      if 'brightness' in values:
        self.brightness = values['brightness']
      if 'state' in values:
        if values['state'] == "ON":
          self.set(self.brightness)
        elif values['state'] == "OFF":
          self.set(0)
    
  def write(self):
    if self.linker.client is None:
      return
    payload = "OFF"
    if self.get() > 0:
      payload = "ON"
    payload = PAYLOAD_STATE % (self.get(), payload)  
    self.linker.client.publish(TOPIC_STATE % (PLATFORM, self.id), payload, 1, True)

  def toggle(self):
    if self.get() > 0:
      self.set(0)
    else:
      self.set(self.brightness)      
        