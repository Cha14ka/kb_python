if 'source_act' in result[6]:
	if result[6]['source_act'] == 'chat_invite_user':
		param = (('v', '5.68'), ('user_ids',result[6]['source_mid']),('access_token',token))
		name = requests.post('https://api.vk.com/method/users.get', data=param)
		name = json.loads(name.text)
		name = name['response'][0]['first_name']+' '+name['response'][0]['last_name']
		apisay('🌝🌝🌝🌝ПРИВЕТ 🐓'+name+'🐓🌚🌚🌚🌚<br>🙋В этой беседе вам отсосёт Кариночка и остальные 💩говноботы💩🙋<br>Напиши "кб помощь" чтобы узнать команды бота<br>Принимаю заявки в течении 30 секунд!',toho,'')