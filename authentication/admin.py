# Django imports
from django.contrib import admin

# Module imports
from authentication.models import User, Account

admin.site.register(User)
admin.site.register(Account)