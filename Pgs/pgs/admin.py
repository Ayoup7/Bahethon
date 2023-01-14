from django.contrib import admin
from .models import Eligible, Degree, Specialty, Departments, Colleges, Universities, Users, UserFile, home, News, Tokens
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.models import User
# Register your models here.


class AccountInLine(admin.StackedInline):
    model = Users
    can_delete = False
    verbose_name = 'user Information'

class UserFileInLine(admin.StackedInline):
    model = UserFile
    can_delete = False
    verbose_name = 'user Paper'

class TokensInLine(admin.StackedInline):
    model = Tokens
    can_delete = False
    verbose_name = 'user Tokens'

class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInLine, UserFileInLine, TokensInLine)

class ThingInline(admin.TabularInline):
    model = Specialty

class SpecialtyAdmin(admin.ModelAdmin):
    inlines = [
        ThingInline,
    ]




class homeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)  
admin.site.register(Eligible)
admin.site.register(Degree)
admin.site.register(Universities)
admin.site.register(Colleges)
admin.site.register(Departments, SpecialtyAdmin)
admin.site.register(Specialty)
admin.site.register(home, homeAdmin)
admin.site.register(News)
