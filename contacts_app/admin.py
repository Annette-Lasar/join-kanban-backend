from django.contrib import admin
from contacts_app.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'color']


