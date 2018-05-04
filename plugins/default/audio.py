if answ[1] == 'музыка':
	param = (('v', '5.29'), ('q',answ_text),('count','200'),('sort','2'),('access_token',token),('forward_messages',torep),('audio_id','456239510'))
	res = requests.post('https://api.vk.com/method/audio.search', data=param)
	#apisay(res.text,toho,torep)
	res = json.loads(res.text)
	print(res)
	if (res['response']['count'] != 0):
		fcount=0
		info = ''
		for k in range(len(res['response']['items'])-1):
			if(fcount == 10):
				break
			info = info+'audio'+str(res['response']['items'][k]['owner_id'])+'_'+str(res['response']['items'][k]['id'])+','
			fcount = fcount+1
		param = (('v', '5.74'), ('peer_id',toho),('access_token',token),('forward_messages',torep),('message','Музыка по вашему запросу'),('attachment',info))
		requests.post('https://api.vk.com/method/messages.send', data=param)
		#apisay(ret.text,toho,torep)
	else:
		apisay('Музыка по запросу не найдена',toho,torep)