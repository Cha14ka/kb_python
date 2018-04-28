import urllib.parse
if answ[1] == 'скажи':
	if (answ_text == ''):
		apisay('А текст мб стоит вписать?)',toho,torep)
	else:
		answ_text = answ_text.replace('<br>','')
		key = 'c8694d7c-afff-48c1-9701-b10def466526'
		audio = requests.get('https://tts.voicetech.yandex.net/generate?&format=mp3&quality=hi&emotion=evil&key='+key+'&text='+str(urllib.parse.quote_plus(answ_text))).content
		#print(audio)
		open('tmp/audio.mp3','wb').write(audio)
		ret = requests.get('https://api.vk.com/method/docs.getMessagesUploadServer?type=audio_message&peer_id='+str(toho)+'&access_token={access_token}&v=5.68'.format(access_token=token)).json()
		#print(ret)
		if not os.path.exists('tmp'):
					os.mkdir('tmp')
		with open('tmp/audio.mp3', 'rb') as f:
			ret = requests.post(ret['response']['upload_url'], files={'file': f}).text
		ret = json.loads(ret)
		ret = requests.get('https://api.vk.com/method/docs.save?v=5.68&file='+ret['file']+'&title=vo&access_token='+token).text
		ret = json.loads(ret)
		#print(ret)
		ret = requests.get('https://api.vk.com/method/messages.send?attachment=doc'+str(ret['response'][0]['owner_id'])+'_'+str(ret['response'][0]['id'])+'&v=5.68&forward_messages='+str(torep)+'&peer_id='+str(toho)+'&access_token='+str(token))