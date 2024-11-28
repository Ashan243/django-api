from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models
from core.models import User
# Register your models here.




@admin.register(User)
class UserAdminInline(BaseUserAdmin):
    add_fieldsets = (None, {
        "classes": ("wide",),
        "fields": ("username", "password1", "password2", "email", "first_name", "surnanme")
    })
    

#Managing Model Views
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "username", "username_checker", "product_title"]
    list_editable = ["username"]
    
    def product_title(self, cls):
        return cls.product.item
    
    #Programmatically Generated Column
    @admin.display(ordering="username")
    def username_checker(self, username): 
        if len(username.username) == 7:
            return "Good Length"
        return "Bad Length"

@admin.register(models.Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["item"]
