# -*- coding: utf-8 -*- 
import sys, threading, traceback, psutil, requests,json, os, random, datetime, untangle, urllib.parse, time, html
from datetime import timedelta
#Файлы системы бота
token = json.loads(open('system/info','r').read())['token']
kb_name = json.loads(open('system/info','r').read())['names']
game_module = json.loads(open('system/game_module','r').read())
botstat = json.loads(open('system/stats','r').read())
cmds_at_start = botstat['start']
#Функции
def apisay(text,toho,torep):
	param = {'v':'5.68','peer_id':toho,'access_token':token,'message':text,'forward_messages':torep}
	result = requests.post('https://api.vk.com/method/messages.send', data=param)
	return result.text
def exitgame():
	print(str(userid)+' покинул игру '+game_module['active_users'][str(userid)])
	del game_module['active_users'][str(userid)]
def sendpic(pic,mess,toho,torep):
	ret = requests.get('https://api.vk.com/method/photos.getMessagesUploadServer?access_token={access_token}&v=5.68'.format(access_token=token)).json()
	with open('tmp/'+pic, 'rb') as f:
		ret = requests.post(ret['response']['upload_url'],files={'file1': f}).text
	ret = json.loads(ret)
	ret = requests.get('https://api.vk.com/method/photos.saveMessagesPhoto?v=5.68&album_id=-3&server='+str(ret['server'])+'&photo='+ret['photo']+'&hash='+str(ret['hash'])+'&access_token='+token).text
	ret = json.loads(ret)
	requests.get('https://api.vk.com/method/messages.send?attachment=photo'+str(ret['response'][0]['owner_id'])+'_'+str(ret['response'][0]['id'])+'&message='+mess+'&v=5.68&forward_messages='+str(torep)+'&peer_id='+str(toho)+'&access_token='+str(token))
def evalcmds(filename,toho,torep,answ):
	exec(open(filename,'r').read())
#Лонгполл
data = requests.get('https://api.vk.com/method/messages.getLongPollServer?access_token='+str(token)+'&v=5.68&lp_version=2').text
data = json.loads(data)['response']
start_time = time.monotonic()
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
		#Обработка сообщений
		if updates: 
			for result in updates:
				if result[0] == 4:
					toho = result[3]
					torep = result[1]
					exec(open('system/core.py','r').read())
					if (result[3] < 2000000000):
						userid = result[3]
					else:
						userid = result[6]['from']
					blacklist = json.loads(open('system/users','r').read())['blacklist']
					answ = result[5].split(' ')
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
							threading.Thread(target=evalgames,args=(answ_text,toho,torep)).start()
					###game
					kb_cmd = json.loads(open('system/cmds','r').read())
					if len(answ) > 1:
						answ[0] = answ[0].lower()
						answ[1] = answ[1].lower()
						if (str(userid) not in game_module['active_users'] and (str(userid) not in blacklist) and (answ[0] in kb_name) and ((answ[1] in kb_cmd["default"]) or (answ[1] in kb_cmd["vip"]) or (answ[1] in kb_cmd["admin"]))):
							print('[Упоминание кб в '+str(toho)+']')
							cmds_at_start = cmds_at_start+1
							botstat['alltime'] = botstat['alltime']+1
							if userid not in botstat['users']:
								botstat['users'].append(userid)
							open('system/stats','w').write(json.dumps(botstat))
							answ_text = result[5].split(' ')
							if len(answ_text) >2:
								answ_text.remove(answ_text[0])
								answ_text.remove(answ_text[0])
							else:
								answ_text = ''
							answ_text = ' '.join(answ_text)
							answ_text = html.unescape(answ_text)
							users = json.loads(open('system/users','r').read())
							viplist = users['vip']
							adminlist = users['admin']
							if answ[1] in kb_cmd['default']:
								threading.Thread(target=evalcmds,args=('plugins/default/'+kb_cmd['default'][answ[1]],toho,torep,answ)).start()
							if answ[1] in kb_cmd['vip']:
								if str(userid) in viplist:
									threading.Thread(target=evalcmds,args=('plugins/vip/'+kb_cmd['vip'][answ[1]],toho,torep,answ)).start()
								else:
									apisay('У тебя нет випки чтоб юзать эту команду, пуся',toho,torep)
									#print(answ[1])
									#print(kb_cmd["vip"])
							if answ[1] in kb_cmd['admin']:
								if str(userid) in adminlist:
									threading.Thread(target=evalcmds,args=('plugins/admin/'+kb_cmd['admin'][answ[1]],toho,torep,answ)).start()
								else:
									apisay('До админки тебе ещё далеко',toho,torep)
						if (str(userid) not in game_module['active_users'] and (str(userid) not in blacklist) and (answ[0] in kb_name) and (answ[1] not in kb_cmd["default"]) and (answ[1] not in kb_cmd["vip"]) and (answ[1] not in kb_cmd["admin"])):
							blacklistcmds = ['гиф','гцитата']
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