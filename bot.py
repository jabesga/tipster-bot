#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import signal
import sys

import apuestas_deportivas

from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')

token = parser.get('Config', 'token') # TIPSTERBOT

offset = None

def signal_handler(signal, frame):
    print('Bot stopped. Ctrl+C pressed!')
    sys.exit(0)

def checkUpdates():
    global offset
    response = requests.post(
        url='https://api.telegram.org/bot{0}/{1}'.format(token, 'getUpdates'),
        data={'offset': offset}
    ).json()
    
    if response['ok'] == True: # If request is successfull and...
        if response['result']: # ...if there are new updates
            
            if offset == None: # Update the offset
                offset = response['result'][0]['update_id']
                print 'Offset updated! (%s)' % str(offset)

            if response['result'][0]['update_id'] == offset:
                message = response['result'][0]['message']
                print message # Print the message
                
                offset += 1 # Update the offset
                return message
        # else:
            #print 'No new messages'
    else:
        print 'Unsuccessful request. Error code: %s. %s' % (response['error_code'], response['description'])
    
def sendMessage(chat_id, text):
    response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(token, 'sendMessage'),
            data={'chat_id': chat_id, 'text': text}
        ).json()

def sendSticker(chat_id, file_id):
    response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(token, 'sendSticker'),
            data={'chat_id': chat_id, 'sticker': file_id}
        ).json()

def sendPhoto_using_string(chat_id, file_id):
    response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(token, 'sendPhoto'),
            data={'chat_id': chat_id, 'photo': file_id}
        ).json()

def sendPhoto_using_file(chat_id, photo):

    response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(token, 'sendPhoto'),
            data={'chat_id': chat_id},
            files={'photo': (photo, open('images/' + photo, "rb"))},
        ).json()
    print response

import time
def is_a_command(message):
    splittedMessage = message['text'].split()

    if splittedMessage[0] == '/pronosticos' or splittedMessage[0] == '/pronosticos@TipsterBot':
        if len(splittedMessage) == 1:
            sendMessage(message['chat']['id'], '/pronosticos <Futbol|Tenis|Baloncesto|Beisbol>')
        elif len(splittedMessage) == 2:
            if splittedMessage[1].lower() in ['futbol','tenis','baloncesto','beisbol']:
                response_list = apuestas_deportivas.ver_pronosticos(splittedMessage[1])
                if response_list:
                    for response in response_list:
                        sendMessage(message['chat']['id'], response)
                else:
                    sendMessage(message['chat']['id'], 'No se han encontrado pronosticos')

import unicodedata

signal.signal(signal.SIGINT, signal_handler)

print 'Bot initialized!'

while True:

    message = checkUpdates()

    if message != None:
        if 'new_chat_participant' in message:
            pass

        if 'left_chat_participant' in message:
            pass

        if 'text' in message:
            is_a_command(message)
