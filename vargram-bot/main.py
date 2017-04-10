#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging, sys
logging.basicConfig(
    format='%(asctime)s %(name)s: %(levelname)s: %(message)s',
    level=logging.INFO
)

import parse
from version import VERSION
from config import config
from bot import TelegramBot

if __name__ == '__main__':
  if len(sys.argv) > 1 and \
      (sys.argv[1] == '-v' or sys.argv[1] == '--version'):
    print('VarGram Bot\nVersion {}'.format(VERSION))
    sys.exit(0)

  bot = TelegramBot(config['token'])
  
  # function to wrap library call for parsing page
  def parsing():
    return parse.parse_page(
        config['mailman-url'].replace('$Y', '2017').replace('$M', 'April')
    )

  bot.initialize(
      parsing,
      {
        'name': config['group-name'],
        'id': config['group-id']
      },
      {
        'from': config['smtp-user'],
        'to': config['smtp-to'],
        'password': config['smtp-pass'],
        'server': config['smtp-address'],
        'port': config['smtp-port']
      }
  )

  logging.info('Starting bot!')
  bot.start(config['webhook-url'], config['webhook-port'])