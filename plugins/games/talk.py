if answ_text == 'exit':
	exitgame()
	apisay('Ты вышел из общения',toho,torep)
else:
	param = (('q',answ_text),('adminname','кекер'))
	ret = requests.post('https://isinkin-bot-api.herokuapp.com/1/talk',data=param).json()
	apisay(ret['text'],toho,torep)