# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 14:04:11 2021

@author: Overthinking Tech
"""

#%% Imports
import smtplib, ssl
import twitter #pip install python-twitter
import time
import numpy as np

#%% Twitter Api connection
filename = 'API_Tokens.txt'
data = np.loadtxt(filename,delimiter=',',dtype=str)
api = twitter.Api(consumer_key=data[0],
  consumer_secret=data[1],
    access_token_key=data[2],
    access_token_secret=data[3])

#%% Email setup
filename = 'Email_UserPass.txt'
emaildata = np.loadtxt(filename,delimiter=',',dtype=str)

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = emaildata[0]
password = emaildata[1]

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send a start up email
try:
    server = smtplib.SMTP(smtp_server,port)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(sender_email, password)
    server.sendmail(emaildata[0], emaildata[2], "Python Twitter script is running...")
except Exception as e:
    # Print any error messages
    print(e)

#%% Function to check character type
# I encountered errors when emojis and special unicode characters. This can be 
# editted to expand what gets kept.
def isproperchar(ch):
    if ch.isalpha() or ch.isdigit(): 
        return True
    else:
        return False
    
#%% Main
# Grab the list of your "friends," accounts you follow.
users = api.GetFriends()

# I know try and expect are not the best practice, but I'm lazy.
try:
    f = open("ArticlesAlreadyFound.txt", "r")
except:
    f = open("ArticlesAlreadyFound.txt", "x")
    f = open("ArticlesAlreadyFound.txt", "r")
# Reads a file of past found articles so you do not get emailed about the same
# srticle every time
founds = f.read()
f.close()
foundlist = founds.split('\n')
foundlist = foundlist[0:-1]

# Define words you want to search for in the tweet
lookfors = ['publish','article']

for user in users:
    userid = user.id
    username = user.name
    tweets = api.GetUserTimeline(userid)
    for tweet in tweets:
        ttext = tweet.text
        for lookfor in lookfors:
            if 'http' in ttext and 't.co/' in ttext and lookfor in ttext:
                startpos = ttext.find('http')
                pos2 = ttext.find('t.co/')
                posadder = 0
                
                whilebool = True
                while(whilebool):
                    try:
                        testch = ttext[pos2+5+posadder:pos2+5+posadder+1]
                        if isproperchar(testch):
                            posadder += 1
                        else:
                            whilebool = False
                    except:
                        whilebool = False
                if posadder >=8:
                    if 'https' in ttext:
                        endpos = startpos+13+posadder
                    else:
                        endpos = startpos+12+posadder
                    link = ttext[startpos:endpos]
                    include = True
                    for found in foundlist:
                        if found==link:
                            include = False
                for lookfor in lookfors:
                    if lookfor in ttext:
                        if include:
                            print(username+':',ttext)
                            f = open("ArticlesAlreadyFound.txt", "a")
                            f.write(link)
                            f.write('\n')
                            time.sleep(0.5)
                            f.close()
                            foundlist.append(link)
                            etext = username + ": " + link
                            message = """\
Subject: Twitter Link

"""
                            message += etext
                            server.sendmail(emaildata[0], emaildata[2], message)
                            time.sleep(2)

