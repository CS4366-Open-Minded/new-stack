"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

#STATE_CHOICES = (
#    ('AL', 'Alabama'),
#    ('AK', 'Alaska'),
#    ('AZ', 'Arizona'),
#    ('AR', 'Arkansas'),
#    ('CA', 'California'),
#    ('CO', 'Colorado'),
#    ('CT', 'Connecticut'),
#    ('DC', 'District of Columbia'),
#    ('DE', 'Delaware'),
#    ('FL', 'Florida'),
#    ('GA', 'Georgia'),
#    ('HI', 'Hawaii'),
#    ('ID', 'Idaho'),
#    ('IL', 'Illinois'),
#    ('IN', 'Indiana'),
#    ('IA', 'Iowa'),
#    ('KS', 'Kansas'),
#    ('KY', 'Kentucky'),
#    ('LA', 'Louisiana'),
#    ('ME', 'Maine'),
#    ('MD', 'Maryland'),
#    ('MA', 'Massachusetts'),
#    ('MI', 'Michigan'),
#    ('MN', 'Minnesota'),
#    ('MS', 'Mississippi'),
#    ('MO', 'Missouri'),
#    ('MT', 'Montana'),
#    ('NE', 'Nebraska'),
#    ('NV', 'Nevada'),
#    ('NH', 'New Hampshire'),
#    ('NJ', 'New Jersey'),
#    ('NM', 'New Mexico'),
#    ('NY', 'New York'),
#    ('NC', 'North Carolina'),
#    ('ND', 'North Dakota'),
#    ('OH', 'Ohio'),
#    ('OK', 'Oklahoma'),
#    ('OR', 'Oregon'),
#    ('PA', 'Pennsylvania'),
#    ('RI', 'Rhode Island'),
#    ('SC', 'South Carolina'),
#    ('SD', 'South Dakota'),
#    ('TN', 'Tennessee'),
#    ('TX', 'Texas'),
#    ('UT', 'Utah'),
#    ('VT', 'Vermont'),
#    ('VA', 'Virginia'),
#    ('WA', 'Washington'),
#    ('WV', 'West Virginia'),
#    ('WI', 'Wisconsin'),
#    ('WY', 'Wyoming')
#    )

class Article(models.Model):
    source = models.CharField(max_length=200)
    author = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True)
    text = models.CharField(max_length=400)
    url = models.URLField(max_length=200)
    urlImage = models.URLField(max_length=200, null=True)
    publishedOn = models.CharField(max_length=200)
    sentimentNeg = models.CharField(max_length=100, null=True)
    sentimentNeu = models.CharField(max_length=100, null=True)
    sentimentPos = models.CharField(max_length=100, null=True)

class FactCheck(models.Model):
    sentence = models.CharField(max_length=254,null=True)
    sentenceNumber = models.IntegerField()
    URLFact = models.URLField(max_length=254, null=True)
    similarityPercentage = models.DecimalField(max_digits=4, decimal_places=4)
    article = models.ForeignKey('Article')

# class Sentiment(models.Model):
#     sentimentResult = models.CharField(max_length=100, null=True)
#     url = models.URLField()
    #article = models.ForeignKey('Article', null=True)

#temporary table to store search results in
#will make implementation simpler for now
class searchArticle(models.Model):
    source = models.CharField(max_length=200)
    author = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True)
    text = models.CharField(max_length=400)
    url = models.URLField(max_length=200)
    urlImage = models.URLField(max_length=200, null=True)
    publishedOn = models.CharField(max_length=200)
    sentimentNeg = models.CharField(max_length=100, null=True)
    sentimentNeu = models.CharField(max_length=100, null=True)
    sentimentPos = models.CharField(max_length=100, null=True)


class userArticle(models.Model):
    article_id = models.ForeignKey('Article')
    userName = models.CharField(max_length=200)

class shareArticle(models.Model):
    article = models.ForeignKey('Article')
    sentFrom = models.CharField(max_length=255)
    sentTo = models.CharField(max_length=255)