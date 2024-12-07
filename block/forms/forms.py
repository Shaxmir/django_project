from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

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
        fields = ['content']

        labels = {
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
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заг. (200сим)'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст (1024)',
                'rows': 5
            }),
        }
        labels = {
            'title': 'Название',
            'content': 'Описание',
        }






