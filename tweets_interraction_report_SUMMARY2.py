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
        
#        harvest=Label(self,text='Enter Twitter User and Get Interactions Data:')
#        harvest.grid(row=7,column=0, padx=5, pady=3)
#        self.e5 = Entry(self, width=30)
#        self.e5.grid(row=7,column=1, padx=5, pady=3)
        
        #First Name
        stday=Label(self,text='Start Day:').grid(row=0)
        self.sday = Entry(self, width=5).grid(row=1)
        
        stmonth=Label(self,text='Start Month:').grid(row=3)
        self.smonth = Entry(self, width=5).grid(row=4)

        
        
        enday=Label(self,text='End Day:').grid(row=5)
        self.eday = Entry(self, width=5).grid(row=6)
        
        enmonth=Label(self,text='End Month:').grid(row=7)
        self.emonth = Entry(self, width=5).grid(row=8,pady=3)

      
        OPTIONS = [
        "Somaliya_Cusub",
        "Xalka_Somaliya",
        "TheVillaSomalia"
        ] 
        self.variable = StringVar(self)
        self.variable.set(OPTIONS[0]) # default value
        self.w = OptionMenu(self, self.variable, *OPTIONS)
        self.w.grid(row=7,column=2, padx=5, pady=3)
        
        self.f = Button(self, text='Get Interractions With The User',command=self.get_interractions)
        self.f.grid(row=7,column=3, padx=5, pady=3)
        
        

        

#####################################################################################################################################

    def get_interractions(self):
        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        status = tweepy.API(auth)
        
#        sday = self.sday.get()
#        smonth = self.smonth.get()
#        
#        eday = self.eday.get()
#        emonth = self.emonth.get()
#        
#        #username = self.e5.get()
        username = self.variable.get()
        print (self.variable.get())
        
        #username = "somaliya_cusub"# sys.argv[1]
        # 2018, 2, 14, 0, 0, 0
        #   t.Year(), t.Month(), t.Day(),t.Hour(), t.Minute(), t.Second())
        
        startDate = datetime.datetime(2018, 2, 10, 0, 0, 0)
        endDate =   datetime.datetime(2018, 3, 1, 11, 59, 59)

        for status in tweepy.Cursor(status.user_timeline, username).items(200):
            # prints all tweets and retweets related with the following user
            print('https://twitter.com/'+username+'/status/'+str(status.id))
            thelink = 'https://twitter.com/'+username+'/status/'+str(status.id)
            if status.created_at < endDate and status.created_at > startDate:
                    print("Today is: "+str(status.created_at))
                    r = requests.get(thelink)
                    hiti = ""
                    soup = BeautifulSoup(r.text, 'lxml')
                    # find('p', attrs={'class' : 'TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text'})
                    for hiti in soup.findAll(attrs={'class' : 'TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text'}):
                        page = hiti.getText()
                        print (page)
                        #print("end of the text")
                    hito = ""
                    soup = BeautifulSoup(r.text, 'lxml')
                    
                    for hit in soup.findAll(attrs={'class' : 'ProfileTweet-actionCountForAria'}):
                    #for hit in soup.findAll(attrs={'class' : 'ProfileTweet-actionCount'}):
                    #for hit in soup.findAll(attrs={'class' : 'ProfileTweet-actionList js-actions'}):
            
                        Date_created =status.created_at
                        message = status.text
                        hito+=hit.contents[0].strip()+" "
                        
                        #print (hit.contents[0].strip())
                        
                        tweet_data = hit.contents[0].strip()
                    

                    print(hito[:32])


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
