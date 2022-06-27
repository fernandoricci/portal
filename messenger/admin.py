from django.contrib import admin

from messenger.models import Message, Thread

class ThreadAdmin(admin.ModelAdmin):
    icon_name = 'message'
    list_display = ('updated',)
class MessageAdmin(admin.ModelAdmin):
    icon_name = 'markunread'
    list_display = ('user', 'created')
    
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message, MessageAdmin)

