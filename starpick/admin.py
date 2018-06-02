from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Entry)
admin.site.register(Like)
admin.site.register(Pick)
admin.site.register(Tag)
admin.site.register(Token)
admin.site.register(Follow)
admin.site.register(Comment)