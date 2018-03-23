'''
==========================
tracks by
user
messages

content: showing all tweets
         Matching
location
mentioned by

users: all
       specific
engagement
 altleast by: 0 Retweets
                likes
              0 relies
=============================

put accounts:
get accounts interraction reports do they care

sent out 70
user
  replies and who did
  
 
retweet
   pos
   neg

'''

# https://pythonspot.com/en/tkinter-askquestion-dialog/
# https://anthonydebarros.com/2013/07/04/python-twitter-facebook-api-script-sqlite/
# https://pythonspot.com/en/matplotlib/
from textblob import TextBlob
from TwitterSearch import *
#import smtplib  ########################for sending emails
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import tweepy
import csv
from credentials import*
from time import sleep
import time
import requests
from bs4 import BeautifulSoup
import re
import datetime


from textblob.classifiers import NaiveBayesClassifier 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#####################################################################################################################################

class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master,width=700,height=580,bd=2,relief=GROOVE)
        self.pack(fill=X, padx=40, pady=40)
        self.output()

 
        
    def output(self):
        
        #First Name
        firstName=Label(self,text='First Name:')
        firstName.grid(row=1,column=0, padx=5, pady=3)
        self.e = Entry(self, width=20)
        self.e.grid(row=1,column=1, padx=5, pady=3)

        #Last Name
        lastName=Label(self,text='Last Name:')
        lastName.grid(row=1,column=2, padx=5, pady=3)
        self.e1 = Entry(self, width=20)
        self.e1.grid(row=1,column=3, padx=5, pady=3)
        
        self.b = Button(self, text='Submit',command=self.writeToFile)
        self.b.grid(row=1,column=4, padx=5, pady=3)
        
        
        
#####################################################################################################################################
        
        #Message
        post=Label(self,text='Enter Tweet Message:')
        post.grid(row=3,column=0, padx=5, pady=3)
        self.e2 = Entry(self, width=50)
        self.e2.grid(row=3,column=1, padx=5, pady=3)
        
        self.c = Button(self, text='Post Message',command=self.post_Message)
        self.c.grid(row=3,column=2, padx=5, pady=3)
        
        #Get Contents from Twitter
        #firstName=Label(self,text='Enter Search Term:')
        #firstName.grid(row=5,column=0, padx=5, pady=3)
        
        get_content=Label(self,text='Search A Message:')
        get_content.grid(row=5,column=0, padx=5, pady=3)
        
        self.e3 = Entry(self, width=50)
        self.e3.grid(row=5,column=1, padx=5, pady=3)
        
        self.d = Button(self, text='Search Message',command=self.get_content)
        self.d.grid(row=5,column=2, padx=5, pady=3)
        
        self.f = Button(self, text='Search Message And Trans and Analyze',command=self.get_content)
        self.f.grid(row=5,column=3, padx=5, pady=3)
        
      
        # 2/2/2018
        T = Text(self, height=12, width=13)
        T.insert(END, "Just a text Widget\nin two lines\n")
        #self.T.pack()
        # end 2/2/2018
        

        #harvest followers of a user from Twitter
        
        harvest=Label(self,text='Find Followers Of User:')
        harvest.grid(row=6,column=0, padx=5, pady=3)
        self.e4 = Entry(self, width=50)
        self.e4.grid(row=6,column=1, padx=5, pady=3)
        
        self.e = Button(self, text='Find Followers',command=self.harvest_followers)
        self.e.grid(row=6,column=2, padx=5, pady=3)
        

        #interractions  from Twitter
        
        harvest=Label(self,text='Enter Twitter User and Get Interactions Data:')
        harvest.grid(row=7,column=0, padx=5, pady=3)
        self.e5 = Entry(self, width=50)
        self.e5.grid(row=7,column=1, padx=5, pady=3)
        
        self.f = Button(self, text='Interractions',command=self.get_interractions)
        self.f.grid(row=7,column=2, padx=5, pady=3)
        

        #Facebook Comments
        
        harvest=Label(self,text='what are they saying in facebook:')
        harvest.grid(row=8,column=0, padx=5, pady=3)
        self.e6 = Entry(self, width=50)
        self.e6.grid(row=8,column=1, padx=5, pady=3)
        
        self.g = Button(self, text='Facebook Comments',command=self.get_facebook_messages)
        self.g.grid(row=8,column=2, padx=5, pady=3)
        
        
        
##################################################################################################################
  


# print (cl.classify("This is an amazing library!"))

#  You can get the label probability distribution with the prob_classify(text) method.
        

        
#####################################################################################################################################

