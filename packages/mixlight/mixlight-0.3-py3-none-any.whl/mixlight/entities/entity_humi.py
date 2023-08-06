

import logging

PREFIX = 'hass'
PLATFORM = 'sensor'

TOPIC_CONFIG = "hass/%s/%s/config"
PAYLOAD_CONFIG = '{"name": "%s", "unique_id": "%s.%s", "unit_of_measurement": "%%" }'

TOPIC_STATE = "hass/%s/%s/state"
PAYLOAD_STATE = '%s'


class entity_Humi():

  def __init__(self, id, addr, name, type, linker):
    self.id = id
    self.addr = addr
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
    return self.linker.boards[self.addr].humi  
    
  def set(self, *data):
    pass

  def read(self, topic, values):
    pass

  def write(self):
    if self.linker.client is None:
      return
    payload = "0"
    if self.get() > 0:
      payload = str(self.get())
    self.linker.client.publish(TOPIC_STATE % (PLATFORM, self.id), payload, 1, True)
        
        