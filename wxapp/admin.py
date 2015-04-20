from django.contrib import admin

from wxapp.models import clothes
# Register your models here.

class clothesAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'category', 'season', 'tag', 'choose_count', 'image_filename')

admin.site.register(clothes, clothesAdmin)