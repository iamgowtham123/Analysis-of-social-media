from flask import Flask, render_template, request
import tweepy
from textblob import TextBlob

app = Flask(_name_)

# Twitter API credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def perform_sentiment_analysis(query):
    # Perform sentiment analysis on tweets containing the query
    tweets = tweepy.Cursor(api.search, q=query, lang="en").items(100)
    polarity_sum = 0
    subjectivity_sum = 0
    count = 0

    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        polarity_sum += analysis.sentiment.polarity
        subjectivity_sum += analysis.sentiment.subjectivity
        count += 1

    if count > 0:
        average_polarity = polarity_sum / count
        average_subjectivity = subjectivity_sum / count
    else:
        average_polarity = 0
        average_subjectivity = 0

    return average_polarity, average_subjectivity

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    query = request.form['query']
    polarity, subjectivity = perform_sentiment_analysis(query)

    return render_template('analysis.html', query=query, polarity=polarity, subjectivity=subjectivity)

if _name_ == '_main_':
    app.run(debug=True)