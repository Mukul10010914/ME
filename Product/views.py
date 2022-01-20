from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.conf import settings
from Product.models import item

def addp(request):
	if request.method == "POST":
		t = request.POST.get('type')
		name = request.POST.get('name')
		description = request.POST.get('description')
		
		i = item(name=name, description=description, code=t)
		i.save()

		return redirect('/Product/Add/')
	else:
		return render(request, "add_product.html", {})

def viewp(request):
	e = item.objects.filter(code="Elastic")
	v = item.objects.filter(code="Velcro")
	return render(request, "view_product.html", {'e':e, 'v':v})