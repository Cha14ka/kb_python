if (answ[1]=='кто'):	
					if (toho < 2000000000):
						apisay('В личной переписке это не работает. Лишь в конфе',toho,torep)
					else:
						resapi = toho-2000000000;
						text = answ
						param = (('v', '5.68'), ('chat_id',resapi),('access_token',token))
						res = requests.post('https://api.vk.com/method/messages.getChatUsers', data=param)
						res = json.loads(res.text)
						rand = random.randint(0,len(res['response'])-1)
						param = (('v', '5.68'), ('user_ids',res['response'][rand]),('access_token',token))
						name = requests.post('https://api.vk.com/method/users.get', data=param)
						name = json.loads(name.text)
						name = name['response'][0]['first_name']+' '+name['response'][0]['last_name']
						if (random.randint(0,1)==0):
							apisay('Есть вероятность что это - '+name,toho,torep)
						else:
							apisay('Я уверена это у нас '+name,toho,torep)