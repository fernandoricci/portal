from django.contrib import admin

from messenger.models import Message, Thread

class ThreadAdmin(admin.ModelAdmin):
    icon_name = 'collections_bookmark'

class MessageAdmin(admin.ModelAdmin):
    icon_name = 'collections_bookmark'

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message, MessageAdmin)

