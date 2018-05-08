if answ[1] == 'когда':
	months = ['сентября','октября','ноября','декабря','января','февраля','марта','апреля','мая','июня','июля','августа']
	randnum = random.randint(0,10)
	if randnum <= 2:
		apisay(random.choice(['Когда Путин сольётся','Когда я перестану быть говнокодом']),toho,torep)
	else:
		apisay('Я уверена это случится '+str(random.randint(1,31))+' '+random.choice(months)+' '+str(random.randint(2018,2050)),toho,torep)