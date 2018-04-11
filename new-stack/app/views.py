"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect
from .models import Article
import requests
from bs4 import BeautifulSoup
import re
import string
import json
import sys
import os
import datetime

from app.forms import BootstrapRegistrationForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    Articles = getData()
    return render(
        request,
        'app/index.html', Articles
    )

def htmlRetrieval():
    now = datetime.datetime.now()

    #with open('custom_stopwords.txt') as e:
        #stopwordList=e.read()+','.join(set(stopwords.words('english')))

    sourceURL = ('https://newsapi.org/v2/top-headlines?'
        'country=us&'
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

    # urlHolder = []
    # with open("url.txt", "r") as urlTXT:
    #     inpt = urlTXT.readlines()
    #     for line in inpt:
    #         urlHolder.append(line)

        for z in range(0, len(data["articles"])):
            #concept_ex = concept_extractor(fname.split(".",1)[0]+str(z), texthold[z], stopwordList, "JSON")
            #sList, pList, uList = concept_checker(fname.split(".",1)[0]+str(z)+"_concepts.txt", "total_concepts.txt") 
            output[data["articles"][z]["url"]] = [{}]
            output[data["articles"][z]["url"]][0]["title"] = titlehold[z]
            output[data["articles"][z]["url"]][0]["description"] = data["articles"][z]["description"]
            output[data["articles"][z]["url"]][0]["author"] = data["articles"][z]["author"]
            output[data["articles"][z]["url"]][0]["publishedAt"] = data["articles"][z]["publishedAt"]
            #output[data["articles"][z]["url"]][0]["source"] = {}
            #output[data["articles"][z]["url"]][0]["source"]["id"] = data["articles"][z]["source"]["id"]
            output[data["articles"][z]["url"]][0]["source"] = data["articles"][z]["source"]["name"]
            output[data["articles"][z]["url"]][0]["urlToImage"] = data["articles"][z]["urlToImage"]
            output[data["articles"][z]["url"]][0]["text"] = (" ".join(texthold[z].split())).replace(" ,","")
            #output[data["articles"][z]["url"]][0]["similarityList"] = {}
            # for i in range(1, len(sList)+1):
            #     if float(pList[i-1]) > .2:
            #         output[data["articles"][z]["url"]][0]["similarityList"][i] = {}
            #         output[data["articles"][z]["url"]][0]["similarityList"][i]["mostSimilarSentence"] = sList[i-1].replace("\\", "").replace("\"","").replace("[","").replace("]","").replace("'","")
            #         output[data["articles"][z]["url"]][0]["similarityList"][i]["similarityPercentage"] = pList[i-1]
            #         if uList[i-1] > -1:
            #             output[data["articles"][z]["url"]][0]["similarityList"][i]["sentenceURL"] = urlHolder[uList[i-1]]


        t.write(json.dumps(output, sort_keys=True))




def getData(): 
    #htmlRetrieval()

    now = datetime.datetime.now()
    #data = json.load(open("["+str(now.day)+"-"+str(now.month)+"-"+str(now.year)+"].json"))
   
    #Retrieve data for backend
    
    response = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=6894e635a38d4de3be2367635985676d")
    response = response.json()

    # check if article exists in database
    # make a query to the database if title exists in database then no need to store again
    
    #for i in range(0,12):
        # title = response["articles"][i]["title"]
        # if(Article.objects.filter(title=title)):
        #     continue
        # url=response["articles"][i]["url"]
        # fullText = data[url][0]["text"]
        # Article.objects.create(title=response["articles"][i]["title"], author=response["articles"][i]["author"], description=response["articles"][i]["description"], urlImage=response["articles"][i]["urlToImage"], url=url, source=response["articles"][i]["source"]["name"], text=fullText, publishedOn=response["articles"][i]["publishedAt"])

    context = Article.objects.all().order_by('-id')[:12]
    #context = Article.objects.all()[:12]
    Articles = {
        'Articles': context
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
