from django.contrib import admin
from block.models import Book, Tasks, Post
# Register your models here.


class UpdatePost(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Book)
admin.site.register(Tasks)
admin.site.register(Post, UpdatePost)