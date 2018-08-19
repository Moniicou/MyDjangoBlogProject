from django.contrib import admin
from .models import Post, Tag, Category

# Register your models here.

"""
帖子 Post： 
		标题 title
		创建时间 created_time
		修改时间 modified_time
		摘要	excerpt
		内容	content
		作者	author
		类别	category
		标签云	tag
"""


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_time', 'modified_time']

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register((Category))