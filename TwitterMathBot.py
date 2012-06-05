#!/usr/bin/python
import twitter
import re
import time
import os,sys
os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
db_file = 'db/last_id'
err_log_file = 'log/error.log'
req_log_file = 'log/request.log'

def getLastId():                #Gets the last Id traited and save it in db/last_id
    fp = open(db_file,"r")
    content = fp.read()
    fp.close()
    return content

def putLastId(last_id):        #Updates db/last_id
    fp = open(db_file,"w")
    fp.write(str(last_id))
    fp.close()

def putErrLog(msg):           # Errors are logged here log/error.log
    fp = open(err_log_file,"a")
    localtime = time.asctime(time.localtime(time.time()))
    fp.write(str(localtime)+" :: "+str(msg)+"\n")
    fp.close
    
def putReqLog(msg):           # All requests are logged in log/request.log
    fp = open(req_log_file,"a")
    localtime = time.asctime(time.localtime(time.time()))
    fp.write(str(localtime)+" :: "+str(msg)+"\n")

print time.asctime(time.localtime(time.time()))
# Configuring Twitter's API. These informations are provided by Twitter for each application you create.

consumer_k = ''
consumer_s = ''
oauth_token = ''
oauth_token_secret = ''

#initialization
api = twitter.Api(consumer_key=consumer_k,consumer_secret=consumer_s,access_token_key=oauth_token,access_token_secret=oauth_token_secret)
last_id = getLastId()

search = api.GetSearch(term='#redCalc',since_id=last_id) # Looking for all the tweets containing #redcalc hashtag since the last Id
i=0
for s in search:
  if i==0:
    putLastId(s.id)
    i+=1
# Calculating ...
  utext = re.sub(str(s.user.screen_name),'',s.text)    
  utext = re.sub(r'[ :@%#a-zA-Z]','',utext)
  putReqLog(s.text)

  try:
     status = api.PostUpdate("@"+s.user.screen_name+" "+utext+"="+str(eval(utext)))  # Sending the anwser if succeed.
  except: 
     putErrLog(s.text)
     status = api.PostUpdate("@"+s.user.screen_name+" Hmm I don't think that you are doing maths !")            # Send this if not, 
