from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from cuentas.models import Account 
from cuentas.models import UserProfile
from django.utils.html import format_html
class AccountAdmin(UserAdmin):

    icon_name = 'account_circle'

    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_link = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    
    icon_name = 'portrait'

    def thumbnail(self, object):
        return format_html('<img src={} width="30" style="border-radius:50%;"'.format(object.profile_picture.url))

    thumbnail.short_description = 'Imagen del Perfil'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')

admin.site.register(Account, AccountAdmin) #registro la clase Account y la AccountAdmin
admin.site.register(UserProfile, UserProfileAdmin) #registro la clase UserProfile y la UserProfileAdmin
