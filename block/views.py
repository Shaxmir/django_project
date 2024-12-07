from datetime import datetime
from typing import List

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse, Http404, \
    HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
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
        'task': 'Tasks/task.html',
        'post': 'Post/posts.html',
        'books': 'Books/books.html',
        'chat': 'Message/chat.html',
        'polls': 'Polls/pulls.html'
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
                print('Фильтр задач: TRUE')
            elif filter == 'false':
                # Показывать только невыполненные задачи
                tasks = Tasks.objects.filter(is_completed=False).order_by('is_completed')
                print('Фильтр задач: FALSE')
            else:
                # Показывать все задачи
                tasks = Tasks.objects.all()
                print('Ничего')

            context['task'] = tasks


        elif page == 'books':
            # Получение фильтра по автору из GET-запроса
            author_filter = self.request.GET.get('author')
            # Получение фильтра по цене из GET-запроса
            price_filter = self.request.GET.get('price')
            # Начинаем с базового QuerySet
            books = Book.objects.all()
            # Применяем фильтр по автору, если указан
            if author_filter:
                books = books.filter(author__icontains=author_filter)

            # Применяем фильтр по цене, если указан
            if price_filter == 'true':
                books = books.order_by('-price')  # По убыванию цены
                print('Фильтр книг по цене: TRUE')

            elif price_filter == 'false':
                books = books.order_by('price')  # По возрастанию цены
                print('Фильтр книг по цене: FALSE')
            # Передаём отфильтрованные данные в контекст
            context['books'] = books

        else:
            # Словарь для других данных
            data_fetchers = {
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
            if page == 'books':
                context['books'] = model.objects.get(id=object_id)
            elif page == 'post':
                context['post'] = model.objects.get(id=object_id)
            print('ID: ', object_id, 'PAGE: ', page, 'MODEL: ', model.objects.get(id=object_id), 'MODEL NAME: ', model)

        except model.DoesNotExist:
            raise Http404(f"Object with id {object_id} not found in '{page}'.")

        return context  #


# Класс для создания объектов в БД
class CreatedMaster(CreateView):
    model_mapping = {
        'task': Tasks,
        'books': Book,
        'post': Post,
        'chat': Message,
        'poll': Poll
    }
    template_mapping = {
        'task': 'Tasks/create.html',
        'books': 'Books/create.html',
        'post': 'Post/create_post.html',
        'chat': 'Message/create.html',
        'poll': 'Polls/create.html',
    }
    form_mapping = {
        'task': TasksForm,
        'books': BookForm,
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
        'books': Book,
        'post': Post,
        'chat': Message,
        'poll': Poll
    }
    template_mapping = {
        'task': 'Tasks/edit.html',
        'books': 'Books/book_edit.html',
        'post': 'Post/edit_post.html',
        'chat': 'Message/edit.html',
        'poll': 'Polls/edit.html',
    }
    form_mapping = {
        'task': TasksForm,
        'books': BookForm,
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
        obj = get_object_or_404(model, id=pk)
        return obj

    def get_success_url(self):
        page = self.kwargs.get('page')
        return reverse_lazy('pages', kwargs={'page': page})


# Класс которым удаляем объекты из БД
class DeleteMaster(DeleteView):
    model_mapping = {  # Указываем модель, с которой работает класс
        'task': Tasks,
        'books': Book,
        'post': Post,
        'chat': Message,
        'poll': Poll
    }
    template_mapping = {  # Шаблон для подтверждения удаления
        'task': 'Tasks/delete.html',
        'books': 'Books/delete.html',
        'post': 'Post/delete_post.html',
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


# Функция для покупки книг
def sell(request, id):
    bookSell = get_object_or_404(Book, id=id)
    print(bookSell)
    if bookSell.stock > 0:
        bookSell.stock -= 1
        bookSell.save()
        return JsonResponse({'success': True, 'message': 'Книга продана'})
    return JsonResponse({'success': False, 'message': 'Неверный метод запроса'})


