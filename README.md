# Sentiment Analysis of Tweets

This project performs sentiment analysis on tweets fetched from Twitter using the Nitter scraper. The analysis is done using the TextBlob library, which provides a simple API for diving into common natural language processing (NLP) tasks.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Data Processing](#data-processing)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Features

- Fetches tweets using hashtags from Nitter.
- Normalizes and cleans the tweet text.
- Analyzes sentiment (polarity and subjectivity) of the tweets.
- Categorizes tweets into positive, negative, and neutral sentiments.
- Outputs the results to a CSV file.

## Requirements

- Python 3
- `pandas`
- `nltk`
- `textblob`
- `ntscraper`

You can install the required libraries using pip:

```bash
pip install pandas nltk textblob ntscraper
