"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect

import requests

from app.forms import BootstrapRegistrationForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def getData(): 
    #Retrieve data for backend
    response = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=6894e635a38d4de3be2367635985676d")
    response = response.json()

    sourceName = []
    author = []
    title = []
    description = []
    url = []
    urlImage = []
    publishedAt = []


    for i in range(0,19):
        sourceName.append(response["articles"][i]["source"]["name"]) 
        author.append(response["articles"][i]["author"]) 
        title.append(response["articles"][i]["title"])
        description.append(response["articles"][i]["description"])
        url.append(response["articles"][i]["url"])
        urlImage.append(response["articles"][i]["urlToImage"])
        publishedAt.append(response["articles"][i]["publishedAt"])
    
    Article = {
        'Source': sourceName,
        'Author': author,
        'Title': title,
        'Description': description,
        'Url': url,
        'UrlImage': urlImage,
        'PublishedAt': publishedAt,
        'range': range(10)
    }
    return Article

#def home(request):
#    assert isinstance(request, HttpRequest)
#    Article = getData()
#    return render(
#        request,
#        'app/index2.html',
#        Article
#        )

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
