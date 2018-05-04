import subprocess
if answ[1]=='vox':
	vox_str = answ_text.split(' ')
	vox_count = len(answ_text.split(' '))
	listdir = os.listdir('tmp/vox')
	voxlist = []
	for i in range(vox_count):
		if vox_str[i]+'.wav' in listdir:
			voxlist.append(vox_str[i])
		else:
			tmpvox = list(vox_str[i])
			for k in range(len(tmpvox)):
				if tmpvox[k]+'.wav' in listdir:
					voxlist.append(tmpvox[k])
	voxcmd = ''
	for i in range(len(voxlist)):
		voxcmd += 'file \'vox/'+str(voxlist[i])+'.wav\'\n'
	print(voxcmd)
	open('tmp/voxlist.txt','w').write(voxcmd)
	voxcmd = 'ffmpeg -f concat -safe 0 -i tmp/voxlist.txt -c copy tmp/vox.wav'
	ps = subprocess.Popen(voxcmd.split(' '), stdout=subprocess.PIPE)
	output = ps.communicate()[0]
	ret = requests.get('https://api.vk.com/method/docs.getMessagesUploadServer?type=audio_message&peer_id='+str(toho)+'&access_token={access_token}&v=5.68'.format(access_token=token)).json()
	if not os.path.exists('tmp'):
		os.mkdir('tmp')
	with open('tmp/vox.wav', 'rb') as f:
		ret = requests.post(ret['response']['upload_url'], files={'file': f}).text
	ret = json.loads(ret)
	ret = requests.get('https://api.vk.com/method/docs.save?v=5.68&file='+ret['file']+'&title=vo&access_token='+token).text
	ret = json.loads(ret)
	ret = requests.get('https://api.vk.com/method/messages.send?attachment=doc'+str(ret['response'][0]['owner_id'])+'_'+str(ret['response'][0]['id'])+'&v=5.68&forward_messages='+str(torep)+'&peer_id='+str(toho)+'&access_token='+str(token))
	os.remove('tmp/vox.wav')