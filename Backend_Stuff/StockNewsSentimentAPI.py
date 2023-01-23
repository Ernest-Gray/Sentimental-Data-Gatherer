from flask import Flask, request
import SentimentAnalysis
import StockNewsScalper
import datetime as dt
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

@app.route("/Hello_World")
def hello():
    return "Hello, World!"

#Returns the average'd sentiment data on a ticker for a given range
@app.route('/stocknews', methods=['GET'])
def StockNewsSentimentFun():
    ticker = request.args.get('ticker')
    print("Getting data on: " + ticker)
    
    #Get the news
    news = StockNewsScalper.GathererData(ticker).news
    
    #Extract the titles
    titles = [item['title'] for item in news]
    
    #Get sentiment of the titles
    sentiment = SentimentAnalysis.GetSentiment(titles)
    
    #Process the sentiment
    labels = dict.fromkeys(SentimentAnalysis.candidate_labels)
    labels = {key: float(0) for key,value in labels.items()}
    n = len(sentiment)

    for prediction in sentiment:
        for x in range(len(prediction['labels'])):
            labels[prediction['labels'][x]] += prediction['scores'][x]
        
    #Average out the values
    labels = {key: value/n for key,value in labels.items()}
    
    #Add the news time delta
    labels['NewsTimeDelta'] = str(GetNewsTimeLength(news))
    
    return labels

def GetNewsTimeLength(news:list):
    #See how old the data is
    times = []
    for article in news:
        times.append(dt.datetime.fromtimestamp(article['providerPublishTime']))
        
    oldest, newest = min(times), max(times)
    time_diff = relativedelta(newest, oldest)
    return time_diff


if __name__ == "__main__":
    app.run()