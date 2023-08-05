#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import random
import ikabot.config as config
from ikabot.web.sesion import get
from ikabot.helpers.pedirInfo import read
from ikabot.helpers.gui import enter

def sendToBot(s, msg, Token=False):
	if Token is False:
		msg = '{}\n{}'.format(config.infoUser, msg)
	with open(config.telegramFile, 'r') as filehandler:
		text = filehandler.read()
		(botToken, chatId) = text.splitlines()
		get('https://api.telegram.org/bot{}/sendMessage'.format(botToken), params={'chat_id': chatId, 'text': msg})

def telegramFileValido():
	with open(config.telegramFile, 'r') as filehandler:
		text = filehandler.read()
	rta = re.search(r'\d{6,}:[A-Za-z0-9_-]{34,}\n\d{8,9}', text)
	return rta is not None

def botValido(s):
	if telegramFileValido():
		return True
	else:
		print('Debe proporcionar las credenciales válidas para comunicarse por telegram.')
		print('Se requiere del token del bot a utilizar y de su chat_id')
		print('Para más informacion sobre como obtenerlos vea al readme de https://github.com/santipcn/ikabot')
		rta = read(msg='¿Porporcionará las credenciales ahora? [y/N]', values=['y','Y','n', 'N', ''])
		if rta.lower() != 'y':
			return False
		else:
			botToken = read(msg='Token del bot:')
			chat_id = read(msg='Chat_id:')
			with open(config.telegramFile, 'w') as filehandler:
				filehandler.write(botToken + '\n' + chat_id)
			rand = random.randint(1000, 9999)
			sendToBot(s, 'El token a ingresar es:{:d}'.format(rand), Token=True)
			rta = read(msg='Se envio un mensaje por telegram, ¿lo recibió? [Y/n]', values=['y','Y','n', 'N', ''])
			if rta.lower() == 'n':
				with open(config.telegramFile, 'w') as file:
					pass
				print('Revíse las credenciales y vuelva a proveerlas.')
				enter()
				return False
			else:
				recibido = read(msg='Ingrese el token recibido mediante telegram:', digit=True)
				if rand != recibido:
					with open(config.telegramFile, 'w') as file:
						pass
					print('El token es incorrecto')
					enter()
					return False
				else:
					print('El token es correcto.')
					enter()
					return True
