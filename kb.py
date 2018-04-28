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
kb_name = ['kb','кб','кл','кч']
def apisay(text,toho,torep):
	param = (('v', '5.68'), ('peer_id', toho),('access_token',token),('message',text),('forward_messages',torep))
	result = requests.post('https://api.vk.com/method/messages.send', data=param)
	return result.text
print('Инициализация лонгполла завершена')
data = requests.get('https://api.vk.com/method/messages.getLongPollServer?access_token='+str(token)+'&v=5.68&lp_version=2').text
data = json.loads(data)['response']
def evalcmds(directory):
	dir = os.listdir(directory)
	#print(dir)
	for plugnum in range(len(dir)):
		exec(open(directory+'/'+str(dir[plugnum]),'r').read())
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
					open('system/msgs','a+').write(str(result)+'\n')
					result[5] = result[5].lower()
					#print(result[5])
					answ = result[5].split(' ')
					kb_cmd = json.loads(open('system/cmds','r').read())
					#print(kb_cmd['default'])
					if len(answ) > 1:
						if ((answ[0] in kb_name) and (answ[1] in kb_cmd["default"]) or (answ[1] in kb_cmd["vip"])):
							toho = result[3]
							torep = result[1]
							if (toho < 2000000000):
								userid = toho
							else:
								userid = result[6]['from']
							print('[Упоминание кб в '+str(toho)+']')
							answ_text = result[5].split(' ')
							if len(answ_text) >2:
								answ_text.remove(answ_text[0])
								answ_text.remove(answ_text[0])
							else:
								answ_text = ''
							answ_text = ' '.join(answ_text)
							try:
								thr = threading.Thread(target=evalcmds,args=('plugins/default',))
								thr.start()
							except KeyError:
								pass
							viplist = json.loads(open('system/vip','r').read())
							#print(userid,viplist)
							#print(viplist[0])
							if str(userid) in viplist:
								try:
									thr1 = threading.Thread(target=evalcmds,args=('plugins/vip',))
									thr1.start()
								except KeyError:
									pass
							else:
								if answ[1] in kb_cmd['vip']:
									apisay('И куда это мы лезем?)',toho,torep)
						if ((answ[0] in kb_name) and (answ[1] not in kb_cmd["default"]) and (answ[1] not in kb_cmd["vip"])):
							blacklistcmds = ['видео','музыка','vox','гиф']
							if answ[1] not in blacklistcmds:
								answtext = result[5].split(' ')
								answtext.remove(answtext[0])
								answtext = ' '.join(answtext)
								param = (('q',answtext),('adminname','кекер'))
								ret = requests.post('https://isinkin-bot-api.herokuapp.com/1/talk',data=param).json()
								apisay(ret['text'],result[3],result[1])
	except Exception as error:
		print(error)
	data['ts'] = response['ts'] 
