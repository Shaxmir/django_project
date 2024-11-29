from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from datetime import datetime

from django.template.context_processors import request

from block.management.commands.filters import Command
from block.models import Tasks
from block.management.commands import filters
from block.models import Book
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
def books(request, id=None):
    if id != None:
        books = Book.objects.filter(id=id)
        return render(request, 'books.html', {'books': books, 'my_date': datetime.now()})
    else:
        books = Book.objects.all()
        return render(request, 'books.html', {'books': books, 'my_date': datetime.now()})
#Функции для задачь

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


#Функции для каталога с книгами

def add_book(request):
    if request.method == 'POST':
        book_add = Book()
        book_add.title = request.POST.get('title')
        book_add.author = request.POST.get('author')
        book_add.price = request.POST.get('price')
        book_add.stock = request.POST.get('stock')
        book_add.save()
    return HttpResponseRedirect('/books')
def book_edit(request, id):
    try:
        bookEdit = Book.objects.get(id=id)
        if request.method == 'POST':
            bookEdit.title = request.POST.get('title')
            bookEdit.author = request.POST.get('author')
            bookEdit.price = request.POST.get('price')
            bookEdit.stock = request.POST.get('stock')
            bookEdit.save()
            return HttpResponseRedirect('/books')
        else:
            return render(request, 'book_edit.html', {'bookEdit': bookEdit, 'my_date': datetime.now()})
    except Tasks.DoesNotExist:
        return HttpResponseNotFound("<h2>Ошибочка при редактировании)</h2>")
def sell(request, id):
        bookSell = Book.objects.get(id=id)
        if bookSell.stock > 0:
            bookSell.stock -= 1
            bookSell.save()
            return JsonResponse({'success': True, 'message': 'Книга продана'})
        return JsonResponse({'success': False, 'message': 'Книга кончилась'})
def author(request, author):
    author = Book.objects.filter(author=author)
    return render(request, 'author.html',{'author': author, 'my_date': datetime.now()})