from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.conf import settings

def home(request):
	return render(request, "home.html", {})

def signin(request):
	if request.method == 'POST':
		username = request.POST.get('companyname')
		password = request.POST.get('gstno')

		user = auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request, user)
			return redirect('/')
		else:
			messages.info(request,'INVALID CREDENTIALS')
			return render(request, "signin.html", {})

	else:
		return render(request, "signin.html", {})

def contact(request):
	return render(request, "contact.html", {})

def logout(request):
	auth.logout(request)
	return redirect('/')