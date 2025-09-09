from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Cancion)
admin.site.register(Album)
admin.site.register(Genero)
admin.site.register(Playlist)
admin.site.register(Historial_reproduccion)



