if answ[1] == 'givevip':
	param = (('v','5.68'),('access_token',token),('message_ids',torep))
	ret = requests.post('https://api.vk.com/method/messages.getById',data = param).text
	ret = json.loads(ret)['response']['items'][0]['fwd_messages'][0]['user_id']
	vips = json.loads(open('system/vip','r').read())
	vips.append(str(ret))
	open('system/vip','w').write(json.dumps(vips))
	apisay('Выдала випку id'+str(ret),toho,torep)
if answ[1] == 'delvip':
	param = (('v','5.68'),('access_token',token),('message_ids',torep))
	ret = requests.post('https://api.vk.com/method/messages.getById',data = param).text
	ret = json.loads(ret)['response']['items'][0]['fwd_messages'][0]['user_id']
	vips = json.loads(open('system/vip','r').read())
	try:
		vips.remove(str(ret))
		open('system/vip','w').write(json.dumps(vips))
		apisay('Забрала випку ук id'+str(ret),toho,torep)
	except ValueError:
		apisay('Такого юзера нет в списке',toho,torep)