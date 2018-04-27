if (answ[0] in kb_name and answ[1] in ['стат','статус','стата']):
	text = '[ Статистика ]<br>Система:<br>&#8195;Процессоры:<br>'
	for idx, cpu in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
		text += '&#8195;&#8195;Процессор №'+str(idx+1)+': '+str(cpu)+'%<br>'
	mem = psutil.virtual_memory()
	MB = 1024 * 1024
	text += '&#8195;ОЗУ:<br>&#8195;&#8195;Всего: '+str(int(mem.total / MB))+'MB<br>&#8195;&#8195;Использовано: '+str(int((mem.total - mem.available) / MB))+'MB<br>&#8195;&#8195;Свободно: '+str(int(mem.available / MB))+'MB<br>&#8195;&#8195;Использовано ботом: '+str(int(psutil.Process().memory_info().vms / MB))+'MB'
	param = (('v', '5.68'), ('peer_id',toho), ('access_token', token),('message', text),('forward_messages',torep))
	requests.post('https://api.vk.com/method/messages.send', param)