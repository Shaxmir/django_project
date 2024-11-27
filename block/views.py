from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
# Create your views here.

def index(request):#home page
    return render(request, 'index.html', context={"my_date": datetime.now()})
def about(request):#about page
    return render(request, 'about.html', context={"my_date": datetime.now()})
def сatalog(request):#catalog shop page
    return render(request, 'catalog.html', context={"my_date": datetime.now()})
def contact(request):#contact page
    return render(request, 'contacts.html', context={"my_date": datetime.now()})