# get followers, find out how many tweets by hin/her, location 
    
    def harvest_followers(self):
                    #accountvar = "Somaliya_Cusub" #raw_input("Account name: ")
                    print (self.e4.get())
                    accountvar = self.e4.get()
                    #todo: upgrade this to read usernames from a file.
                    print("searching for followers of "+accountvar)

                    #todo: upgrade this to read usernames from a file.
                    print("searching for followers of "+accountvar)
                    # Creating the API object while passing in auth information
                    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
                    
                    #tells tweepy.API to automatically wait for rate limits to replenish
                    #  API.followers([id/screen_name/user_id][, cursor])
                    
                    users = tweepy.Cursor(api.followers, screen_name=accountvar).items()
                    
                    count = 0
                    errorCount=0
                    #outputfile = accountvar+"followers.txt"
                    #outputfilecsv = accountvar+"followers.csv"
                    #f = open(outputfile,'w')
                    #f.write("screen name,followers count,statuses count,Location,geo_enabled \n")
                            
                    #fc = csv.writer(open(outputfilecsv, 'wb'))
                    while True:
                        try:
                            user = next(users)
                            count += 1
                            #use count-break during dev to avoid twitter restrictions
                            #if (count>10):
                            #    break
                        except tweepy.TweepError:
                            #catches TweepError when rate limiting occurs, sleeps, then restarts.
                            #nominally 15 minnutes, make a bit longer to avoid attention.
                            print ("sleeping....")
                            time.sleep(60*16)
                            user = next(users)
                        except StopIteration:
                            break
                        try:
                           
                            print("@"+(user.screen_name)+","+str(user.followers_count)+","+ str(user.statuses_count)+","+ str(user.location)+","+ str(user.geo_enabled)+"\n")
                           
                           # print ("@" + user.screen_name + " has " + str(user.followers_count) +\
                            #       " followers, has made "+str(user.statuses_count)+" tweets and location=" +\
                            #       user.location+" geo_enabled="+str(user.geo_enabled)+" count="+str(count))
                            
                            
                            #write to file .txt
                            
                            #2/6/2018
                            
                            #f.write("@" + (user.screen_name)+", "+str(user.followers_count)+", "+ str(user.statuses_count)+", "+ str(user.location)+", "+ str(user.geo_enabled)+"\n")
                           #end 2/6/2018
                            #f.write(user.screen_name+", "+str(user.followers_count)+", "+ str(user.statuses_count)+"\n")
                            #fc.writerow([user.screen_name, str(user.followers_count), str(user.statuses_count), user.location, str(user.geo_enabled)])
                        except UnicodeEncodeError:
                            errorCount += 1
                            #print ("UnicodeEncodeError,errorCount ="+str(errorCount))
                            #f.close()
                            #fc.close()
                            #apparently don't need to close csv.writer.
                            #print ("completed, errorCount ="+str(errorCount)+" total users="+str(count))
                            #print "@" + user.screen_name
                            #todo: write users to file, search users for interests, locations etc.


#####################################################################################################################################


# write message to file
                            
    def writeToFile(self):
        with open('WorkOrderLog.csv', 'a') as f:
            w=csv.writer(f, delimiter=',')
            #w.writerow([self.e.get()])
            w.writerow([self.e1.get()])
           #w.writerow([str(self.e1.get()),str(self.e.get()) ])
            
#####################################################################################################################################            
            
    def writeToFile2(self):
        with open('WorkOrderLog.csv', 'a') as f:
            w=csv.writer(f, quoting=csv.QUOTE_ALL)
            first_name = self.e.get()
            last_name = self.e1.get()
            
            print (first_name)
            print(last_name)
            
            w.writerow(first_name)
            w.writerow(last_name)
            
            #w.writerow([self.e.get()])
            #w.writerow([self.e1.get()])
#####################################################################################################################################
            
# post tweets to your account
    def post_Message(self):
        print (self.e2.get())
        api.update_status(self.e2.get())
          
          


#####################################################################################################################################

    def get_interractions(self):
        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        status = tweepy.API(auth)
        
        username = self.e5.get()
        
        #username = "somaliya_cusub"# sys.argv[1]
        # 2018, 2, 14, 0, 0, 0
        #   t.Year(), t.Month(), t.Day(),t.Hour(), t.Minute(), t.Second())
        
        startDate = datetime.datetime(2018, 2, 11, 0, 0, 0)
        endDate =   datetime.datetime(2018, 2, 28, 11, 59, 59)
