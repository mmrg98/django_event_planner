from django.contrib import admin
from .models import Events, Book


# ---- new ----
admin.site.register(Events)
admin.site.register(Book)
