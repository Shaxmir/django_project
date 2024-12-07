from django.contrib import admin
from block.models import Book, Tasks, Post, Poll, Message
from block.models.poll import Option


# Register your models here.


class UpdatePost(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Book)
admin.site.register(Message)
admin.site.register(Tasks)
admin.site.register(Poll)
admin.site.register(Option)
admin.site.register(Post, UpdatePost)