#        ############################################################################        
#        for i in range(100):
#            print(i)
#            
#            firstTweet = api.user_timeline("somaliya_cusub")[i]
#            print('Created on: '+str(firstTweet.created_at))
#            print ('Message:'+str(firstTweet.text))
#            tweet_ID = firstTweet.id
#    
#        ############################################################################
        # tmpTweets = api.user_timeline(username)
        # for status in tweepy.Cursor(status.user_timeline, "somaliya_cusub").items(200):
        for status in tweepy.Cursor(status.user_timeline, username).items(200):
            print('https://twitter.com/'+username+'/status/'+str(status.id))
            #print(status.id)
            for url in status.entities['urls']:
                if status.created_at < endDate and status.created_at > startDate:
                    print("it is today"+str(status.created_at))
                    r = requests.get(url['expanded_url'])
                    hiti = ""
                    soup = BeautifulSoup(r.text, 'lxml')
                    # find('p', attrs={'class' : 'TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text'})
                    for hiti in soup.findAll(attrs={'class' : 'TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text'}):
                        page = hiti.getText()
                        print (page)
                        print("end of the text")
                        
                        
            for url in status.entities['urls']:
                if status.created_at < endDate and status.created_at > startDate:
                    print("it is today"+str(status.created_at))
                    r = requests.get(url['expanded_url'])
                    hito = ""
                    soup = BeautifulSoup(r.text, 'lxml')
                    for hit in soup.findAll(attrs={'class' : 'ProfileTweet-actionCountForAria'}):
            
                        Date_created =status.created_at
                        message = status.text
                        hito+=hit.contents[0].strip()+" "
                        
                        #print (hit.contents[0].strip())
                        
                        tweet_data = hit.contents[0].strip()
                        #print("===============================")
                        m = re.match(r"(\w+)", tweet_data)
                        remake = m.group(1)
                    #print("=== =================================")   
                    #print (url['expanded_url'])        
                    # 0 replies 4 retweets 16 likes
                    
                    b = TextBlob(hito)
                    
                    if((b.detect_language())== 'ar'):
                        print('contains arabic')

                    m = re.match(r"(\w+) (\w+) (\w+) (\w+) (\w+) (\w+)", hito)
                    #print(status.created_at)
                    #print("=======")
                    print(m.group(0))
                    tweet_data9 = m.group(0)
                    #tweet_data10 = tweet_data9.replace(" retweets ", ",")
                    tweet_data10 = re.sub("[^0-9^.]", " ", tweet_data9)
                    print(tweet_data10)
            
                    tweet_data10 = re.sub("[^0-9^.]", " ", tweet_data9)
                    
                    #print(tweet_data10)        
                    tweet_data11 = tweet_data10.replace("       ", " ")
                    tweet_data12 = tweet_data11.replace("   ", " ")
                    tweet_data13 = tweet_data12.replace("  ", " ")
                    print(tweet_data13)
                    
                    ############write file######################################################
                    outputfile = "interractions.txt"
                    f = open(outputfile,'a')
                    try:
                        f.write(str((Date_created))+" "+str((tweet_data13))+" "+str(url['expanded_url'])+"\n")
                    except UnicodeEncodeError:
                        print ("UnicodeEncodeError,errorCount")
                    f.close()
                    message2 = "interractions_message.txt"
                    f = open(message2,'a')
                    try:
                        #f.write(str("Replies")+" "+str("Retweets)+" "+str("Likes"))
                        f.write(status.text+"\n")
                    except UnicodeEncodeError:
                        print ("UnicodeEncodeError,errorCount")
                    f.close()

    

              
                          
#####################################################################################################################################
# get content
    def get_content(self):
        
        # machine learning stuff
        ####################### Machine learning Data ###################################
        train = [
                    ('I love this sandwich.', 'pos'),
                    ('this is an amazing place!', 'pos'),
                    ('I feel very good about these beers.', 'pos'),
                    ('this is my best work.', 'pos'),
                    ("what an awesome view", 'pos'),
                    ('I do not like this restaurant', 'neg'),
                    ('I am tired of this stuff.', 'neg'),
                    ("I can't deal with this", 'neg'),
                    ('he is my sworn enemy!', 'neg'),
                    ("Turkey to start a big agricultural", 'neg'),
                    ('Government forces take control of', 'pos'),
                    ('my boss is horrible.', 'neg')
                ]
        test = [
                    ('the beer was good.', 'pos'),
                    ('I do not enjoy my job', 'neg'),
                    ("I ain't feeling dandy today.", 'neg'),
                    ("I feel amazing!", 'pos'),
                    ('Gary is a friend of mine.', 'pos'),
                    ("I can't believe I'm doing this.", 'neg')
                ]

