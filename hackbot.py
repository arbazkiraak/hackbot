#!/usr/bin/python
import time
import subprocess
import telepot
import os

def handle(msg):
        chat_id = msg['chat']['id']
        command = msg['text']

        
        print "Got Command : %s " %command
        bot.sendMessage(chat_id,'\xF0\x9F\x98\x81 Welcome to ~HackBot v1.0~    \xE2\x9C\x94')
	
	if command.startswith('help') or command.startswith('/start'):
		bot.sendMessage(chat_id,'\xF0\x9F\x98\x9A HELP MENU: ')
		bot.sendMessage(chat_id,'1. Run built-in tools : example -> nmap -sV site.com')
		bot.sendMessage(chat_id,'2. Give Foldername and Command : example -> tool foldername python scriptname.py\n')
	elif command.startswith('tool'):
		words = command.split()
		mm=words[1]
		cmd=words[2]+' '+words[3]
		final=words[2:]
		print map(str,final)
		makeitastring = ' '.join(map(str, final))
		print makeitastring
		#print str(words[1]:words[-1])
		directory='/root/Desktop/pentest/'+str(mm)
		bot.sendMessage(chat_id,"\xF0\x9F\x92\xBC your Path: "+str(directory))
		
		if os.path.isdir(directory):
			print "PATH IS OK"
			try:
				os.chdir(directory)
				bot.sendMessage(chat_id,"\xF0\x9F\x93\x81 Changing Directory to: "+str(directory))
				print "OK"
				bot.sendMessage(chat_id,'\xF0\x9F\x90\x8D '+str(makeitastring))
				bot.sendMessage(chat_id,'\xF0\x9F\x92\xBB  [-] Wait.....[-]')
				pp=subprocess.check_output(makeitastring,shell=True)
				bot.sendMessage(chat_id,pp)
			except ValueError as ex:
				bot.sendMessage(ex,'Something')
		else:
			bot.sendMessage(chat_id,'Error : please check your folder path')
			bot.sendMessage(chat_id,'Make sure you folder at /root/Desktop/pentest/')

		
	else:
		bot.sendMessage(chat_id,'\xF0\x9F\x98\x88 [+] Got Command \xF0\x9F\x98\x88')
		bot.sendMessage(chat_id,command)
		bot.sendMessage(chat_id,'\xF0\x9F\x92\xBB  [-] Wait.....[-]')
		aa=subprocess.check_output(command,shell=True)
		bot.sendMessage(chat_id,aa)

api = open('api.txt','r')
api_cont = api.read()
bot = telepot.Bot(api_cont)
bot.message_loop(handle)
print '[+] Server is Listenining [+]'
print '[=] Type Command from Messenger [=]'

while 1:
        time.sleep(10)
