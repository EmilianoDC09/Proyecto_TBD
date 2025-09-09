from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
import os
from django.conf import settings
from django.db.models import Q


# Create your views here.
def login(request):
    #limpipar la sesion
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
    print("entro a login")

    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasenia = request.POST.get('contrasenia')
        usuario = Usuario.objects.filter(correo=correo).first()
        request.session['usuario_id'] = usuario.id # Guardar el ID del usuario en la sesión
        if contrasenia == usuario.contrasenia and correo == usuario.correo:
            if usuario.is_artist:
                canciones = Cancion.objects.filter(id_usuario=usuario.id)
                albunes = Album.objects.filter(id_usuario=usuario.id)
                return render(request, 'Artista/Artista_Inicio.html', {'usuario': usuario, 'canciones': canciones, 'albunes': albunes})
            else:
                cancones_recientes = Historial_reproduccion.objects.filter(id_usuario=usuario.id)
                #cacniones aleatoreas de la base de datos 
                canciones_aleatoreas = Cancion.objects.all().order_by('?')[:10]
                # albune saleatores
                albunes_aleatoreos = Album.objects.all().order_by('?')[:5]
                return render(request, 'Usuario/Usuario_Inicio.html', {'canciones_recientes': cancones_recientes, 'canciones_aleatoreas': canciones_aleatoreas, 'albums': albunes_aleatoreos,'usuario': usuario})
        else:
            return render(request, 'Usuario/login.html', {'error': 'Correo o contraseña incorrectos'})
    else:
        return render(request, 'Usuario/login.html')
    
def register(request):
    #limpiar la sesion
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
    print("entro a register")

    if(request.method == 'POST'):
        print("entro a post")
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        contrasenia = request.POST.get('contrasenia')
        contraseniaC = request.POST.get('contraseniaC')
        is_artist = request.POST.get('isArtista')
        print("is_artist: ", is_artist)
        if is_artist == 'on':
            is_artist = True
        else:
            is_artist = False
        if contrasenia == contraseniaC:
            usuario = Usuario.objects.create(nombre=nombre, correo=correo, contrasenia=contrasenia, is_artist=is_artist)
            request.session['usuario_id'] = usuario.id
            if is_artist:
                return render(request, 'Artista/Artista_Inicio.html', {'usuario': usuario})
            else:
                return render(request, 'Usuario/Usuario_GenerosFavoritos.html', {'usuario': usuario})
        else:
            return render(request, 'Usuario/register.html', {'error': 'Las contraseñas no coinciden'})
    else:
        return render(request, 'Usuario/register.html')

def buscar_contenido(request):
    print("entro a buscar contenido")
    query = request.GET.get('q', '')
    print("query: ", query)
    if query:
        # Filtrar canciones, artistas y álbumes que coincidan con la búsqueda
        canciones = Cancion.objects.filter(Q(nombre__icontains=query) | Q(id_usuario__nombre__icontains=query))
        artistas = Usuario.objects.filter(Q(nombre__icontains=query) & Q(is_artist=True))
        albunes = Album.objects.filter(Q(nombre__icontains=query) | Q(id_usuario__nombre__icontains=query))

        resultados = {
            'canciones':[
            {'id': cancion.id, 'nombre': cancion.nombre, 'artista': cancion.id_usuario.nombre, 'album': cancion.id_album.nombre, 'genero': cancion.id_genero.nombre} for cancion in canciones
            ],
            'artistas': [
                {'id': artista.id, 'nombre': artista.nombre} for artista in artistas
            ],
            'albunes': [
                {'id': album.id, 'nombre': album.nombre, 'artista': album.id_usuario.nombre} for album in albunes
            ]
        }

        print("canciones: ")
        for cancion in canciones:
            print("cancion: ", cancion.nombre)
            print("id cancion: ", cancion.id)
            print("id artista: ", cancion.id_usuario.id)
            print("id album: ", cancion.id_album.id)
            print("id genero: ", cancion.id_genero.id)

        print("artistas: ")
        for artista in artistas:
            print("artista: ", artista.nombre)
            print("id artista: ", artista.id)

        print("albunes: ")
        for album in albunes:
            print("album: ", album.nombre)
            print("id album: ", album.id)
            print("id artista: ", album.id_usuario.id)
        return JsonResponse(resultados)
    return JsonResponse({'canciones': [], 'artistas': [], 'albunes': []})

