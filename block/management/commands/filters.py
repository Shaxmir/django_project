from django.core.management.base import BaseCommand
from datetime import datetime
from block.models import Tasks


class Command(BaseCommand):
    BaseCommand.help = 'Фильтрация по дате. Если задаче больше 1 дня то она удаляется автоматически'

    def handle(self, *args, **kwargs):
        date_now = datetime.now()
        ex_date = Tasks.objects.filter(due_data__lt=date_now, is_completed=False)
        count = ex_date.count()
        ex_date.delete()
        self.stdout.write(f'Удалено {count} записей')