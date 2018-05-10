# -*- coding: utf-8 -*- 
import sys
import threading
import traceback
import psutil
import requests
import json
import os
import random
import datetime
import untangle
import urllib.parse
token = open('system/token','r').read()
token = token.split('\n')[0]
kb_name = ['kb','кб','кл','кч']
def apisay(text,toho,torep):
	param = (('v', '5.68'), ('peer_id', toho),('access_token',token),('message',text),('forward_messages',torep))
	result = requests.post('https://api.vk.com/method/messages.send', data=param)
	return result.text
def exitgame():
	print(str(userid)+' покинул игру '+game_module['active_users'][str(userid)])
	del game_module['active_users'][str(userid)]
open('system/msgs','w').write('')
data = requests.get('https://api.vk.com/method/messages.getLongPollServer?access_token='+str(token)+'&v=5.68&lp_version=2').text
data = json.loads(data)['response']
def evalcmds(directory,toho,torep,answ):
	dir = os.listdir(directory)
	#print(dir)
	for plugnum in range(len(dir)):
		exec(open(directory+'/'+str(dir[plugnum]),'r').read())
game_module = open('system/game_module','r').read()
game_module = json.loads(game_module)
print('Инициализация бота завершена')
while True:
	try:
		response = requests.get('https://{server}?act=a_check&key={key}&ts={ts}&wait=20&mode=2&version=2'.format(server=data['server'], key=data['key'], ts=data['ts'])).json() 
		try: 
			updates = response['updates'];
		except KeyError:
			data = requests.get('https://api.vk.com/method/messages.getLongPollServer?access_token='+str(token)+'&v=5.68&lp_version=2').text
			data = json.loads(data)['response']
			continue
		if updates: 
			for result in updates: 
				if result[0] == 4:
					if (result[3] < 2000000000):
						userid = result[3]
					else:
						userid = result[6]['from']
					toho = result[3]
					torep = result[1]
					###game
					if (result[3] > 2000000000):
						if str(userid) in game_module['active_users']:
							answ_text = result[5].lower()
							print(str(userid)+' в игре '+game_module['active_users'][str(userid)])
							#print(game_module['games_info'][game_module['active_users'][userid]])
							def evalgames(answ_text,toho,torep):
								#print(game_module['games_info'][game_module['active_users'][userid]])
								#print(answ_text,toho,torep)
								exec(open(game_module['games_info'][game_module['active_users'][userid]],'r').read())
							thr = threading.Thread(target=evalgames,args=(answ_text,toho,torep))
							thr.start()
					###game
					open('system/msgs','a+').write(str(result)+'\n')
					result[5] = result[5].lower()
					answ = result[5].split(' ')
					kb_cmd = json.loads(open('system/cmds','r').read())
					#print(kb_cmd['default'])
					if len(answ) > 1:
						if (str(userid) not in game_module['active_users'] and (answ[0] in kb_name) and ((answ[1] in kb_cmd["default"]) or (answ[1] in kb_cmd["vip"]) or (answ[1] in kb_cmd["admin"]))):
							print('[Упоминание кб в '+str(toho)+']')
							answ_text = result[5].split(' ')
							if len(answ_text) >2:
								answ_text.remove(answ_text[0])
								answ_text.remove(answ_text[0])
							else:
								answ_text = ''
							answ_text = ' '.join(answ_text)
							try:
								thr = threading.Thread(target=evalcmds,args=('plugins/default',toho,torep,answ))
								thr.start()
							except KeyError:
								pass
							viplist = json.loads(open('system/vip','r').read())
							adminlist = json.loads(open('system/admin','r').read())
							if str(userid) in viplist:
								try:
									thr1 = threading.Thread(target=evalcmds,args=('plugins/vip',toho,torep,answ))
									thr1.start()
								except KeyError:
									pass
							else:
								if answ[1] in kb_cmd['vip']:
									apisay('Тебя нет в вайтлисте чтоб юзать эту команду, пуся',toho,torep)
							if str(userid) in adminlist:
								try:
									thr1 = threading.Thread(target=evalcmds,args=('plugins/admin',toho,torep,answ))
									thr1.start()
								except KeyError:
									pass
							else:
								if answ[1] in kb_cmd['admin']:
									apisay('До админки тебе ещё далеко',toho,torep)
						if ((answ[0] in kb_name) and (answ[1] not in kb_cmd["default"]) and (answ[1] not in kb_cmd["vip"]) and (answ[1] not in kb_cmd["admin"]) and (str(userid) not in game_module['active_users'])):
							blacklistcmds = ['гиф','преакт','цитата','гцитата']
							if answ[1] not in blacklistcmds:
								answtext = result[5].split(' ')
								answtext.remove(answtext[0])
								answtext = ' '.join(answtext)
								param = (('q',answtext),('adminname','кекер'))
								ret = requests.post('https://isinkin-bot-api.herokuapp.com/1/talk',data=param).json()
								apisay(ret['text'],result[3],result[1])
	except Exception as error:
		adminlist = json.loads(open('system/admin','r').read())
		print(error)
		apisay(error,adminlist[0],'')
	data['ts'] = response['ts'] 
