from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from block.models import Tasks


class Command(BaseCommand):
    help = "Удаляет задачи, которым больше одного дня"

    def handle(self, *args, **kwargs):
        threshold_date = now() - timedelta(days=1)
        deleted_count, _ = Tasks.objects.filter(due_data__lt=threshold_date).delete()
        self.stdout.write(self.style.SUCCESS(f"Удалено задач: {deleted_count}"))
