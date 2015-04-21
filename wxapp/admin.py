from django.contrib import admin

from wxapp.models import clothes
from wxapp.models import user
# Register your models here.

class clothesAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'category', 'season', 'tag', 'choose_count', 'image_filename')

class userAdmin(admin.ModelAdmin):
	list_display = ('id', 'nickname', 'openid')

admin.site.register(clothes, clothesAdmin)
admin.site.register(user, userAdmin)