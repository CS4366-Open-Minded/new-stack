"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

from datetime import datetime
from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
import requests

from .forms import BootstrapRegistrationForm
from .tokens import account_activation_token

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