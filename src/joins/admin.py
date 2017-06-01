from django.contrib import admin

# Register your models here.
from .models import Join

class JoinAdmin(admin.ModelAdmin):
	list_display = ['email','friend', 'timestamp', 'updated']
	class meta:
		model = Join

admin.site.register(Join, JoinAdmin)


#admin.site.register(JoinFriends)
