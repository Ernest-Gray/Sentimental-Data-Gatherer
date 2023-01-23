
#Import our ai model for "Zero-Shot Classification".  Model at "https://huggingface.co/facebook/bart-large-mnli"
from transformers import pipeline
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

#Denote the labels to use
candidate_labels = ['Very Good', 'Good', 'Nuetral', 'Bad', 'Very Bad']


#Import yfinance lib to get news data from stocks
import yfinance as yf

def GetStockNewsSentiment(ticker:str):

    # Get the ticker object
    ticker = yf.Ticker(ticker)

    # Get the most recent news articles
    news = ticker.news

    #Extract the titles from the request stored in 'news'
    titles = [item['title'] for item in news]

    #Perform analysis with the classifier of the sequence using the given labels.
    output = classifier(titles, candidate_labels)

    return output

def GetSentiment(input_data:str):
    #Perform analysis with the classifier of the sequence using the given labels.
    return classifier(input_data, candidate_labels)

if __name__ == "__main__":
    output = GetSentiment("MSFT")
    #Save the output
    import json
    with open("output.json", 'w') as file:
        json.dump(output, file)
