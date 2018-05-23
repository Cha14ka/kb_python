import subprocess
if answ[1] == 'exec':
	if (answ_text == ''):
		apisay('А текст мб стоит вписать?)',toho,torep)
	else:
		cmd = answ_text.split('<br>')
		with open('tmp/exec.py', 'w') as cl:
			for i in range(len(cmd)):
				cl.write(cmd[i]+'\n')
		shell = subprocess.Popen('chmod 755 tmp/exec.py;python3 tmp/exec.py',shell=True,stdout=subprocess.PIPE)
		output = shell.communicate()[0]
		apisay(output,toho,torep)
