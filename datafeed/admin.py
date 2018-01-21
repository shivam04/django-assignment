from django.contrib import admin
from .models import DataFeed

class DataFeedAdmin(admin.ModelAdmin):
	list_display = ["id","input_text","user"]
	class Meta:
		model = DataFeed



admin.site.register(DataFeed,DataFeedAdmin)