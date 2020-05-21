from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Subject, Tag, Question, History

admin.site.register(Subject)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(History)
admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.site_header = "Machine Learning"
admin.site.site_title = "Machine Learning Portal"
admin.site.index_title = "Bienvenido al portal de administración de Machine Learning"

