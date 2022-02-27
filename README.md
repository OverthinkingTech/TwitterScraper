# TwitterScraper
A simple python tool for scraping data from your twitter accounts you follow.

The purpose of this python script is to look for tweets from your followers that contains links to articles. The link gets saved to a text file and emailed to you.
The text file of links also works to keep track of what has been found before so you won't recieve the same link twice in your inbox.
This means the python script is great to run as a cron job.

You will also need 2 additional files in the same folder as the python script:
  -API_Tokens.txt
      --This needs to be a comma seperated list:
        "consumer_key,consumer_secret,access_token_key,access_token_secret"
  -Email_UserPass.txt
      --This needs to be a comma seperated list:
        "sending_gmail,sending_gmail_password,recieving_email"
        
        
Import list:
import smtplib, ssl
import twitter #pip install python-twitter
import time
import numpy as np
