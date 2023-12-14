# Register your models here.
from django.contrib import admin
# import your models here
from .models import Bird, Feeding, House, Photo

# Register your models here
admin.site.register(Bird)
admin.site.register(Feeding)
admin.site.register(House)
admin.site.register(Photo)
