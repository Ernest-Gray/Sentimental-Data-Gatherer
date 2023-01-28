#Imports
import praw
import json
from datetime import datetime as dt
import SentimentAnalysis as SA

class RedditScrapper():

    def __init__(self) -> None:
        #Get Credentials
        with open('Backend_Stuff\config.json', 'r') as file:
            data = json.load(file)
            client_id = data['reddit_clientID']
            client_secret = data['reddit_secret']

        #Get Data using PRAW 'Python Reddit api w???'
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent='MyApp/1.0 by grayhound_56')

    def GetData(self, subreddit:str, titleEquals:list, postCount:int, commentCount:int):
        
        #Get the subreddit
        subreddit = self.reddit.subreddit(subreddit)

        #Formulate the query
        query = ""
        for title in titleEquals[:-1]:
            query += "title:" + str(title)
            query += " OR "
        query += "title:" + str(titleEquals[-1])
        print("Seaching Query: " + query)
        
        #Get the queried data
        data_filtered = subreddit.search(query, sort='relevance', limit=postCount, time_filter='all')

        data_filtered = list(data_filtered)
        print("Data found: " + str(len(data_filtered)))

        #Show most recent and oldest post timestamps
        print("Date Range from: " + str(dt.utcfromtimestamp(int(data_filtered[0].created_utc))) + " to " + str(dt.utcfromtimestamp(int(data_filtered[-1].created_utc))))

        #Do analyis on the sentiment of the titles
        titles = [item.title for item in data_filtered]
        print("Performing Sentimental Analysis on " + str(len(titles)) + " Titles")
        titleSentiment = SA.GetSentiment(titles)
        titleSentiment = SA.GetSummationSentiment(titleSentiment)
        
        #Scrape comments next THIS OPERATION TAKES A LONG TIME
        data_list = []

        for post in data_filtered:
            comments = post.comments[:commentCount]
            comments = [item.body for item in comments]
            data_list.append({"Title": post.title, "Comments" : comments})


        #Perform Sentiment Analyis (SA) on the comments
        comments = [item['Comments'] for item in data_list]
        comments_flat = []
        for sublist in comments:
            for comment in sublist:
                comments_flat.append(comment)
        print("Performing Sentimental Analysis on " + str(len(comments_flat)) + " Comments")
        commentSentiment = SA.GetSentiment(comments_flat)
        commentSentiment = SA.GetSummationSentiment(commentSentiment)
        return titleSentiment, commentSentiment


if __name__ == "__main__":
    scraper = RedditScrapper()
    titleSA, commentSA = scraper.GetData('DayTrading', ["msft", 'microsoft', 'apple', 'appl', 'google', 'googl'], None, 1)
    print(titleSA)
    print(commentSA)