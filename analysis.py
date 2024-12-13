import pandas as pd
import re
import string
from ntscraper import Nitter
from textblob import TextBlob
from collections import Counter

# Initialize Nitter scraper
scraper = Nitter()

# Fetch tweets
try:
    tweets = scraper.get_tweets('AGI', mode="hashtag", number=500)
    all_tweets = [tweet['text'] for tweet in tweets['tweets']]
except Exception as e:
    print(f"Error fetching tweets: {e}")
    all_tweets = []

# Normalization function
def get_normalize(text):
    text = re.sub(r'\&\w*;', '', text)
    text = re.sub(r'@[^\s]+', '', text)  # Remove mentions
    text = re.sub(r'\$\w*', '', text)    # Remove dollar signs
    text = text.lower()                   # Convert to lowercase
    text = re.sub(r'https?:\/\/.*\/\w*', '', text)  # Remove URLs
    text = re.sub(r'#\w*', '', text)     # Remove hashtags
    text = re.sub(r'[' + string.punctuation.replace('@', '') + ']+', ' ', text)  # Remove punctuation
    text = re.sub(r'\b\w{1,2}\b', '', text)  # Remove short words
    text = re.sub(r'\s\s+', ' ', text)   # Remove extra spaces
    text = re.sub("[^a-zA-Z]", " ", text)  # Remove non-alphabetic characters
    return text.strip()                  # Strip leading/trailing spaces

# Normalize tweets
normalized_tweets = [get_normalize(tweet) for tweet in all_tweets]

# Filter out empty tweets
normalized_tweets = [tweet for tweet in normalized_tweets if tweet]

# Create DataFrame
tweets_df = pd.DataFrame({'tweets': normalized_tweets})

# Perform sentiment analysis with error handling
def get_sentiment(text):
    try:
        return TextBlob(text).sentiment
    except Exception as e:
        print(f"Error analyzing sentiment for text: {text} - {e}")
        return None  # Return None if there's an error

# Apply sentiment analysis
sentiments = tweets_df['tweets'].apply(get_sentiment)

# Filter out None results
valid_sentiments = sentiments.dropna()

# Assign sentiment results to DataFrame
# We need to ensure that we only keep the rows with valid sentiments
tweets_df = tweets_df.loc[valid_sentiments.index]  # Keep only the rows with valid sentiments

# Create a DataFrame from valid sentiments
polarity_subjectivity = pd.DataFrame(valid_sentiments.tolist(), columns=['Polarity', 'Subjectivity'], index=valid_sentiments.index)

# Assign the new DataFrame to the original DataFrame
tweets_df[['Polarity', 'Subjectivity']] = polarity_subjectivity

# Count sentiment categories
def categorize_sentiment(polarity):
    if polarity > 0:
        return 'positive'
    elif polarity < 0:
        return 'negative'
    else:
        return 'neutral'

tweets_df['sentiment'] = tweets_df['Polarity'].apply(categorize_sentiment)

# Count occurrences
sentiment_counts = Counter(tweets_df['sentiment'])
number_of_tweets_analyzed = sum(sentiment_counts.values())

# Print results
print(f'Number of Tweets Analyzed = {number_of_tweets_analyzed}')
print(f'Positive tweets = {sentiment_counts["positive"]}')
print(f'Negative tweets = {sentiment_counts["negative"]}')
print(f'Neutral tweets = {sentiment_counts["neutral"]}')

# Shuffle DataFrame
tweets_df = tweets_df.sample(frac=1).reset_index(drop=True)

# Save to CSV
tweets_df.to_csv('twitter.csv', index=False)