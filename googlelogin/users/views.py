from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from google.oauth2 import id_token
from google.auth.transport import requests
import os
# Create your views here.

def home(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect("/")
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)

    # In a real app, I'd also save any new user here to the database. See below for a real example I wrote for Photon Designer.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    request.session['user_data'] = user_data

    return redirect('sign_in')