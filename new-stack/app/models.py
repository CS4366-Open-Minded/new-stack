"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

import requests

STATE_CHOICES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DC', 'District of Columbia'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming')
    )

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(('Confirmation Status'),
        default=False,
        help_text=('Designates if a user has confirmed his/her email.'),
    )

class ArticleManager(models.Manager):
 
   def create_article(self, sourceID, sourceName, authorName, title, description, url, urlToImage, publishedOn):
        article = self.model(source_ID=sourceID, source_Name=sourceName, author_Name=authorName, title=title, description=description, url=url, url_To_Image=urlToImage, published_On=publishedOn)
        if self.filter(title=title).count() == 0:
            article.save(using=self._db)
        return article

   def request_articles(self):
       """
       Requests 20 articles from News API
       """
       response = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=6894e635a38d4de3be2367635985676d").json()
        
       for i in range(0, 20):
           id = response["articles"][i]["source"]["id"]
           sourceName = response["articles"][i]["source"]["name"]
           author = response["articles"][i]["author"]
           title = response["articles"][i]["title"]
           description =  response["articles"][i]["description"]
           url = response["articles"][i]["url"]
           urlImage = response["articles"][i]["urlToImage"]
           publishedAt = response["articles"][i]["publishedAt"]

           self.create_article(id, sourceName, author, title, description, url, urlImage, publishedAt)
        

class Article(models.Model):
    source_ID = models.CharField(max_length=200, null=True)
    source_Name = models.CharField(max_length=200, null=True)
    author_Name = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=254, null=True)
    url = models.URLField(max_length=200)
    url_To_Image = models.URLField(max_length=200)
    published_On = models.CharField(max_length=200)

    objects = ArticleManager()

    def get_sourceID(self):
        """
        Returns the source ID of the article.
        """
        return self.source_ID

    def get_source_name(self):
        """
        Returns the source name of the article.
        """
        return self.source_Name

    def get_author(self):
        """
        Returns the author name of the article.
        """
        return self.author_Name

    def get_title(self):
        """
        Returns the title of the article.
        """
        return self.title

    def get_url(self):
        """
        Returns the url of the article.
        """
        return self.url

    def get_url_to_image(self):
        """
        Returns the url to the image of the article.
        """
        return self.url_To_Image

    def get_publication_date(self):
        """
        Returns the publication date of the article.
        """
        return self.published_On