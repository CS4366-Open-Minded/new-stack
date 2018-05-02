"""
Definition of views.
"""
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Article,FactCheck,searchArticle, userArticle, shareArticle
import requests
from bs4 import BeautifulSoup
import re
import string
import json
import sys
import os
from nltk.corpus import stopwords
from concept_extraction import concept_extractor
from concept_compare import concept_checker
from Vader_Sentiment_Analyzer import Vader_Sentiment
from voting_information import get_upcoming_election
from PieChart import sentimentChart 
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
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app.forms import BootstrapRegistrationForm
from nltk import tokenize

from datetime import datetime

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    Articles = getData()

    return render(
        request,
        'app/index.html', Articles
    )

def queryNewsAPI():
    pageSize = 5
    url = ('https://newsapi.org/v2/top-headlines?country=us&pageSize='+str(pageSize)+'&apiKey=723ffc551d7e4fa1b3ed28c2b6051c44')

    data = requests.get(url).json()
    return data

def parseDateTime(publishedAt):
    t = 'T'
    Z = 'Z'
    date = ''
    time = ''

    for i in publishedAt:
        if i == t:
            break
        date += i
            
    date = datetime.strptime(str(date),'%Y-%m-%d')
    date = date.strftime('%b %d, %Y')
    timestart = publishedAt.find(t)
    timeEnd = publishedAt.find(Z)

    for i in range(timestart+1, timeEnd):
        time += publishedAt[i]

    AM = 0
           
    d = datetime.strptime(time, "%H:%M:%S")
    hour = time[0:2]

    if(int(hour) != 0 and int(hour) < 12):
        d = d.strftime("%I:%M:%S")
        publishedAt = d+ ' AM'+'      '+date
    else:
        d = d.strftime("%I:%M:%S")
        publishedAt = d+' PM'+'     '+date

    return publishedAt

def factCheck():
    #get articles from NewsAPI
    data = queryNewsAPI()

    now = datetime.now()

    with open('custom_stopwords.txt') as e:
        stopwordList=e.read()+','.join(set(stopwords.words('english')))

    url = []
    for z in range(0, len(data["articles"])):
        url.append(data["articles"][z]["url"])

    session = requests.session()
    fname = "["+str(now.day)+"-"+str(now.month)+"-"+str(now.year)+"].json"
    
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

    #fact check algorithm
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

            publishedAt = parseDateTime(publishedAt)

            #Run sentiment analysis algorithm
            sentiment = Vader_Sentiment(text)

            

            Article.objects.create(title=title, author=author, description=description, urlImage=urlImage, url=url, source=source, text=text, publishedOn=publishedAt, sentimentNeg=sentiment["neg"], sentimentNeu=sentiment["neu"], sentimentPos=sentiment["pos"])

            #query to get current article id for foreign key reference to FactCheck
            query = Article.objects.get(title=title)            

            sentimentChart(sentiment["pos"], sentiment["neg"], sentiment["neu"], query.id)

            for i in range(1, len(sList)+1):
                if float(pList[i-1]) > .2:
                    sentenceNumber = i
                    similarityPercentage = pList[i-1]
                    if uList[i-1] > -1:
                        URLFact = urlHolder[uList[i-1]]
                    FactCheck.objects.create(sentenceNumber=sentenceNumber, similarityPercentage=similarityPercentage, URLFact=URLFact, article_id=query.id)



def getData(): 
    #factCheck()
    
    factContent = []
    urlFact = []
    articles = Article.objects.order_by('-id')[:12]
    facts = FactCheck.objects.all().order_by('-id')

    for fact in facts:
        fact.URLFact = fact.URLFact.replace("\n", "")
        factContent.append(fact)

    Articles = {
        'Article': articles,
        'factCheck': factContent,
    }
    return Articles

def voting(request):
    """Renders the voting information page."""
    assert isinstance(request, HttpRequest)
    message = get_upcoming_election();
    return render(
        request,
        'app/voting-information.html',
        {
            'title': 'Voting Information',
            'message':message,
            'year':datetime.now().year,
            }
        )

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
        publishedAt = parseDateTime(publishedAt)
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

def save(request):
    if request.GET.get('article'):
        query = request.GET.get('article')
        queryArticle = Article.objects.get(id=query)

        user = User.objects.get(username=request.user.username)
        #check if user already saved clicked article
        savedArticle = userArticle.objects.all()
        for article in savedArticle:
            if(article.article_id.id == queryArticle.id):
                return HttpResponseRedirect('/', messages.add_message(request, messages.INFO, "Article is already saved!"))
        userArticle.objects.create(article_id=queryArticle, userName=user)
        return HttpResponseRedirect('/', messages.add_message(request, messages.INFO, "Article has been saved"))

def savePage(request):
    content = []
    factContent = []
    urlFact = []

    articleContent = userArticle.objects.filter(userName=request.user.username) 

    for article in articleContent:
        content.append(Article.objects.filter(id=article.article_id.id))
        facts = FactCheck.objects.filter(article_id=article.article_id.id)
        for fact in facts:
            fact.URLFact = fact.URLFact.replace("\n", "")
            factContent.append(fact)
            urlFact.append(fact.URLFact)

    Articles = {
        'Articles': content,
        'factCheck': factContent,
    }
    return render(request, 'app/myArticle.html', Articles)

def share(request):
    if request.GET.get('shareArticle'):
        article_id = request.GET.get('shareArticle')
        queryArticle = Article.objects.get(id=article_id)
        user = User.objects.get(username=request.user.username)
        username = request.GET.get("username")

        if(User.objects.filter(username=username)):
            shareArticle.objects.create(article=queryArticle, sentFrom=user, sentTo=username)
        else:
            return HttpResponseRedirect('/', messages.add_message(request, messages.INFO, "Username does not exist"))
        return HttpResponseRedirect('/', messages.add_message(request, messages.INFO, "You shared an article with "+username))

def sharePage(request):
    #get all article ids that are shared with your username 
    sharedArticle = shareArticle.objects.filter(sentTo=request.user.username)
    articleContent = []
    factContent = []
    urlFact = []

    for article in sharedArticle:
        articleContent.append(Article.objects.filter(id=article.article_id))
        facts = FactCheck.objects.filter(article_id=article.article_id)
        for fact in facts:
            fact.URLFact = fact.URLFact.replace("\n", "")
            factContent.append(fact)
            urlFact.append(fact.URLFact)
    shareContent = {
        'share': sharedArticle,
        'Article': articleContent,
        'factCheck': factContent,
    }
    return render(request, 'app/share.html', shareContent)
