from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(UserInfo)
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ArticleDetail)
admin.site.register(Article2Tag)
admin.site.register(ArticleUpDown)
admin.site.register(Comment)
admin.site.register(Blog)


