'''
Created on Feb 8, 2018

@author: ahmed

Email access to info, control pc
currently only works with gmail
must have a bot account on gmail
Not secure at all really
'''

import time
from emailBot import emailBot

mailBot = emailBot("BOT EMAIL ACCOUNT", "BOT EMAIL PASSWORD")

while True:
    mailBot.checkUnread()
    time.sleep(30)