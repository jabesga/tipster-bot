#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

group_of_interest = ['11','24','32']

def ver_pronosticos(sport):
    global group_of_interest
    data = requests.get('http://www.apuestasdeportivas.com/m/api/v1/pronosticos/')
    json_data = json.loads(data.content) # Array con todas las apuestas

    response_list = []

    for bet in json_data:
        
        if bet["txt_deporte"] == sport.capitalize():
            
            if bet["id_grupo"] in group_of_interest:
                
                message = ''

                message += bet["real_name"] + ':\n'
                if bet['txt_deporte'] == 'Futbol':
                    message += b'\xE2\x9A\xBD'.decode('utf-8')
                elif bet['txt_deporte'] == 'Tenis':
                    message += b'\xF0\x9F\x8E\xBE'.decode('utf-8')
                elif bet['txt_deporte'] == 'Beisbol':
                    message += b'\xE2\x9A\xBE'.decode('utf-8')
                elif bet['txt_deporte'] == 'Baloncesto':
                    message += b'\xF0\x9F\x8F\x80'.decode('utf-8')
                    
                message += ' ' + bet['txt_competicion'] + '\n'
                message += bet['name'] + '\n'
                message += bet['apuesta'] + ' @ ' + bet['cuota'] + '\n'
                message += bet['startdate']
                #if bet["id_grupo"] == '11':
                #    message += ' (Operación Tipster)'
                #if bet["id_grupo"] == '24':
                #    message += ' (Pronosticador Premium)'
                #if bet["id_grupo"] == '32':
                #    message += ' (Pronosticador Experto)'

                
                #print message
                response_list.append(message)
    
    return response_list

        