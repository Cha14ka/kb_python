if answ[1] in ['talk','чат']:
	game_module['active_users'][userid] = 'talk'
	apisay('Ты вступил в разговор с ботом. Для выхода напиши "exit"',toho,torep)