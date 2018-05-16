import textwrap
from PIL import Image, ImageDraw, ImageFont
if answ[1] == 'цитата':
	#####
	resnew = requests.get('https://api.vk.com/method/messages.getById?access_token='+token+'&v=5.68&message_ids='+str(torep)).text
	#print(resnew)
	resnew = json.loads(resnew)
	#print(resnew)
	id = resnew['response']['items'][0]['fwd_messages'][0]['user_id']
	ret = requests.post('https://api.vk.com/method/users.get',data={'v':'5.68','user_ids':id,'access_token':token,'fields':'photo_max'}).json()
	text = ''
	for k in range(len(resnew['response']['items'][0]['fwd_messages'])):
		text += resnew['response']['items'][0]['fwd_messages'][k]['body']+'\n'
	text = text.replace('\n','<br>')
	url = ret['response'][0]['photo_max']
	name = ret['response'][0]['first_name']+' '+ret['response'][0]['last_name']
	avatar = requests.get(url, stream=True).raw
	#####
	avatar = Image.open(avatar)
	avatar = avatar.resize([50,50],resample=Image.BILINEAR)
	data = textwrap.wrap(text, 50)
	data = '<br>'.join(data)
	data = data.split('<br>')
	y = 50+(29*len(data))
	fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 25)
	title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30)
	img = Image.new('RGB', (750, y), color = (255,255,255))
	d = ImageDraw.Draw(img)
	d.rectangle([0,0,750,50],outline=None,fill=(211,211,211))
	img.paste(avatar,[0,0,50,50])
	#d.text((0,50), '\n'.join(data), font=fnt, fill=(0, 0, 0))
	offset = 50
	for line in range(len(data)):
		#print(str(line)+':'+data[line])
		d.text((0,offset),data[line],font=fnt,fill=(0,0,0))
		offset += 29
		#print(offset)
	d.text((55,5), name, font=title, fill=(0, 0, 0))
	img.save('tmp/quote.jpg')
	sendpic('quote.jpg','',toho,torep)