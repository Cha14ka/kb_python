if answ[1] == 'бура':
	if answ_text.split(' ')[0] in kb_name:
		r34text = ''
	else:
		r34text = answ_text
	try:
		try:
			parse = untangle.parse('http://safebooru.org/index.php?page=dapi&s=post&q=index&limit=100&tags='+str(r34text))
			randnum = random.randint(0,len(parse.posts.post))
			mess = 'Бурятские артики по запросу<br>('+str(randnum)+'/'+str(len(parse.posts.post))+')<br>----------<br>Остальные теги: '+parse.posts.post[randnum]['tags']
			parse = parse.posts.post[randnum]['file_url']
			parse = parse.replace('//','http://')
			pic = requests.get(parse).content
			if not os.path.exists('tmp'):
					os.mkdir('tmp')
			open('tmp/booru.jpg','wb').write(pic)
			############################################
			ret = requests.get('https://api.vk.com/method/photos.getMessagesUploadServer?access_token={access_token}&v=5.68'.format(access_token=token)).json()
			with open('tmp/booru.jpg', 'rb') as f:
				ret = requests.post(ret['response']['upload_url'], files={'file1': f}).text
			ret = json.loads(ret)
			ret = requests.get('https://api.vk.com/method/photos.saveMessagesPhoto?v=5.68&album_id=-3&server='+str(ret['server'])+'&photo='+ret['photo']+'&hash='+str(ret['hash'])+'&access_token='+token).text
			ret = json.loads(ret)
			ret = requests.get('https://api.vk.com/method/messages.send?attachment=photo'+str(ret['response'][0]['owner_id'])+'_'+str(ret['response'][0]['id'])+'&message='+mess+'&v=5.68&peer_id='+str(toho)+'&access_token='+str(token))
		except UnicodeEncodeError:
			apisay('Ничего не найдено :(',toho,torep)
	except AttributeError:
		apisay('Ничего не найдено :(',toho,torep)