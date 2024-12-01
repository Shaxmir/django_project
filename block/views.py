from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from datetime import datetime

from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from block.management.commands.filters import Command
from block.models import Tasks, Book, Post, Message, Poll
from block.management.commands import filters
from block.models.message import Author
from block.models.poll import Option, User_poll
from django.db.models import F


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
    return render(request, 'Tasks/task.html', {'task': task,"my_date": datetime.now()})
def books(request, id=None):
    if id != None:
        books = Book.objects.filter(id=id)
        return render(request, 'Books/books.html', {'books': books, 'my_date': datetime.now()})
    else:
        books = Book.objects.all()
        return render(request, 'Books/books.html', {'books': books, 'my_date': datetime.now()})
def post(request, id=None):
    if id != None:
        post = Post.objects.filter(id=id)
        post_all = Post.objects.all()
        return render(request, 'Post/posts.html', {'post': post, 'post_all': post_all, 'my_date': datetime.now()})
    else:
        post = Post.objects.all()
        return render(request, 'Post/posts.html', {'post': post, 'my_date': datetime.now()})

def chat(request):
    chat = Message.objects.all().order_by('-create_at')
    aut = Author.objects.all()
    if request.method == 'POST':
        author = Author.objects.create(author=request.POST.get('author'))
        mess = Message(content=request.POST.get('content'))
        author.message = mess
        author.message.save()
        return HttpResponseRedirect('/chat')
    else:

        return render(request, 'Message/chat.html', {'chat': chat, 'aut': aut, 'my_date': datetime.now()})
def polls(request, id=None):
    if id != None:
        pull = Poll.objects.filter(id=id)
        pull_all = Poll.objects.all()
        option = Option.objects.filter(poll_id=id)
        return render(request, 'Polls/pulls.html', {'pull': pull, 'pull_all': pull_all, 'option': option, 'my_date': datetime.now()})
    else:
        pull = Poll.objects.all()
        return render(request, 'Polls/pulls.html', {'pull': pull, 'my_date': datetime.now()})

####################Функции для задачь#####################

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
            return render(request, 'Tasks/edit.html',{'task_edit':task_edit})
    except Tasks.DoesNotExist:
        return HttpResponseNotFound("<h2>Ошибочка при редактировании</h2>")

def delete(request,id):
    try:
        task_delete = Tasks.objects.get(id=id)
        task_delete.delete()
        return HttpResponseRedirect('/task')
    except Tasks.DoesNotExist:
        return HttpResponseNotFound('<h2>Ошибочка при удалении</h2>')


####################Функции для каталога с книгами#######################

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
            return render(request, 'Books/book_edit.html', {'bookEdit': bookEdit, 'my_date': datetime.now()})
    except Book.DoesNotExist:
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

################### Функции для постов ############################





def create_post(request):
    if request.method == 'POST':
        post = Post()
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.updated_at = ''
        post.save()
        return HttpResponseRedirect('/post')
    else:
        return render(request, 'Post/create.html', {'edit_post': edit_post, 'my_date': datetime.now()})
def edit_post(request, id):
    try:
        edit_post = Post.objects.get(id=id)
        if request.method == 'POST':
            edit_post.title = request.POST.get('title')
            edit_post.content = request.POST.get('content')
            edit_post.update_at = datetime.now()
            edit_post.save()
            return HttpResponseRedirect('/post')
        else:
            return render(request, 'Post/edit.html', {'edit_post': edit_post, 'my_date': datetime.now()})
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Ошибочка при редактировании)</h2>")
def delete_post(request, id):
    try:
        del_post = Post.objects.get(id=id)
        if request.method == 'POST':
            del_post.delete()
            return HttpResponseRedirect('/post')
        else:
            return render(request, 'Post/delete_post.html', {'del_post': del_post, 'my_date': datetime.now()})
    except Post.DoesNotExist:
        return HttpResponseNotFound('<h2>Ошибочка при удалении</h2>')


#####################################Функции для опросов##################################################


def vote(request, pid, oid):
    options = get_object_or_404(Option, id=oid, poll_id=pid)
    if request.method == 'POST':
        print(request.method.POST['poll'])
    return HttpResponseRedirect('/polls')
"""    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip_address:
        ip_address = ip_address.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    user_poll = User_poll.objects.all()
    if user_poll.ip_address == ip_address and user_poll.poll_id == pid:
        return HttpResponseNotFound('Вы уже голосовали')
    else:
        user_poll.ip_address = request.POST.get('ip_address')
        user_poll.poll_id = request.POST.get('poll_id')
        user_poll.votes_id = request.POST.get('votes_id')
        user_poll.save()
    """