### import model
        
        cl = NaiveBayesClassifier(train)
        print (self.e3.get())
        thequery = self.e3.get()
        
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        
        for tweet in tweepy.Cursor(api.search,
                               q=thequery,
                               since='2018-02-12',
                               until='2018-02-18',
                               lang=tso.set_language('so')).items(15):
            # lang='en').items(6):
            
          # api.send_direct_message(user_id = 'xxxxx,text = bericht)
          # # Retweet tweets as they are found
          #tweet.retweet()
          #print('Retweeted the tweet')
            try:
                if not tweet.retweeted:
                    print("retweeted")
                    print('Tweet by: @' + tweet.user.screen_name)
                    
                    
                
                print('=================this are the users===============')
                #print('Tweet by: @' + tweet.user.screen_name)
                #print ('Location: ' + tweet.user.location)
                print ('Message: ' +tweet.text)
                
                print("the translation to English is:")
                # 
                # what is the sentiment positive or negative
                print (cl.classify(tweet.text))
                # textblob 
                somali_blob = TextBlob(tweet.text)
                print(somali_blob.translate(from_lang="so", to='en')) ## translate from somali to english
                            
                #
                
                
                #labels[0].config(text="helloooowClick2!!")

                sleep(5)
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break
            
            
            
    
              
#####################################################################################################################################

    def get_facebook_messages(self):
    
        
        page_url = 'https://graph.facebook.com/v2.8/XalkaSoomaaliyaa/feed?fields=id,message,reactions,shares,from,caption,created_time,likes.summary(true)' 
        comments_url = 'https://graph.facebook.com/v2.8/{post_id}/comments?filter=stream&limit=100'
        
        
        params = {'access_token': 'EAACEdEose0cBAAXrzuCRciwNPIt7D9oJfqTz9QTOcm54ZAM5lhGUVjtB1HV08r2qgHlrJN7gVrQjZAKZCavaI5Mk19zCZB0jjRn00Y5Hweir3TeyXWu32obY9wZAaJ6TJtXISIG6z2JegnbD8Oh0ajFTzodcERtrBF2qtZCSuQujpDZC7HZBaZAXjsdRNoBfK9YKU4NA5ll5zsJjVWhSn9eKh'}
        
        
        posts = requests.get(page_url, params = params)
        posts = posts.json()
        #print (posts)
        

    
        
        while True:
            try:
            ###Retrieve one post
                for element in posts['data']:
                    #print(element)
                    #print(element['shares'])
                    #print(element['likes'])
                    
                    
                    #collection_posts.insert_one(element)
                    ####Retrieve all comments for this post
                    this_comment_url = comments_url.replace("{post_id}",element['id'])
                    comments = requests.get(this_comment_url, params = params).json()
                    
                    #loop through all comments until the response is empty (there are no more comments)
                    while ('paging' in comments and 'cursors' in comments['paging'] and 'after' in comments['paging']['cursors']):
                        ###Iterate through all comments
                        for comment in comments['data']:
                            comment['post_id'] = element['id']
                            # print(comment['created_time'])
                            print(comment['message'])
                            
                            #print([comment])
                            #collection_comments.insert(comment)
                        
                        comments = requests.get(this_comment_url + '&after=' + comments['paging']['cursors']['after'], params = params).json()
         
                ###Go to the next page in feed
                posts = requests.get(posts['paging']['next']).json()
            except: # (KeyError, e):
                print("error")
                break            
#####################################################################################################################################

'''               
# get the original tweets authored by set of users (i.e., I want to exclude any tweet in their timeline that is actually a retweet)
# 
    def exclude_tweet_retweet(self):
        tweets= api.user_timeline(id=user['id'], count=30,include_rts=True)
        for tweet in tweets:
            if not tweet.retweeted:
                print("tit was not retreewted")
            # analyze_tweet(tweet)    
            else:
                    print("tit was not retreewted")
                    #do something with retweet
#

#####################################################################################################################################                    
#retweet every tweet a person sends out.
            
    def retweet_a_person_tweet(self):
        for status in api.user_timeline('someuser'):
            api.retweet(status.id)
    

 ''' 

#####################################################################################################################################                    

                  

if __name__ == "__main__":
     root=Tk()
     root.title('Twitter System:: Abdi Musa')
     #root.iconbitmap('data/Twitter-icon1.icon')
     root.minsize(700,700)
     root.geometry("1120x700")
     app=App(master=root)
     app.mainloop()
     root.mainloop()
     
#####################################################################################################################################
'''     


def get_replies(tweet):
    user = tweet.user.screen_name
    tweet_id = tweet.id
    max_id = None
    logging.info("looking for replies to: %s" % tweet_url(tweet))
    while True:
        q = urllib.parse.urlencode({"q": "to:%s" % user})
        try:
            replies = t.GetSearch(raw_query=q, since_id=tweet_id, max_id=max_id, count=100)
        except twitter.error.TwitterError as e:
            logging.error("caught twitter api error: %s", e)
            time.sleep(60)
            continue
        for reply in replies:
            logging.info("examining: %s" % tweet_url(reply))
            if reply.in_reply_to_status_id == tweet_id:
                logging.info("found reply: %s" % tweet_url(reply))
                yield reply
                # recursive magic to also get the replies to this reply
                for reply_to_reply in get_replies(reply):
                    yield reply_to_reply
            max_id = reply.id
        if len(replies) != 100:
            break
            
            '''