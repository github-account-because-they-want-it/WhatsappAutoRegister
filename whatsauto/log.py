'''
Created on Jan 16, 2015
'''

import logging
from os import path

class WhatsappLogger(logging.Logger):
  
  def __init__(self, *args, **kwargs):
    super(WhatsappLogger, self).__init__(*args, **kwargs)
    self.setupLog()

  def setupLog(self):
    self.setLevel(logging.DEBUG)
    log_file_path = path.join(self.log_dir, "whatsapp.log")
    handler = logging.FileHandler(log_file_path)
    self.addHandler(handler)
    handler.setFormatter(logging.Formatter('%(levelname)s @ [%(asctime)s] :: %(message)s',
                                       datefmt="%Y-%m-%d %H:%M:%S"))