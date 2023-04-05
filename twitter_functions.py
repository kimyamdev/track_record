import tweepy
import datetime
import openai
from textblob import TextBlob
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

consumer_key = "8ECBb4tumoV855xGd674O5iqa"
consumer_secret = "BV17aRh22MIN35CUjPizuXWuqvs0NXh22kBr9VsoHF0PXoPc98"
access_token = "345411064-BtLLWTOerFuibNAmfdbnKHqJXHdSKW440ULEkt0M"
access_token_secret = "Vkfov2UfGCN6DVDS8eFNk83RyBE10jXzSmD2iMB3Ps6kO"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
openai.api_key = "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"

def topic_tweets(topic, num_tweets):
    
    # Define the search query parameters
    search_words = '"{}" -filter:retweets'.format(topic)
    num_tweets = num_tweets

    # Search for tweets containing the query
    tweets = api.search_tweets(q = search_words, count = num_tweets)

    # Define a list to store the tweet text
    tweet_texts = []
    tweet_urls = []

    # Loop through the tweets and append the text to the list
    for tweet in tweets:
            url_dict_list = tweet.entities['urls']
            try:
                url = url_dict_list[0]['url']
                tweet_urls.append(url)
                txt = re.sub(r"http\S+", "", tweet.text)
                txt = re.sub(r"@\S+", "", txt)
                tweet_texts.append(txt)
            except: 
                continue
            
    combined_urls_tweets = dict(zip(tweet_urls, tweet_texts))
    print(combined_urls_tweets)

    # Combine the tweet texts into a single string
    tweet_text = " ".join(tweet_texts)

    # Define the OpenAI summarization model
    model_engine = "text-davinci-002"

    # Summarize the text using OpenAI
    summary = openai.Completion.create(
        engine=model_engine,
        prompt=tweet_text,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Print the summary
    # print(summary.choices[0].text.strip())

    content_dict = {
            "combined_urls_tweets": combined_urls_tweets,
            "summary_topic_tweets": summary.choices[0].text.strip()
    }

    return content_dict

def user_tweets(screen_name, num_tweets):
    # Define the search query parameters
    user = api.get_user(screen_name=screen_name)
    user_id = user.id_str
    num_tweets = num_tweets

    # Search for tweets from the user
    tweets = api.user_timeline(user_id=user_id, count=num_tweets)

    # Define a list to store the tweet text
    tweet_texts = []
    tweet_urls = []

    # Loop through the tweets and append the text to the list
    for tweet in tweets:
        url_dict_list = tweet.entities['urls']
        try:
            url = url_dict_list[0]['url']
            tweet_urls.append(url)
            txt = re.sub(r"http\S+", "", tweet.text)
            txt = re.sub(r"@\S+", "", txt)
            tweet_texts.append(txt)
        except:
            continue

    combined_urls_tweets = dict(zip(tweet_urls, tweet_texts))
    print(combined_urls_tweets)

    # Combine the tweet texts into a single string
    tweet_text = " ".join(tweet_texts)

    # Define the OpenAI summarization model
    model_engine = "text-davinci-002"

    # Summarize the text using OpenAI
    summary = openai.Completion.create(
        engine=model_engine,
        prompt=tweet_text,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Print the summary
    # print(summary.choices[0].text.strip())

    content_dict = {
        "combined_urls_tweets": combined_urls_tweets,
        "summary_user_tweets": summary.choices[0].text.strip()
    }

    return content_dict


def cluster_tweets(tweet_dict, num_clusters):
    """
    Cluster tweets based on text and return a dictionary with tuples of URL and text for each cluster.
    
    Args:
        tweet_dict (dict): A dictionary containing URLs as keys and tweet text as values.
    
    Returns:
        dict: A dictionary with cluster labels as keys and lists of tuples (URL, text) as values.
    """
    # Create a list of tweet texts and their corresponding URLs
    texts = list(tweet_dict.values())
    urls = list(tweet_dict.keys())

    # Vectorize the tweet texts using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(tfidf_matrix)
    labels = kmeans.labels_

    # Create a dictionary to store cluster information
    cluster_dict = {}

    # Iterate through the clusters and populate the dictionary with tuples of URL and text
    for i, label in enumerate(labels):
        if label not in cluster_dict:
            cluster_dict[label] = []
        cluster_dict[label].append((urls[i], texts[i]))

    print("cluster_dict")
    print(cluster_dict)

    return cluster_dict