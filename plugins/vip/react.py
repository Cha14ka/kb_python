import re
if answ[1] == 'реакт':
	count = requests.get('http://reactor.cc/search/'+answ_text.replace(' ','+')).text
	count = re.split('<a href=\'/search/',count)
	count = count[len(count)-2]
	count = count.split('>')[1].replace('</a','')
	count = random.randint(0,int(count))
	parse = requests.get('http://reactor.cc/search?q='+answ_text.replace(' ','+')+'/'+str(count)).text
	strings = ['class="prettyPhotoLink" rel="prettyPhoto"><img src="', '" width="']
	try:
		parse = re.split(strings[0],parse)
		randint = random.randint(1,len(parse))
		parse = re.split(strings[1],parse[randint])[0]
		mess = 'Дрочи давай'
		pic = requests.get(parse).content
		open('tmp/preact.jpg','wb').write(pic)
		ret = requests.get('https://api.vk.com/method/photos.getMessagesUploadServer?access_token={access_token}&v=5.68'.format(access_token=token)).json()
		with open('tmp/preact.jpg', 'rb') as f:
			ret = requests.post(ret['response']['upload_url'], files={'file1': f}).text
		ret = json.loads(ret)
		ret = requests.get('https://api.vk.com/method/photos.saveMessagesPhoto?v=5.68&album_id=-3&server='+str(ret['server'])+'&photo='+ret['photo']+'&hash='+str(ret['hash'])+'&access_token='+token).text
		ret = json.loads(ret)
		ret = requests.get('https://api.vk.com/method/messages.send?attachment=photo'+str(ret['response'][0]['owner_id'])+'_'+str(ret['response'][0]['id'])+'&message='+mess+'&v=5.68&peer_id='+str(toho)+'&access_token='+str(token))
	except IndexError:
		apisay('Ничего не найдено :(',toho,torep)