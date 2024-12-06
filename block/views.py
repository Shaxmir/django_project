from datetime import datetime
from typing import List

from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from block.forms.forms import TasksForm, BookForm, MessageForm, PostForm, PollForm, OptionForm
from block.management.commands.filters import Command
from block.models import Tasks, Book, Post, Message, Poll
from block.models.poll import Option, User_poll


# Класс для вывода всех страниц
class BasePage(TemplateView):
    """Обработка динамических страниц в зависимости от переданного параметра `page` в URL"""

    template_mapping = {
        'index': 'index.html',
        'about': 'about.html',
        'catalog': 'catalog.html',
        'contact': 'contacts.html',
        'task' : 'Tasks/task.html',
        'post' : 'Post/posts.html',
        'books' : 'Books/books.html',
        'chat' : 'Message/chat.html',
        'polls' : 'Polls/pulls.html'
    }
    def get_template_names(self) -> List[str]:
        """
        Возвращает список шаблонов в зависимости от переданного параметра `page` в URL.

        Если страница не найдена в словаре шаблонов, выбрасывает ошибку 404.
        """
        # Получаем параметр 'page' из URL или используем 'index' по умолчанию
        page = self.kwargs.get('page', 'index')
        # Если шаблон не найден, выбрасываем ошибку 404
        template = self.template_mapping.get(page)
        if not template:
            raise Http404(f"Page '{page}' not found. Please check the URL or return to the <a href='/'>home page</a>.")
        # Возвращаем список шаблонов (даже если один шаблон, нужно вернуть список)
        return [template]

    def get_context_data(self, **kwargs):
        """
        Добавляет текущую дату в контекст, чтобы она отображалась на всех страницах.
        """

        # Получаем контекст от родительского класса
        context = super().get_context_data(**kwargs)
        # Добавляем текущую дату в контекст
        context['my_date'] = datetime.now()

        page = self.kwargs.get('page')
        filter = self.request.GET.get('filter')


        if page == 'task':
            if filter == 'true':
                # Показывать только выполненные задачи
                tasks = Tasks.objects.filter(is_completed=True).order_by('-is_completed')
                print('TRUE')
            elif filter == 'false':
                # Показывать только невыполненные задачи
                tasks = Tasks.objects.filter(is_completed=False).order_by('is_completed')
                print('FALSE')
            else:
                # Показывать все задачи
                tasks = Tasks.objects.all()
                print('NICIGO')

            context['task'] = tasks
        else:
            # Словарь для других данных
            data_fetchers = {
                'books': Book.objects.all(),
                'chat': Message.objects.all(),
                'post': Post.objects.all(),
                'polls': Poll.objects.all(),
            }

            fetch_data = data_fetchers.get(page, [])
            context[page] = fetch_data

        return context



# Класс для вывода деталей
class ObjectDetailView(TemplateView):
    template_mapping = {
        'books': 'Books/books.html',
        'task': 'Tasks/tasks.html',
        'post': 'Post/posts.html',
        'chat': 'Message/chat.html',
        'polls': 'Polls/pull.html',
    }

    model_mapping = {
        'books': Book,
        'task': Tasks,
        'post': Post,
        'chat': Message,
        'polls': Poll,
    }

    def get_template_names(self) -> List[str]:
        page = self.kwargs.get('page')
        template = self.template_mapping.get(page)
        if not template:
            raise Http404(f"Page '{page}' not found.")
        return [template]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_date'] = datetime.now()
        page = self.kwargs.get('page')
        object_id = self.kwargs.get('id')

        model = self.model_mapping.get(page)
        if not model:
            raise Http404(f"Model for page '{page}' not found.")

        try:
            context['books'] = model.objects.get(id=object_id)
            print('ID: ', object_id, 'PAGE: ', page, 'MODEL: ', model.objects.get(id=object_id), 'MODEL NAME: ', model )

        except model.DoesNotExist:
            raise Http404(f"Object with id {object_id} not found in '{page}'.")

        return context#


# Класс для создания объектов в БД
class CreatedMaster(CreateView):

    model_mapping = {
        'task': Tasks,
        'book': Book,
        'post': Post,
        'chat': Message,
        'poll': Poll
    }
    template_mapping = {
        'task': 'Tasks/create.html',
        'book': 'Books/create.html',
        'post': 'Post/create.html',
        'chat': 'Message/create.html',
        'poll': 'Polls/create.html',
    }
    form_mapping = {
        'task': TasksForm,
        'book': BookForm,
        'chat': MessageForm,
        'post': PostForm,
        'poll': PollForm,
        'option': OptionForm
    }

    def get_template_names(self):

        page = self.kwargs.get('page')
        template = self.template_mapping.get(page)
        if not template:
            raise Http404('Нет такой страницы!')
        return [template]

    def get_form_class(self):
        page = self.kwargs.get('page')
        form_class = self.form_mapping.get(page)

        if not form_class:
            raise Http404('Проблема с формой')
        return form_class

    def get_model(self):
        page = self.kwargs.get('page')
        model = self.model_mapping.get(page)
        if not model:
            raise Http404('Модель не найдена. ОШИБКА!!!')
        return model

    def get_success_url(self):
        page = self.kwargs.get('page')
        return reverse_lazy('pages', kwargs={'page': page})


