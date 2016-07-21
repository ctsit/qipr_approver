from django.contrib import admin

from .models import Person
from .models import Project
from .models import Position
from .models import Speciality 
from .models import Organization
from .models import Category

admin.site.register(Person)
admin.site.register(Project)
admin.site.register(Position)
admin.site.register(Speciality)
admin.site.register(Organization)
admin.site.register(Category)
