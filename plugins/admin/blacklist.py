if answ[1] == 'givebl':
	param = (('v','5.68'),('access_token',token),('message_ids',torep))
	ret = requests.post('https://api.vk.com/method/messages.getById',data = param).text
	ret = json.loads(ret)['response']['items'][0]['fwd_messages'][0]['user_id']
	vips = json.loads(open('system/blacklist','r').read())
	vips.append(str(ret))
	open('system/blacklist','w').write(json.dumps(vips))
	apisay('Занесла в чс id'+str(ret),toho,torep)
if answ[1] == 'delbl':
	param = (('v','5.68'),('access_token',token),('message_ids',torep))
	ret = requests.post('https://api.vk.com/method/messages.getById',data = param).text
	ret = json.loads(ret)['response']['items'][0]['fwd_messages'][0]['user_id']
	vips = json.loads(open('system/blacklist','r').read())
	try:
		vips.remove(str(ret))
		open('system/blacklist','w').write(json.dumps(vips))
		apisay('Убрала из чс id'+str(ret),toho,torep)
	except ValueError:
		apisay('Такого юзера нет в списке',toho,torep)