from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.conf import settings
from .models import recipient, transport

def add(request):
	return render(request, 'beneficiary.html', {})

def addrecipient(request):
	name = request.POST.get('name')
	gstin = request.POST.get('gstin')
	add1 = request.POST.get('add1')
	add2 = request.POST.get('add2')
	phone = request.POST.get('phone_number')
	gst = request.POST.get('GST')

	r = recipient(name=name, gstin=gstin, add1=add1, add2=add2, phone=phone, gst=gst)
	r.save()

	u = User.objects.create_user(username=name, password=gstin, first_name=gstin)
	return redirect('/Beneficiary/Add/')

def addtransport(request):
	name = request.POST.get('name')
	gstin = request.POST.get('gstin')
	add = request.POST.get('add')
	location = request.POST.get('location')
	phone = request.POST.get('phone_number')

	t = transport(name=name, gstin=gstin, add=add, location=location, phone=phone)
	t.save()
	return redirect('/Beneficiary/Add')

def view(request):
	r = recipient.objects.all()
	t = transport.objects.all()
	return render(request, "view_beneficiary.html", {'r':r, 't':t})