#control usuario

def generos_favoritos(request):
    print("entro a generos favoritos")
    #Guardar los generos favoritos en la sesion 
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')  # Redirige si no hay sesión activa
    usuario = Usuario.objects.get(id=usuario_id)
    generos = Genero.objects.all()  # Obtener todos los géneros
    if request.method == 'POST':
        print("entro a post")
        generos_seleccionados = request.POST.getlist('genres')
        request.session['generos_seleccionados'] = generos_seleccionados
        print("nombre de generos seleccionados: ", generos_seleccionados)
        generos_objetos = Genero.objects.filter(nombre__in=generos_seleccionados) 
        cancones_recientes = Historial_reproduccion.objects.filter(id_usuario=usuario.id) 
        canciones_aleatoreas = Cancion.objects.all().order_by('?')[:10]
        albunes_aleatoreos = Album.objects.all().order_by('?')[:5]        
        return render(request, 'Usuario/Usuario_Inicio.html', {'canciones_recientes': cancones_recientes, 'canciones_aleatoreas': canciones_aleatoreas, 'albums': albunes_aleatoreos,'seleccion':generos_objetos,'usuario': usuario})
    else:
        print("entro a get")
        return render(request, 'Usuario/Usuario_GenerosFavoritos.html', {'usuario': usuario, 'generos': generos})

def inicio_usuario(request):
    print("entro a inicio usuario")
    usuario_id = request.session.get('usuario_id')
    generos_seleccionados = request.session.get('generos_seleccionados')
    print("generos seleccionados: ", generos_seleccionados)
    if not usuario_id:
        return redirect('login')
    usuario = get_object_or_404(Usuario, id=usuario_id)
    me_gusta = Playlist.objects.filter(id_usuario=usuario_id, is_favorito=True, nombre="Tus me gusta").first()
    if request.method == 'POST':
        print("entro a post")
        return redirect('Usuario_Inicio')  # Redirige a la misma vista para evitar reenvío de formulario
    else:
        print("entro a get")
        genero_objetos = Genero.objects.filter(nombre__in=generos_seleccionados)
        cancones_recientes = Historial_reproduccion.objects.filter(id_usuario=usuario.id)
        canciones_aleatoreas = Cancion.objects.all().order_by('?')[:10]
        albunes_aleatoreos = Album.objects.all().order_by('?')[:5]

        return render(request, 'Usuario/Usuario_Inicio.html', {
            'canciones_recientes': cancones_recientes,
            'canciones_aleatoreas': canciones_aleatoreas,
            'albums': albunes_aleatoreos,
            'seleccion': genero_objetos,
            'me_gusta': me_gusta,
            'usuario': usuario
        })
        
def sencillo_usuario(request, cancion_id):

    print("entro a sencillo usuario")
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')  # Redirige si no hay sesión activa
    usuario = Usuario.objects.get(id=usuario_id)
    cancion = Cancion.objects.get(id=cancion_id)
    artista = Usuario.objects.get(id=cancion.id_usuario.id)
    return render(request, 'Usuario/Usuario_Sencillo.html', {'usuario': usuario, 'cancion': cancion, 'artista':artista}) 
      
def album_usuario(request, album_id):
    print("entro a album usuario")
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')  # Redirige si no hay sesión activa
    usuario = Usuario.objects.get(id=usuario_id)
    if request.method == 'POST':
        print("entro a post")
    else:
        print("entro a get")
        album = Album.objects.get(id=album_id)
        canciones = Cancion.objects.filter(id_album=album_id)
        return render(request, 'Usuario/Usuario_Album.html', {'usuario': usuario, 'album': album, 'canciones': canciones})

