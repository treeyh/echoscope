# -*- coding: UTF-8 -*-


import logging

__log_path = ''
__logger = False

def log_init(path:str):
  global __logger
  
  if True == __logger:
    return
  __logger = True

  fmt = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s'
  consoleLog = logging.StreamHandler()
  consoleLog.setLevel(logging.INFO)

  if path != None and path != '':
    fileLog = logging.FileHandler(path)
    fileLog.setLevel(logging.INFO)
    logging.basicConfig(handlers=[consoleLog,fileLog], level=logging.INFO, format=fmt)
  else:
    logging.basicConfig(handlers=[consoleLog], level=logging.INFO, format=fmt)
