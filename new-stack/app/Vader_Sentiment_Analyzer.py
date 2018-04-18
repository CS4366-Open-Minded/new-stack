# -*- coding: utf-8 -*-
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
     
def Vader_Sentiment(text):
    bad_chars = {"’":"'", "“": '"', "”": '"'}
    
    for key, value in bad_chars.iteritems():
        text = text.replace(key, value)
    
    sentences = []
    
    sent_list = tokenize.sent_tokenize(text)
    sentences.extend(sent_list)
    
    sid = SentimentIntensityAnalyzer()
    
    # Obtain a overall intensity scores
    neg = 0.0
    neu = 0.0
    pos = 0.0
    
    # Obtain the overall number of sentences
    sent_count = len(sentences)
    
    for sentence in sentences:
        #print(sentence)
        ss = sid.polarity_scores(sentence)
        neg = neg + ss["neg"]
        neu = neu + ss["neu"]
        pos = pos + ss["pos"]
        
        # for k in sorted(ss):
        #    print('{0}: {1},'.format(k, ss[k]))
        # print("\n")
      
    # Obtain the average of all scores 
    neg = neg / float(sent_count)
    neu = neu / float(sent_count)
    pos = pos / float(sent_count)
    
    # Return the average scores within a dictionary
    overall_sentiment_dict = \
    {
        "neg": round(neg, 3),
        "neu": round(neu, 3),
        "pos": round(pos, 3)
    }
    
    return overall_sentiment_dict