"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect
from .models import Article,FactCheck,searchArticle
import requests
from bs4 import BeautifulSoup
import re
import string
import json
import sys
import os
from datetime import datetime
from nltk.corpus import stopwords
from concept_extraction import concept_extractor
from concept_compare import concept_checker
from Vader_Sentiment_Analyzer import Vader_Sentiment

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app.forms import BootstrapRegistrationForm
from nltk import tokenize

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
    now = datetime.now()

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

            t = 'T'
            z = 'Z'
            date = ''
            time = ''

            for i in publishedAt:
                if i == t:
                    break
                date += i
            
            timestart = text.find(t)
            timeEnd = text.find(z)

            for i in range(timestart+1, timeEnd):
                time += text[i]
            
            d = datetime.strptime(time, "%H:%M:%S")
            d = d.strftime("%I:%M:%S")

            publishedAt = date+' '+d

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
                    FactCheck.objects.create(url=url, sentence=sList[sentenceNumber],sentenceNumber=sentenceNumber, similarityPercentage=similarityPercentage, URLFact=URLFact, article_id=query.id)



def getData(): 
    getArticles()
    
    factContent = []

    articles = Article.objects.order_by('-id')
    facts = FactCheck.objects.all().order_by('-id')

    for fact in facts:
        factContent.append(fact)
        
    Articles = {
        'Article': articles,
        'factCheck': factContent,
    }
    return Articles


def signup(request):
    """Render the signup page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        regform = BootstrapRegistrationForm(request.POST)
        if regform.is_valid():
            user = regform.save()

            # Send activation email to user
            current_site = get_current_site(request)
            mail_subject = 'Activate your NEWSTACK account.'
            message = render_to_string('app/activate-email.html', {
                'user':user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                })
            to_email = regform.cleaned_data['email']
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            messages.success(request, "Account created successfully! Please confirm your email address to complete registration.")
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

def activateAccount(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can sign in to your account.')
    else:
        return HttpResponse('Activation link is invalid!')

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
    searchArticle.objects.all().delete()
    query = request.GET.get('search')
    data = requests.get('https://newsapi.org/v2/top-headlines?country=us&q='+str(query)+'&apiKey=6894e635a38d4de3be2367635985676d').json()
    #print(response)
    if(data["articles"] == []):
        message = "No results found for "+query
        result = {
            'message': message
        }
        return render(request, 'app/search.html', result)
    
    url = []
    texthold = []
    titlehold = []

    for z in range(0, len(data["articles"])):
        url.append(data["articles"][z]["url"])

    session = requests.session()
    for site in url:
        req = session.get(site)
        doc = BeautifulSoup(req.content, 'html.parser')
        title = doc.title
        txt = doc.findAll('p')

        clean = re.compile('<.*?>')

        cleantext = clean.sub('', str(txt))
        cleantext = cleantext.replace("\\n", "").replace("\\r", "").replace("\\t", "")
        cleantext = unicode(cleantext).decode('unicode_escape').encode('ascii', 'ignore')
        texthold.append(cleantext.replace("\"", "").replace(".,", ".").replace("?,", ".").replace("!,", "."))
        
        cleantitle = clean.sub('', str(title))
        cleantitle = cleantitle.replace("\\n", "").replace("\\r", "").replace("\\t", "")
        cleantitle = cleantitle.decode('utf-8').encode('utf-8')
        cleantitle = cleantitle.decode('unicode_escape').encode('ascii', 'ignore')
        cleantitle = cleantitle.replace("\"", "").replace(".,", ".").replace("?,", ".").replace("!,", ".")
        titlehold.append(cleantitle.translate(None, '\n|\\":\'?\"'))



    for z in range(0, len(data["articles"])):
        urlImage = data["articles"][z]["urlToImage"]
        if(urlImage == None):
            continue
        title = titlehold[z]
        if(searchArticle.objects.filter(title=title)):
            continue
        description = data["articles"][z]["description"]
        author = data["articles"][z]["author"]
        publishedAt = data["articles"][z]["publishedAt"]
        source = data["articles"][z]["source"]["name"]
        url = data["articles"][z]["url"]
        text = (" ".join(texthold[z].split())).replace(" ,","")
            
        sentiment = Vader_Sentiment(text)

        searchArticle.objects.create(title=title, author=author, description=description, urlImage=urlImage, url=url, source=source, text=text, publishedOn=publishedAt, sentimentNeg=sentiment["neg"], sentimentNeu=sentiment["neu"], sentimentPos=sentiment["pos"])

    Articles = searchArticle.objects.all()           
        
    result = {
        'query': query,
        'Articles': Articles
    }
    return render(request, 'app/search.html', result)