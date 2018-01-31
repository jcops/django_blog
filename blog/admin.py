from django.contrib import admin

# Register your models here.
from .models import Post,Tag,Category


class PostAdmin(admin.ModelAdmin):
    list_display = ['title','create_time','modified_time','category','author']
    search_fields = ['title']

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)