from django.contrib import admin
from django.urls import path, include
from Usuario import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('generos_favoritos/', views.generos_favoritos, name='generos_favoritos'),
    path('buscar/', views.buscar_contenido, name='buscar_contenido'),


    #control usuario
    path('Usuario/Inicio/', views.inicio_usuario, name='Usuario_Inicio'),
    path('Usuario/Sencillo/<int:cancion_id>', views.sencillo_usuario, name='Usuario_Sencillo'),
    path('Usuario/Album/<int:album_id>', views.album_usuario, name='Usuario_Album'),
    path('Usuario/generos/', views.generos_usuario, name='Usuario_Generos'),
    path('Usuario/genero/<int:genero_id>', views.genero_usuario, name='Usuario_Genero'),
    path('Usuario/Artistas/', views.artistas_usuario, name='Usuario_Artistas'),
    path('Usuario/Artista/<int:artista_id>', views.artista_usuario, name='Usuario_Artista'),
    path('Usuario/Playlists/', views.playlists_usuario, name='Usuario_Playlists'),
    
    path('Usuario/configuracion/', views.configuracion_usuario, name='Usuario_Configuracion'),
   

    #registros y creaciones
    path('registrar_reproduccion/<int:cancion_id>/', views.registrar_reproduccion, name='registrar_reproduccion'),
    path('Usuario/crear-playlist/', views.crear_playlist, name='crear_playlist'),
    


    

    #control artista
    path('Artista/Inicio/', views.inicio_artista, name='Artista_Inicio'),
    path('Artista/nueva-musica/', views.nueva_musica_artista, name='Artista_NuevaMusica'),
    path('Artista/nueva-musica/sencillo/', views.nueva_musica_artista_sencillo, name='Artista_NuevaMusica_Sencillo'),
    path('Artista/nueva-musica/album/', views.nueva_musica_artista_album, name='Artista_NuevaMusica_Album'),
    path('Artista/configuracion/', views.configuracion_artista, name='Artista_Configuracion'),
    path('Artista/archivos/', views.archivos_artista, name='Artista_Archivos'),
    path('Artista/sencillo/<int:cancion_id>', views.sencillo_artista, name='Artista_Sencillo'),
    path('Artista/album/<int:album_id>', views.album_artista, name='Artista_Album')
    


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
