#!/usr/local/bin/python2.7
'''
Created on Jan 15, 2015
'''

__AUTHOR__ = "Mohammed Hamdy"

import logging
from argparse import ArgumentParser
from time import sleep
from os import walk as traverse_dir
from os import path, remove
from whatsauto.util import (make_registration_request, read_numbers_file, get_text_from_speech,
                            get_token, get_account_id)
from whatsauto.log import WhatsappLogger

def make_registration_requests(work_dir, speech_dir, wav_wait_secs=240, request_sleep=1, use_proxy=False):
  numbers_file = path.join(work_dir, "numbers.txt")
  number_generator = read_numbers_file(numbers_file)
  logger = WhatsappLogger(work_dir)
  for (country_code, phone, id_) in number_generator:
    logger.log(logging.DEBUG, "Registering {}-{}".format(country_code, phone))
    result = make_registration_request(country_code, phone, use_proxy)
    if result["status"] == "sent":
      logger.log(logging.INFO, "Request was successful. Waiting {} seconds".format(wav_wait_secs))
      # wait until wav file is retrieved
      sleep(wav_wait_secs)
      logger.log(logging.DEBUG, "Searching for wav with id : {}".format(id_))
      wav_file_found = False
      for (root_dir, dirshere, fileshere) in traverse_dir(speech_dir):
        for file_ in fileshere:
          if id_ in file_ and path.splitext(file_)[1].lower() == ".wav":
            logging.log(logging.INFO, "Found wav file <{}>".format(file_))
            complete_wav_path = path.join(root_dir, file_)
            regcode = get_text_from_speech(work_dir, complete_wav_path)
            token = get_token(work_dir)
            #account_id = get_account_id(work_dir, country_code+phone)
            #open(path.join(work_dir, "success.txt"), "at").write(country_code+phone + 
            #    "," + token + "," + account_id + "\n")
            remove(complete_wav_path)
            wav_file_found = True
            break
        if wav_file_found:
          break
      else:
        logger.log(logging.WARN, "Couldn't find file with suitable id")
    else: # unsuccessful number
      logger.log(logging.WARN, "Request was not successful. status '{}'".format(result["status"]))
      open(path.join(work_dir, result["status"] + ".txt"), "at").write(country_code+phone + "\n")
            
    # sleep between requests
    sleep(request_sleep)
    
if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("-s", "--speech_dir", help="the directory that contains .wav files")
  workdir_default = path.join(path.dirname(__file__), "workdir")
  parser.add_argument("-w", "--work_dir", default=workdir_default, help="folder that contains necessary files like numbers.txt, scripts and wav files")
  parser.add_argument("--wav_wait", type=int, default=240, help="time to wait for wav files to be downloaded (secs)")
  parser.add_argument("--req_sleep", type=int, default=1, help="time to sleep between whatsapp requests")
  parser.add_argument("--proxy", action="store_true")
  args = parser.parse_args()
  make_registration_requests(args.work_dir, args.speech_dir, args.wav_wait, args.req_sleep, use_proxy=args.proxy)
