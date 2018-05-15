from PIL import Image
if answ[1] == 'кек':
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
		image_obj = Image.open('tmp/attachment.jpg')
		try:
			if answ[2] == 'лол':
				image2 = image_obj.crop([0,0,int(image_obj.size[0]/2),int(image_obj.size[1])])
				image2 = image2.transpose(Image.FLIP_LEFT_RIGHT)
				image_obj.paste(image2,(int(image_obj.size[0]/2),0))
				image_obj.save('tmp/kek.jpg')
				sendpic('kek.jpg','',toho,'')
		except IndexError:
			image2 = image_obj.transpose(Image.FLIP_LEFT_RIGHT)
			image2 = image2.crop([0,0,int(image_obj.size[0]/2),int(image_obj.size[1])])
			image2 = image2.transpose(Image.FLIP_LEFT_RIGHT)
			image_obj = image_obj.transpose(Image.FLIP_LEFT_RIGHT)
			image_obj.paste(image2,(int(image_obj.size[0]/2),0))
			image_obj.save('tmp/kek.jpg')
			sendpic('kek.jpg','',toho,'')
	except KeyError:
		apisay('Пикчу то вставь',toho,torep)