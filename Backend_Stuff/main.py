import RedditScraper
import json

#Initialkize Variables
R_scraper = RedditScraper.RedditScrapper()
subreddits = ["DayTrading", "Investing", "Stocks"]
tickers = [["msft", "microsft"], ["appl", "apple"], ["google", "googl"]]
reddit_post_count = 1
comment_count = 1

#Get Data
redditData = []
for sub in subreddits:
    print("Searching r/" + str(sub))
    for ticker in tickers:
        redditData.append({"Subreddit": sub, ticker[0]: R_scraper.GetData(sub, ticker, reddit_post_count, comment_count)})
    print("Done Searching r/" + str(sub))
        
with open('output.json', 'w') as file:
    json.dump(redditData, file)