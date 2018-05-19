if answ[1] == '63':
	if answ_text.split(' ')[0] in kb_name:
		r34text = ''
	else:
		r34text = answ_text
	try:
		try:
			r34text = r34text.replace(' ','+')
			blacklist = '-fur+-darling_in_the_franxx+-furry+-dragon+-guro+-animal_penis+-animal+-wolf+-fox+-webm+-my_little_pony+-monster*+-3d+-animal*+-ant+-insects+-mammal+-horse+-blotch+-deer+-real*+-shit+-everlasting_summer+-copro*+-wtf+'
			parse = untangle.parse('http://rule63.xxx/index.php?page=dapi&s=post&q=index&limit=100&tags='+blacklist+str(r34text))
			randnum = random.randint(0,len(parse.posts.post))
			#print(parse.posts.post[randnum])
			mess = 'Дрочите на здоровье<br>('+str(randnum)+'/'+str(len(parse.posts.post))+')<br>----------<br>Остальные теги: '+parse.posts.post[randnum]['tags']
			parse = parse.posts.post[randnum]['file_url']
			#if parse.find('img.rule34')<0:
				#parse = parse.replace('rule63.xxx','oj2wyzjwgmxhq6dy.cmle.ru')
				#parse = parse.replace('https','http')
				#print(parse)
				#apisay(parse,toho,torep)
			#print(parse)
			pic = requests.get(parse).content
			#print(len(pic))
			if not os.path.exists('tmp'):
				os.mkdir('tmp')
			open('tmp/rule34.jpg','wb').write(pic)
			############################################
			ret = requests.get('https://api.vk.com/method/photos.getMessagesUploadServer?access_token={access_token}&v=5.68'.format(access_token=token)).json()
			with open('tmp/rule34.jpg', 'rb') as f:
				ret = requests.post(ret['response']['upload_url'], files={'file1': f}).text
			ret = json.loads(ret)
			#print(ret)
			ret = requests.get('https://api.vk.com/method/photos.saveMessagesPhoto?v=5.68&album_id=-3&server='+str(ret['server'])+'&photo='+ret['photo']+'&hash='+str(ret['hash'])+'&access_token='+token).text
			ret = json.loads(ret)
			#print(ret)
			ret = requests.get('https://api.vk.com/method/messages.send?attachment=photo'+str(ret['response'][0]['owner_id'])+'_'+str(ret['response'][0]['id'])+'&message='+mess+'&v=5.68&peer_id='+str(toho)+'&access_token='+str(token))
			#print(ret)
		except UnicodeEncodeError:
			apisay('Ничего не найдено :(',toho,torep)
	except AttributeError:
		apisay('Ничего не найдено :(',toho,torep)
