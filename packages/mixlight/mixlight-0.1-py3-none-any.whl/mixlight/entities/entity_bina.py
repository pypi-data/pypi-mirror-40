

import logging

PREFIX = 'hass'
PLATFORM = 'binary_sensor'

TOPIC_CONFIG = "hass/%s/%s/config"
PAYLOAD_CONFIG = '{"name": "%s", "unique_id": "%s.%s", "device_class": "motion" }'

TOPIC_STATE = "hass/%s/%s/state"
PAYLOAD_STATE = '%s'


class entity_Bina():

  def __init__(self, id, addr, nr, name, type, linker):
    self.id = id
    self.addr = addr
    self.number = nr
    self.name = name
    self.linker = linker
    
  def create(self):
    if self.linker.client is None:
      return
    payload = PAYLOAD_CONFIG % (self.name, PLATFORM, self.id)
    rc = self.linker.client.publish(TOPIC_CONFIG % (PLATFORM, self.id), payload, 1, True)
    rc.wait_for_publish()
    self.linker.client.will_set(TOPIC_CONFIG % (PLATFORM, self.id), None, 1, True)
    print (self.id, ' CREATE: ', payload)
    self.write()
    
  def delete(self):
    if self.linker.client is None:
      return
    rc = self.linker.client.publish(TOPIC_CONFIG % (PLATFORM, self.id), None, 1, True)
    rc.wait_for_publish()
    print (self.id, ' DELETE: ')
    
  def get(self):
    return self.linker.boards[self.addr].buttons[self.number]  
    
  def set(self, *data):
    pass

  def read(self, topic, values):
    pass

  def write(self):
    if self.linker.client is None:
      return
    payload = "OFF"
    if self.get() > 0:
      payload = "ON"
    self.linker.client.publish(TOPIC_STATE % (PLATFORM, self.id), payload, 1, True)
        
        