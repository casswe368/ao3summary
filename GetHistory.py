#get the history data to use with history code script
#adapted from https://github.com/alexwlchan/ao3
#using fix to authentication change by https://github.com/escherlat/ao3/

import requests
from bs4 import BeautifulSoup
import cred
import time
import random


#<input name="utf8" type="hidden" value="✓"/>
#<input name="authenticity_token" type="hidden" value="detzEH9sJsiZchx0R9DhZFjtnZiTxcd7hDvBAu5kIg6Ky+hFNZXdmaUKmqw23SJG8HF606MN2x4dbWSXkRY0Fw=="/>
#<input id="user_login" name="user[login]" type="text"/>
#<input id="user_password" name="user[password]" type="password"/>
#<input name="user[remember_me]" type="hidden" value="0"/>

def allHistory():

    sess = requests.Session()

    req = sess.get('https://archiveofourown.org')
    soup = BeautifulSoup(req.text, features='html.parser')

    authenticity_token = soup.find('input', {'name': 'authenticity_token'})['value']
    username=cred.username
    password=cred.password

    req = sess.post('https://archiveofourown.org/users/login', params={
            'authenticity_token': authenticity_token,
            'user[login]': username,
            'user[password]': password,
        })
    f = open('HistoryHTMLTEST.txt', 'a+', encoding='utf-8')
    for i in range(1,494):
        url='https://archiveofourown.org/users/gunpowderandlove/readings?page={}'.format(i)
        req = sess.get(url)
        html=req.text
        f.write(html)
        time.sleep(1+random.random())
    f.close()



def main():
    allHistory()

    
main()