from django import forms
from block.models import Tasks, Book, Message, Poll, Post
from block.models.poll import Option


class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'is_completed']

        labels = {
            'title': 'Название',
            'description': 'Описание',
            'is_completed': 'Выполнено',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливать начальные значения через instance не нужно, они будут установлены автоматически.
        if self.instance and self.instance.pk:
            # Эти строки можно оставить, если хотите контролировать видимость поля или другие атрибуты.
            self.fields['title'].widget.attrs['placeholder'] = 'Название задачи'
            self.fields['description'].widget.attrs['placeholder'] = 'Описание задачи'



class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'stock']

        labels = {
            'title': 'Название',
            'author': 'Имя автора',
            'price': 'Цена',
            'stock': 'Количество книг',
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['author', 'content']

        labels = {
            'author': 'Автор',
            'content': 'Сообщение',
        }

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title','description', 'is_active']

        labels = {
            'title': 'Название',
            'description': 'Описание',
            'is_active': 'Активное',
        }
class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text', 'votes']

        labels = {
            'text': 'Текст голосования',
            'votes': 'Количество голосов'
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

        labels = {
            'title': 'Название',
            'text': 'Описание',
        }