def generos_usuario(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    usuario = Usuario.objects.get(id=usuario_id)
    generos = Genero.objects.all()  # Obtener todos los géneros
    return render(request, 'Usuario/Usuario_Generos.html', {'usuario': usuario, 'generos': generos})

def genero_usuario(request, genero_id):
    print("entro a genero usuario")
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')  # Redirige si no hay sesión activa
    usuario = Usuario.objects.get(id=usuario_id)
    genero = Genero.objects.get(id=genero_id)
    canciones = Cancion.objects.filter(id_genero=genero_id)

    print("canciones del genero: ")
    for cancion in canciones:
        print("cancion: ", cancion.nombre)
        print("id cancion: ", cancion.id)
        print("id artista: ", cancion.id_usuario.id)
        print("id album: ", cancion.id_album.id)
        print("id genero: ", cancion.id_genero.id)
    return render(request, 'Usuario/Usuario_Mix.html', {'usuario': usuario, 'genero': genero, 'canciones': canciones})

def artistas_usuario(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')  # Redirige si no hay sesión activa
    usuario = Usuario.objects.get(id=usuario_id)
    artistas = Usuario.objects.filter(is_artist=True)  # Filtrar solo los artistas
    print("artistas: ")
    for artista in artistas:
        print("artista: ", artista.nombre)
        print("id artista: ", artista.id)
        print("correo artista: ", artista.correo)
        print("foto artista: ", artista.foto.url)
    return render(request, 'Usuario/Usuario_Artistas.html', {'usuario': usuario, 'artistas': artistas})

def artista_usuario(request, artista_id):
    print("entro a artista usuario")
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')  # Redirige si no hay sesión activa
    usuario = Usuario.objects.get(id=usuario_id)
    artista = Usuario.objects.get(id=artista_id)
    canciones = Cancion.objects.filter(id_usuario=artista_id)
    albunes = Album.objects.filter(id_usuario=artista_id)
    return render(request, 'Usuario/Usuario_Artista.html', {'usuario': usuario, 'artista': artista, 'canciones': canciones, 'albums': albunes})

def registrar_reproduccion(request, cancion_id):
    print("entro a registrar reproduccion")
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return redirect('login')  # Redirige si no hay sesión activa
        usuario = Usuario.objects.get(id=usuario_id)
        cancion = Cancion.objects.get(id=cancion_id)
        # Registrar la reproducción en el historial
        Historial_reproduccion.objects.create(
            id_usuario=usuario,
            id_cancion=cancion
        )
    
    return redirect('Usuario_Sencillo', cancion_id=cancion_id)  # Redirige a la vista del sencillo

def crear_playlist(request):
    print("entro a crear playlist")
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        print("no hay usuario activo")
        return redirect('login')  # Redirige si no hay sesión activa
    usuario = Usuario.objects.get(id=usuario_id)
    if request.method == 'POST':
        print("entro a post")
        nombre_playlist = request.POST.get('name')
        
        nueva_playlist = Playlist.objects.create(
            nombre=nombre_playlist,
            is_favorito=False,  # Por defecto, la playlist no es favorita
            id_usuario=usuario
        )
        nueva_playlist.save()  # Guardar la playlist en la base de datos
        return redirect('Usuario_Inicio')  # Redirige a la vista de inicio del usuario
    else:
        print("entro a get")
        return render(request, 'Usuario/Usuario_CrearPlaylist.html', {'usuario': usuario})

def detalles_playlist(request, playlist_id):

    print("entro a detalles playlist")
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')  # Redirige si no hay sesión activa
    usuario = Usuario.objects.get(id=usuario_id)
    playlist = get_object_or_404(Playlist, id=playlist_id, id_usuario=usuario)
    
    if request.method == 'POST':
        print("entro a post")
        # Aquí puedes manejar la lógica para agregar canciones a la playlist
        return redirect('Usuario_Inicio')  # Redirige a la vista de inicio del usuario
    else:
        print("entro a get")
        canciones = Cancion.objects.filter(id_playlist=playlist_id)  # Obtener las canciones de la playlist
        return render(request, 'Usuario/Usuario_DetallesPlaylist.html', {'usuario': usuario, 'playlist': playlist, 'canciones': canciones})

def playlists_usuario(request):

    print("entro a playlists usuario")
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')  # Redirige si no hay sesión activa
    usuario = Usuario.objects.get(id=usuario_id)
    playlists = Playlist.objects.filter(id_usuario=usuario)  # Obtener las playlists del usuario
    #cacnciones de la playlist
    
    print("playlists: ")
    for playlist in playlists:
        print("playlist: ", playlist.nombre)
        print("id playlist: ", playlist.id)
        print("is favorito: ", playlist.is_favorito)
    return render(request, 'Usuario/Usuario_Playlists.html', {'usuario': usuario, 'playlists': playlists})

def configuracion_usuario(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    usuario = Usuario.objects.get(id=usuario_id)
    if request.method == 'POST':
        accion = request.POST.get('action')
        print("accion: ", accion)
        #actualizar mail
        if accion == 'actualizar_email':
            nuevo_email = request.POST.get('new-email')
            confirmacion_email = request.POST.get('confirm-email')
            contrasenia = request.POST.get('current-password')
            if nuevo_email != confirmacion_email:
                return render(request, 'Usuario/Usuario_Configuracion.html', {'usuario': usuario, 'error': 'Los correos no coinciden'})
            if contrasenia != usuario.contrasenia:
                return render(request, 'Usuario/Usuario_Configuracion.html', {'usuario': usuario, 'error': 'Contraseña incorrecta'})
            # Actualizar el correo electrónico del usuario
            usuario.correo = nuevo_email
            usuario.save()
            return redirect('Usuario_Configuracion')
        #actualizar contrasenia
        elif accion == 'actualizar_contrasenia':
            print("entro a actualizar contrasenia")
            nueva_contrasenia = request.POST.get('new-password')
            confirmacion_contrasenia = request.POST.get('confirm-new-password')
            contrasenia_actual = request.POST.get('current-password-input')
            print("nueva contrasenia: ", nueva_contrasenia)
            print("confirmacion contrasenia: ", confirmacion_contrasenia)
            print("contrasenia actual: ", contrasenia_actual)
            if nueva_contrasenia != confirmacion_contrasenia:
                print("las contraseñas no coinciden")
                return render(request, 'Usuario/Usuario_Configuracion.html', {'usuario': usuario, 'error': 'Las contraseñas no coinciden'})
            if contrasenia_actual != usuario.contrasenia:
                print("contraseña incorrecta")
                return render(request, 'Usuario/Usuario_Configuracion.html', {'usuario': usuario, 'error': 'Contraseña incorrecta'})
            # Actualizar la contraseña del usuario
            usuario.contrasenia = nueva_contrasenia
            usuario.save()
            return redirect('Usuario_Configuracion')
        #actualizar nombre
        elif accion == 'actualizar_usuario':
            print("entro a actualizar nombre")
            nuevo_nombre = request.POST.get('new-username')
            contrasenia = request.POST.get('password-for-username')
            if contrasenia != usuario.contrasenia:
                return render(request, 'Usuario/Usuario_Configuracion.html', {'usuario': usuario, 'error': 'Contraseña incorrecta'})
            # Actualizar el nombre del usuario
            usuario.nombre = nuevo_nombre
            usuario.save()
            return redirect('Usuario_Configuracion')
    else:
        print("entro a get")
        return render(request, 'Usuario/Usuario_Configuracion.html', {'usuario': usuario})

#control artista 
def inicio_artista(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')  # Redirige si no hay sesión activa
    usuario = Usuario.objects.get(id=usuario_id)
    canciones = Cancion.objects.filter(id_usuario=usuario.id)
    albunes = Album.objects.filter(id_usuario=usuario.id)
    return render(request, 'Artista/Artista_Inicio.html', {'usuario': usuario, 'canciones': canciones, 'albunes': albunes})   

def nueva_musica_artista(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')  # Redirige si no hay sesión activa
    usuario = Usuario.objects.get(id=usuario_id)
    canciones = Cancion.objects.filter(id_usuario=usuario.id)
    albunes = Album.objects.filter(id_usuario=usuario.id)
    return render(request, 'Artista/Artista_NuevaMusica.html', {'usuario': usuario, 'canciones': canciones, 'albunes': albunes})

def nueva_musica_artista_sencillo(request):
    if request.method == 'POST':
        print("entro a post")
        nombre = request.POST.get('nombre_cancion')
        duracion_segundos = request.POST.get('cancion_duracion')
        id_usuario = request.session.get('usuario_id')
        id_genero = request.POST.get('genero_id')

        cancion_file = request.FILES.get('cancion')
        portada_file = request.FILES.get('portada')

        #convertir la duracion a un formato de minutos y segundos
        segundos = float(duracion_segundos)
        minutos = int(segundos // 60)
        segundos_restantes = int(segundos % 60)
        duracion = f"{minutos:02}:{segundos_restantes:02}"  # Formato MM:SS

        print("nombre: ", nombre)
        print("duracion: ", duracion)
        nueva_cancion = Cancion(
            nombre=nombre,
            duracion=duracion,
            id_usuario=Usuario.objects.get(id=id_usuario),
            id_album=Album.objects.get(id=12),  # Asignar None si no hay álbum
            id_genero=Genero.objects.get(id=id_genero),
        )

        nueva_cancion.archivo.save(cancion_file.name, cancion_file)
        nueva_cancion.portada.save(portada_file.name, portada_file)

        nueva_cancion.save()  # Guardar la canción en la base de datos
        
        return redirect('Artista_Archivos')
    else:
        print("entro a get")
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return redirect('login')  # Redirige si no hay sesión activa
        usuario = Usuario.objects.get(id=usuario_id)
        generos = Genero.objects.all()  # Obtener todos los géneros
        return render(request, 'Artista/Artista_NuevaMusica_Sencillo.html', {'usuario': usuario, 'generos': generos}) 

def nueva_musica_artista_album(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')  # Redirige si no hay sesión activa
    usuario = Usuario.objects.get(id=usuario_id)
    generos = Genero.objects.all()
    if request.method == 'POST':
        print("entro a post")
        #Datos del album 
        nombre_album = request.POST.get('nombre_album')
        portada_album = request.FILES.get('portada')
        genero = request.POST.get('genero_album')
        #Generar album
        album = Album.objects.create(
            nombre=nombre_album,
            portada=portada_album,
            id_usuario=usuario,
            id_genero=Genero.objects.get(id=genero),
        )
        album.portada.save(portada_album.name, portada_album)
        album.save()  # Guardar el álbum en la base de datos
        #Lsta de canciones
        nombres_canciones = request.POST.getlist('cancion_nombre[]')
        duraciones_canciones = request.POST.getlist('cancion_duracion[]')
        archivos_canciones = request.FILES.getlist('cancion_archivo[]')
        # Guardar  cada cancion en la base de datos
        for nombre, duracion, archivo in zip(nombres_canciones, duraciones_canciones, archivos_canciones):
            Cancion.objects.create(
                nombre=nombre,
                duracion=duracion,
                id_usuario=usuario,
                id_album=album,
                id_genero=album.id_genero,
                archivo=archivo,
                portada= album.portada,  # Asignar la portada del álbum a la canción
            )
            # Guardar cada archivo de canción en la base de datos

        return redirect('Artista_Archivos')  # Redirige a la vista de archivos del artista
    else:
        return render(request, 'Artista/Artista_NuevaMusica_Album.html', {'usuario': usuario, 'generos': generos})

def configuracion_artista(request):
    # Obtener el ID del usuario de la sesión
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    usuario = Usuario.objects.get(id=usuario_id)
    if request.method == 'POST':
        print("entro a post")
        nombre = request.POST.get('nombreArtistico')
        descripcion = request.POST.get('descripcion')
        foto_perfil = request.FILES.get('fotoPerfil')
        #Hacer modificaciones al usuario
        usuario.nombre = nombre
        usuario.descripcion = descripcion
        if foto_perfil:
            # Eliminar la foto anterior si existe
            if usuario.foto and usuario.foto.name != 'ruta':
                try:
                    os.remove(os.path.join(settings.MEDIA_ROOT, usuario.foto.name))
                except FileNotFoundError:
                    pass
            usuario.foto.save(foto_perfil.name, foto_perfil)
        usuario.save()
        # Redirigir a la vista de configuración del artista
        return redirect('Artista_Configuracion')
    else:
        print("entro a get")
        generos = Genero.objects.all()  # Obtener todos los géneros
        return render(request, 'Artista/Artista_Configuracion.html', {'usuario': usuario, 'generos': generos})

def archivos_artista(request):

    if request.method == 'POST' and 'eliminar_cancion' in request.POST:
        cancion_id = request.POST.get('cancion_id')
        cancion = get_object_or_404(Cancion, id=cancion_id)
        if cancion.archivo and cancion.archivo.name != 'ruta':
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, cancion.archivo.name))
            except FileNotFoundError:
                pass
        #eliminar la ruta de la portada
        if cancion.portada and cancion.portada.name != 'ruta':
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, cancion.portada.name))
            except FileNotFoundError:
                pass

        cancion.delete()  # Eliminar la canción de la base de datos
        return redirect('Artista_Archivos')  # Redirige a la vista de archivos del artista
    else:
        print("entro a archivos artista")
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return redirect('login')  # Redirige si no hay sesión activa
        usuario = Usuario.objects.get(id=usuario_id)

        canciones = usuario.cancion_set.all()  # Obtener todas las canciones del artista
        return render(request, 'Artista/Artista_Archivos.html', {'usuario': usuario, 'canciones': canciones})

def borra_cancion(request, cancion_id):

    print("entro a borrar cancion")
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')  # Redirige si no hay sesión activa
    usuario = Usuario.objects.get(id=usuario_id)
    cancion = Cancion.objects.get(id=cancion_id)
    #eliminar la ruta de la cancion 
    if cancion.archivo and cancion.archivo.name != 'ruta':
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, cancion.archivo.name))
        except FileNotFoundError:
            pass
    #eliminar la ruta de la portada
    if cancion.portada and cancion.portada.name != 'ruta':
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, cancion.portada.name))
        except FileNotFoundError:
            pass

    cancion.delete()

    
     
    
    return redirect('Artista_Archivos')  # Redirige a la vista de archivos del artista

def sencillo_artista(request, cancion_id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')  # Redirige si no hay sesión activa
    usuario = Usuario.objects.get(id=usuario_id)
    cancion = Cancion.objects.get(id=cancion_id)
    return render(request, 'Artista/Artista_Sencillo.html', {'usuario': usuario, 'cancion': cancion})

def album_artista(request, album_id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')  # Redirige si no hay sesión activa
    usuario = Usuario.objects.get(id=usuario_id)
    if request.method == 'POST':
        print("entro a post")
    else:
        print("entro a get")
        album = Album.objects.get(id=album_id)
        canciones = Cancion.objects.filter(id_album=album_id)
        return render(request, 'Artista/Artista_Album.html', {'usuario': usuario, 'album': album, 'canciones': canciones})