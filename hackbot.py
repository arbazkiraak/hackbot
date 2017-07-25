#!/usr/bin/python
import time
import subprocess
import telepot
import os
import urllib2
import re
import json
import datetime
import requests
import threading
from bs4 import BeautifulSoup
from urllib2 import urlopen
import youtube_dl
import wikipedia

def handle(msg):
        chat_id = msg['chat']['id']
        command = msg['text']

        #direct command execution
        print "Got Command : %s " %command
        bot.sendMessage(chat_id,'\xF0\x9F\x98\x81 Welcome to -+ HackBot v1.2 +- (https://goo.gl/mxQ4Sv) \xE2\x9C\x94')
	
	#welcome screen and help
	if command.startswith('help') or command.startswith('/start'):
		bot.sendMessage(chat_id,'\xF0\x9F\x98\x9A HELP MENU: ')
		bot.sendMessage(chat_id,'1. Run built-in tools : example -> nmap -sV site.com')
		bot.sendMessage(chat_id,'2. Give Foldername and Command : example -> tool foldername python scriptname.py\n')
		bot.sendMessage(chat_id,'3. BTC Rate : example -> btc usd or btc anycurrency')
		bot.sendMessage(chat_id,'4. Hackerone Disclosed Bugs : usage : h1bugs')
		bot.sendMessage(chat_id,'5. Get Tweets of any search and times : usage : tweet bugbounty 5 or tweet motivation 3')
		bot.sendMessage(chat_id,'6. Get details of HackerOne disclosed report: usage: #152407 \n A # sign followed by the report number')
		bot.sendMessage(chat_id,'7. Hackerone Disclosed Bugs for specific program: usage: h1bugs programname')
		bot.sendMessage(chat_id,'8. Get automatically notified about latest HackerOne Disclosure: usage: notifyh1')
		bot.sendMessage(chat_id,'9. Search Wikipedia. usage: wiki yourtiopic')
		bot.sendMessage(chat_id,'10. Get YouTube videos delivered right to your box in mp3 format: usage: yt musicname')
		return 0


	#automatic hackerone notifier
	def notifyh1():
    		site = requests.get('https://hackerone.com/hacktivity.json?sort_type=latest_disclosable_activity_at&filter=type%3Apublic')
    		json_data = json.loads(site.text)
    		rep_id = json_data['reports'][0]['id']
    		rep_str = str(rep_id)
    		with open('latest.txt', 'r') as rmf:
    			data = rmf.read().replace('\n', '')
    		if data != rep_str:
    			with open('latest.txt', 'w') as wmf:
    				wmf.write("%s" % rep_str)
    			bot.sendMessage(chat_id,"\xF0\x9F\x90\x9B New Bug Disclosed on H1 \xF0\x9F\x90\x9B")
    			bot.sendMessage(chat_id,"Title: "+json_data['reports'][0]['title']+" ("+json_data['reports'][0]['readable_substate']+")")
			bot.sendMessage(chat_id,"https://hackerone.com"+json_data['reports'][0]['url'])
    		print(time.ctime())
    		threading.Timer(300, notifyh1).start()
    	if command.startswith('notifyh1'):
   			notifyh1()
   		#end automatic hackerone notifer
   		
	#tool
	elif command.startswith('yt'):
            param = command[3:]
            response = urlopen("https://www.youtube.com/results?search_query="+param)
            data = response.read()
            response.close()
            soup = BeautifulSoup(data,"html.parser")
            vid = soup.find(attrs={'class':'yt-uix-tile-link'})
            link = "https://www.youtube.com"+vid['href']
            title = vid['title']
            titleshorten = title[0:12]
            print "Shorten Title is : "+titleshorten
            bot.sendMessage(chat_id,title+"\n"+link)

            options = {
    			'format': 'bestaudio/best',
    			'postprocessors': [{
        			'key': 'FFmpegExtractAudio',
        			'preferredcodec': 'mp3',
        			'preferredquality': '320'
    			}]
			}

			
			
            with youtube_dl.YoutubeDL(options) as ydl:
            	print ydl.download([link])

            for i,line in enumerate(os.listdir('.')):
            	if titleshorten in line:
            		thatline = line
            		print "ThatLine: "+thatline
            		bot.sendAudio(chat_id,audio=open(thatline,'rb'))
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
	#end tool

	#btc price

	#wiki starts
	elif command.startswith('wiki'):
		try:
			letsplit=command.split()
			makesplit=letsplit[1]
        		response = urlopen("https://en.wikipedia.org/wiki/"+topic)
        		wiksearch = wikipedia.summary(makesplit,sentences=10)
			bot.sendMessage(chat_id,wiksearch+'\n'+wikipedia.page(makesplit).url)
		except Exception as e:
			bot.sendMessage(chat_id,'Error :'+e)
        		
    #wiki ends

	elif command.startswith('btc'):
			arg1=command[4:]
			print arg1
			url= "https://www.google.co.in/search?q=bitcoin+to+"+arg1
			req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
			con = urllib2.urlopen( req )
			Text=con.read()
			position=re.search("1 Bitcoin =",Text)
			res = float(Text[position.end():position.end()+9])
			axx = '1 BTC : '+str(res)+' '+arg1
			bot.sendMessage(chat_id,str(axx))
	#end btc price

	#h1 disclosed report
	elif command.startswith('h1bugs'):
		program=command[7:]
		#specific program
		if program:
			bot.sendMessage(chat_id,'\xF0\x9F\x9A\x80  Loading HackerOne Disclosed Bugs!  \xF0\x9F\x9A\x80')
			bot.sendMessage(chat_id, 'Program: '+program)
			site = requests.get('https://hackerone.com/hacktivity.json?filter=type%3Apublic%20to%3A'+program)
			json_data = json.loads(site.text)
			for i in range(10):
				try:
					title = "Title : "+json_data['reports'][i]['title']
					url = json_data['reports'][i]['url']
					urls = "Report at : https://hackerone.com/"+url
					bot.sendMessage(chat_id,title)
					bot.sendMessage(chat_id,urls)
					print "\n"
				except KeyError:
					pass
		#common hacktivity
		else:
			bot.sendMessage(chat_id,'\xF0\x9F\x9A\x80  Loading HackerOne Disclosed Bugs!  \xF0\x9F\x9A\x80')
			site = requests.get('https://hackerone.com/hacktivity.json?sort_type=latest_disclosable_activity_at&filter=type%3Apublic')
			json_data = json.loads(site.text)
			for i in range(10):
				try:
					title = "Title : "+json_data['reports'][i]['title']
					url = json_data['reports'][i]['url']
					urls = "Report at : https://hackerone.com/"+url
					bot.sendMessage(chat_id,title)
					bot.sendMessage(chat_id,urls)
					print "\n"
				except KeyError:
					pass
	#end h1 disclosed report.

	#twitter search	
	elif command.startswith('tweet') or command.startswith('Tweet'):
		twords=command.split()
		tname=twords[1]
		print tname
		timetweets=twords[2]
		print timetweets
		turl = "https://twitter.com/search?q="+tname+"&src=typd&lang=en"
		print turl
		bot.sendMessage(chat_id,'\xF0\x9F\x9A\x80  Loading Tweets!  \xF0\x9F\x9A\x80')
		response = urllib2.urlopen(turl)
		html = response.read()
		soup = BeautifulSoup(html,'lxml')

		tweets = soup.find_all('li','js-stream-item')
		counts=0
		for tweet in tweets:
			if tweet.find('p','tweet-text'):
				try:
					tweet_user = tweet.find('span','username').text
					tweet_text = tweet.find('p','tweet-text').text.encode('utf8')
					tweet_id = tweet['data-item-id']
					timestamp = tweet.find('a','tweet-timestamp')['title']
					bot.sendMessage(chat_id,tweet_text+'\n')
					counts = counts+1
					print counts
					print timetweets
					if counts == int(timetweets):
						break
					else: 
						pass
						time.sleep(1)
					
				except UnicodeDecodeError:
					pass
			else:
				continue
	#end twitter search

	#coin
	elif command.startswith('coin'):
			res = requests.get('https://api.coinsecure.in/v1/exchange/ticker')
			#print(res.text)
			j = json.loads(res.text)
			sell = j['message']['bid']
			bot.sendMessage(chat_id,str(sell)+' INR')
	#end coin

	#h1 report details
	elif command.startswith('#'):
			repnum=command[1:]
			bot.sendMessage(chat_id,'\xF0\x9F\x9A\x80  Loading report  \xF0\x9F\x9A\x80')
			site = requests.get('https://hackerone.com/reports/'+repnum+'.json')
			json_data = json.loads(site .text)
			if json_data['has_bounty?'] != 0:
				bounty='Bounty: '+json_data['formatted_bounty']
			replink = 'https://hackerone.com/reports/'+repnum
			title = json_data['title']
			username = json_data['reporter']['username']
			url = json_data['reporter']['url']
			state = json_data['readable_substate']
			vulninfo = 'Details:\n'+json_data['vulnerability_information']
			bot.sendMessage(chat_id,parse_mode='HTML',text='(<a href="'+replink+'">#'+repnum+'</a>) <b>'+title+' reported by </b><a href="https://hackerone.com'+url+'">'+username+'</a> <b>('+state+')</b>')
			if json_data['has_bounty?'] != 0:
				bot.sendMessage(chat_id,bounty)
			bot.sendMessage(chat_id,vulninfo)
			print "\n"
	#end h1 report details
	#direct command

	#start youtube
	elif command.startswith('yt'):
            param = command[3:]
            response = urlopen("https://www.youtube.com/results?search_query="+param)
            data = response.read()
            response.close()
            soup = BeautifulSoup(data,"html.parser")
            vid = soup.find(attrs={'class':'yt-uix-tile-link'})
            link = "https://www.youtube.com"+vid['href']
            watchid = vid['href']
            watchid = watchid.replace('/watch?v=','')
            title = vid['title']
            bot.sendMessage(chat_id,title+"\n"+link)

            options = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320'
                }]
            }

            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([link])
                bot.sendAudio(chat_id,audio=open(title+"-"+watchid+".mp3",'rb'))
    #end youtube search

	else:
		bot.sendMessage(chat_id,'\xF0\x9F\x98\x88 [+] Got Command \xF0\x9F\x98\x88')
		bot.sendMessage(chat_id,command)
		bot.sendMessage(chat_id,'\xF0\x9F\x92\xBB  [-] Wait.....[-]')
		aa=subprocess.check_output(command,shell=True)
		bot.sendMessage(chat_id,aa)

	#youtube search
	
    	



#api credentials
api = open('api.txt','r')
api_cont = api.read().strip()
bot = telepot.Bot(api_cont)
bot.message_loop(handle)
print '[+] Server is Listenining [+]'
print '[=] Type Command from Messenger [=]'

while 1:
        time.sleep(10)

