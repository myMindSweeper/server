from bs4 import BeautifulSoup
from datetime import datetime
import json, os

# returns array of all messages in the conversation file as dictionaries with time, user, and text
def scrapePage(name, content):
	soup_page = BeautifulSoup(content, 'html.parser')
	thread = soup_page.find('div', attrs={'class' : 'thread'})
	metas = thread.find_all('div', attrs={'class' : 'message_header'})

	texts = [text.text for text in thread.find_all('p', recursive=False)]
	times = [strToTime(meta.find('span', attrs={'class' : 'meta'}, recursive=False).text) \
		for meta in metas]
	users = [meta.find('span', attrs={'class' : 'user'}, recursive=False).text \
		for meta in metas]

	person = getPerson(name, users)
	speaking = [user != person for user in users]
	msgs = [{'body': x, 'date': y, 'user_speaking': z} \
		for x,y,z in list(zip(texts, times, speaking))[::-1]]
	return person, msgs

# returns datetime object of str
def strToTime(str):
	return datetime.strptime(str, '%A, %B %d, %Y at %I:%M%p').timestamp()

# returns person target user is conversing with
def getPerson(targetUser, users):
	for user in users:
		if user != targetUser:
			return user
	return targetUser

# returns array of all conversations
def scrapeAll(folder):
	name = getName(os.path.join(folder, 'index.htm'))
	convos = []
	for file in os.listdir(folder):
		if file.endswith('.html'):
			person, msgs = scrapePage(name, os.path.join(folder, file))
			if (len(msgs) > 0):
				convos.append({
					'token': None,
					'thread_id': int(file[:-5]),
					'person': person,
					'msg_list': msgs
				})
	return json.dumps(convos, indent=4)

# returns the name of the target user
def getName(file):
	soup_page = BeautifulSoup(open(file), 'html.parser')
	return soup_page.find('div', attrs={'class' : 'contents'}).find('h1').text