# Класс для редактирования объектов БД
class EditMaster(UpdateView):
    model_mapping = {
        'task': Tasks,
        'book': Book,
        'post': Post,
        'chat': Message,
        'poll': Poll
    }
    template_mapping = {
        'task': 'Tasks/edit.html',
        'book': 'Books/edit.html',
        'post': 'Post/edit.html',
        'chat': 'Message/edit.html',
        'poll': 'Polls/edit.html',
    }
    form_mapping = {
        'task': TasksForm,
        'book': BookForm,
        'chat': MessageForm,
        'post': PostForm,
        'poll': PollForm,
        'option': OptionForm
    }

    def get_template_names(self):

        page = self.kwargs.get('page')
        template = self.template_mapping.get(page)
        if not template:
            raise Http404('Нет такой страницы!')
        return [template]

    def get_form_class(self):
        page = self.kwargs.get('page')
        form_class = self.form_mapping.get(page)

        if not form_class:
            raise Http404('Проблема с формой')
        return form_class

    def get_model(self):
        page = self.kwargs.get('page')
        model = self.model_mapping.get(page)
        if not model:
            raise Http404('Модель не найдена. ОШИБКА!!!')
        return model

    def get_object(self):
        # Получаем объект по ID для редактирования
        model = self.get_model()
        pk = self.kwargs.get('id')
        return model.objects.get(id=pk)



    def get_success_url(self):
        page = self.kwargs.get('page')
        return reverse_lazy('pages', kwargs={'page': page})



# Класс которым удаляем объекты из БД
class DeleteMaster(DeleteView):
    model_mapping = {# Указываем модель, с которой работает класс
        'task': Tasks,
        'book': Book,
        'post': Post,
        'chat': Message,
        'poll': Poll
    }
    template_mapping = {# Шаблон для подтверждения удаления
        'task': 'Tasks/delete.html',
        'book': 'Books/delete.html',
        'post': 'Post/delete.html',
        'chat': 'Message/delete.html',
        'poll': 'Polls/delete.html',
    }
    def get_template_names(self):
        """
            Находим страницу
        """
        page = self.kwargs.get('page')
        template = self.template_mapping.get(page)
        if not template:
            raise Http404('Нет такой страницы!')
        return [template]

    def get_model(self):
        """
            Находим модель по названию `page`
        """
        page = self.kwargs.get('page')
        model = self.model_mapping.get(page)
        if not model:
            raise Http404('Модель не найдена. ОШИБКА!!!')
        return model

    def get_object(self):
        """
            Находим объект по переданному ID
        """
        model = self.get_model()
        pk = self.kwargs.get('id')
        return model.objects.get(id=pk)

    def get_success_url(self):
        page = self.kwargs.get('page')
        return reverse_lazy('pages', kwargs={'page': page})





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
        task_create.full_clean()
        task_create.save()
    return HttpResponseRedirect('/task')


def edit(request, id):
    try:
        task_edit = Tasks.objects.get(id=id)

        if request.method == 'POST':
            task_edit.title = request.POST.get('title')
            task_edit.description = request.POST.get('description')
            task_edit.full_clean()
            task_edit.save()
            return HttpResponseRedirect('/task')
        else:
            return render(request, 'Tasks/edit.html', {'task_edit': task_edit})
    except Tasks.DoesNotExist:
        return HttpResponseNotFound("<h2>Ошибочка при редактировании</h2>")


def delete(request, id):
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
    return render(request, 'author.html', {'author': author, 'my_date': datetime.now()})


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


def vote(request, id):
    id = request.POST.get('answer')
    options = get_object_or_404(Option, id=id)
    poll_name = get_object_or_404(Poll, id=options.poll_id)

    if request.method == 'POST':
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_address:
            ip_address = ip_address.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        user_poll = User_poll.objects.filter(poll_id=options.poll_id, ip_address=ip_address)
        if user_poll:
            return HttpResponseNotFound('<h1>Вы же голосовали</h1><br><a href="/polls">Вернуться к опросам</a>')
        else:
            user_in = User_poll()
            user_in.ip_address = ip_address
            user_in.poll_id = options.poll_id
            user_in.save()
            options.votes = F('votes') + 1
            options.save()

    return HttpResponse('<h1>Вы проголосовали</h1><br><a href="/polls">Вернуться к опросам</a>')


def poll_detales(request, id):
    pull = Poll.objects.filter(id=id)
    option = Option.objects.filter(poll_id=id)
    return render(request, 'Polls/pull.html', {'pull': pull, 'option': option, 'my_date': datetime.now()})
