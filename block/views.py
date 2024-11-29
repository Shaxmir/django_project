from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from datetime import datetime

from block.management.commands.filters import Command
from block.models import Tasks
from block.management.commands import filters
# Create your views here.

def index(request):#home page
    return render(request, 'index.html', context={"my_date": datetime.now()})
def about(request):#about page
    return render(request, 'about.html', context={"my_date": datetime.now()})
def сatalog(request):#catalog shop page
    return render(request, 'catalog.html', context={"my_date": datetime.now()})
def contact(request):#contact page
    return render(request, 'contacts.html', context={"my_date": datetime.now()})
def task(request):
    task = Tasks.objects.all()
    return render(request, 'task.html', {'task': task,"my_date": datetime.now()})

def handle(request):
    handle_task = Tasks.objects.all()
    filter = Command()
    filter.handle(handle_task)
    return HttpResponseRedirect('/task')

def create(request):
    if request.method == 'POST':
        task_create = Tasks()
        task_create.title = request.POST.get('title')
        task_create.description = request.POST.get('description')
        task_create.save()
    return HttpResponseRedirect('/task')
def edit(request, id):
    try:
        task_edit = Tasks.objects.get(id=id)

        if request.method == 'POST':
            task_edit.title = request.POST.get('title')
            task_edit.description = request.POST.get('description')
            task_edit.save()
            return HttpResponseRedirect('/task')
        else:
            return render(request, 'edit.html',{'task_edit':task_edit})
    except Tasks.DoesNotExist:
        return HttpResponseNotFound("<h2>Ошибочка при редактировании</h2>")

def delete(request,id):
    try:
        task_delete = Tasks.objects.get(id=id)
        task_delete.delete()
        return HttpResponseRedirect('/task')
    except Tasks.DoesNotExist:
        return HttpResponseNotFound('<h2>Ошибочка при удалении</h2>')