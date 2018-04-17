"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect
from .models import Article,FactCheck
import requests
from bs4 import BeautifulSoup
import re
import string
import json
import sys
import os
import datetime
from nltk.corpus import stopwords
from concept_extraction import concept_extractor
from concept_compare import concept_checker
from Vader_Sentiment_Analyzer import Vader_Sentiment 


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.forms import BootstrapRegistrationForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    Articles = getData()
    # paginator = Paginator(Articles, 12)

    # page = request.GET.get('page')
    # Articles = paginator.get_page(page)

    return render(
        request,
        'app/index.html', Articles
    )

def getArticles():
    now = datetime.datetime.now()

    with open('custom_stopwords.txt') as e:
        stopwordList=e.read()+','.join(set(stopwords.words('english')))

    sourceURL = ('https://newsapi.org/v2/top-headlines?'
        'country=us&pageSize=12&'
        'apiKey=723ffc551d7e4fa1b3ed28c2b6051c44')
    url = []
    data = requests.get(sourceURL).json()
    for z in range(0, len(data["articles"])):
        url.append(data["articles"][z]["url"])

    session = requests.session()
    fname = "["+str(now.day)+"-"+str(now.month)+"-"+str(now.year)+"].json"

    output = {}
    texthold = []
    titlehold = []
    index=0
    with open(fname, 'w') as t:
        for site in url:
            req = session.get(site)
            doc = BeautifulSoup(req.content,'html.parser')
            title = doc.title
            txt = doc.findAll('p')

            clean = re.compile('<.*?>')

            cleantext = clean.sub('', str(txt))
            cleantext = cleantext.replace("\\n", "").replace("\\r", "").replace("\\t","")
            cleantext= unicode(cleantext).decode('unicode_escape').encode('ascii','ignore')
            texthold.append(cleantext.replace("\"", "").replace(".,", ".").replace("?,", ".").replace("!,", "."))

            cleantitle = clean.sub('', str(title))
            cleantitle = cleantitle.replace("\\n", "").replace("\\r", "").replace("\\t","")
            cleantitle = cleantitle.decode('utf-8').encode('utf-8')
            cleantitle = cleantitle.decode('unicode_escape').encode('ascii','ignore')
            cleantitle = cleantitle.replace("\"", "").replace(".,", ".").replace("?,", ".").replace("!,", ".")
            titlehold.append(cleantitle.translate(None, '\n|\\":\'?\"'))

            index+=1

    urlHolder = []
    with open("url.txt", "r") as urlTXT:
        inpt = urlTXT.readlines()
        for line in inpt:
            urlHolder.append(line)

        for z in range(0, len(data["articles"])):
            concept_ex = concept_extractor(fname.split(".",1)[0]+str(z), texthold[z], stopwordList, "JSON")
            sList, pList, uList = concept_checker(fname.split(".",1)[0]+str(z)+"_concepts.txt", "total_concepts.txt") 

            urlImage = data["articles"][z]["urlToImage"]
            if(urlImage == None):
                continue
            title = titlehold[z]
            if(Article.objects.filter(title=title)):
                continue
            description = data["articles"][z]["description"]
            author = data["articles"][z]["author"]
            publishedAt = data["articles"][z]["publishedAt"]
            source = data["articles"][z]["source"]["name"]
            
            url = data["articles"][z]["url"]
            text = (" ".join(texthold[z].split())).replace(" ,","")
            
            sentiment = Vader_Sentiment(text)

            Article.objects.create(title=title, author=author, description=description, urlImage=urlImage, url=url, source=source, text=text, publishedOn=publishedAt, sentimentNeg=sentiment["neg"], sentimentNeu=sentiment["neu"], sentimentPos=sentiment["pos"])

            #query to get current article id for foreign key reference to FactCheck
            query = Article.objects.get(title=title)            

            for i in range(1, len(sList)+1):
                if float(pList[i-1]) > .2:
                    sentenceNumber = i
                    similarityPercentage = pList[i-1]
                    if uList[i-1] > -1:
                        URLFact = urlHolder[uList[i-1]]
                    FactCheck.objects.create(url=url, sentenceNumber=sentenceNumber, similarityPercentage=similarityPercentage, URLFact=URLFact, article_id=query.id)



def getData(): 
    #getArticles()
    
    articleContent = Article.objects.order_by('-id')
    factContent = FactCheck.objects.all().order_by('-id')

    Articles = {
        'Article': articleContent,
        'factCheck': factContent,
    }
    return Articles


def signup(request):
    """Render the signup page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        regform = BootstrapRegistrationForm(request.POST)
        if regform.is_valid():
            regform.save()
            messages.success(request, "Account created successfully!")
            return redirect('register')
    else:
            regform = BootstrapRegistrationForm()
    
    return render(
        request,
        'app/register.html',
        {
            'form': regform,
            'title':'Sign Up',
            'year':datetime.now().year,
            }
        )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


def search(request):
    query = request.GET.get('search')

    result = {
        'query': query,
    }
    return render(request, 'app/search.html', result)