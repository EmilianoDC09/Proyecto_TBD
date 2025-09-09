from django.db import models
from .storage import OverwriteStorage

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    descripcion = models.CharField(max_length=300, default="descripcion")
    contrasenia = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='Foto_perfiles/', storage= OverwriteStorage(), max_length=300, default="ruta")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    is_artist = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre
    
class Genero(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    portada = models.ImageField(upload_to='portadas/', storage= OverwriteStorage(), max_length=300, default="ruta")

    def __str__(self):
        return self.nombre    

class Album(models.Model):
    nombre = models.CharField(max_length=50)
    portada = models.ImageField(upload_to='portadas/', storage= OverwriteStorage(), max_length=300, default="ruta")
    fecha_lanzamiento = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre   
    
class Playlist(models.Model):
    nombre = models.CharField(max_length=50)
    is_favorito = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class Cancion(models.Model):
    nombre = models.CharField(max_length=50)
    duracion = models.CharField(max_length=50, default="00:00") 
    portada = models.ImageField(upload_to='portadas/', storage= OverwriteStorage(),max_length=300, default="ruta")
    fecha_lanzamiento = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_album = models.ForeignKey(Album, on_delete=models.CASCADE)
    id_genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='canciones/', storage=OverwriteStorage(), max_length=300, default="ruta")
    def __str__(self):
        return self.nombre
    def __str__(self):
        return self.nombre


class Historial_reproduccion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE)
    def __str__(self):
        return self.fecha



