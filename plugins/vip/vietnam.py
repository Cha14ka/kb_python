from PIL import Image
if answ[1] == 'вьетнам':
	param = (('v','5.68'),('access_token',token),('message_ids',torep))
	ret = requests.post('https://api.vk.com/method/messages.getById',data = param).text
	ret = json.loads(ret)
	try:
		ret = ret['response']['items'][0]['attachments'][0]['photo']
		retkeys = list(ret.keys())
		numlist = 0
		for i in range(len(retkeys)):
			if retkeys[i].find('photo') != -1:
				if int(retkeys[i].split('_')[1]) > numlist:    
					numlist = int(retkeys[i].split('_')[1])
		ret = ret['photo_'+str(numlist)]
		ret = requests.get(ret).content
		open('tmp/attachment.jpg','wb').write(ret)
		pic1 = Image.open('tmp/vietnam.png')
		pic2 = Image.open('tmp/attachment.jpg')
		pic1 = pic1.resize(pic2.size)
		pic2 = pic2.convert('RGBA')
		pic3 = Image.alpha_composite(pic2,pic1)
		pic3.save('tmp/vietnam.jpg')
		ret = requests.get('https://api.vk.com/method/photos.getMessagesUploadServer?access_token={access_token}&v=5.68'.format(access_token=token)).json()
		with open('tmp/vietnam.jpg', 'rb') as f:
			ret = requests.post(ret['response']['upload_url'], files={'file1': f}).text
		ret = json.loads(ret)
		ret = requests.get('https://api.vk.com/method/photos.saveMessagesPhoto?v=5.68&album_id=-3&server='+str(ret['server'])+'&photo='+ret['photo']+'&hash='+str(ret['hash'])+'&access_token='+token).text
		ret = json.loads(ret)
		ret = requests.get('https://api.vk.com/method/messages.send?attachment=photo'+str(ret['response'][0]['owner_id'])+'_'+str(ret['response'][0]['id'])+'&v=5.68&peer_id='+str(toho)+'&access_token='+str(token))
	except KeyError:
		apisay('Пикчу то вставь',toho,torep)