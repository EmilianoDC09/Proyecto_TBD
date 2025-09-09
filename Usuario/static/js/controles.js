// Variables globales
let currentTrack = 0;
let isPlaying = false;

// Elementos del DOM
const audioPlayer = document.querySelector('.audio-player');
const playBtn = document.querySelector('.play-btn');
const bigPlayBtn = document.querySelector('.play-album');
const siguienteBtn = document.querySelector('.siguiente-btn');
const atrasBtn = document.querySelector('.atras-btn');
const trackName = document.querySelector('.track-name');
const artistName = document.querySelector('.artist-name');
const albumArt = document.querySelector('.album-art img');
const progressBar = document.querySelector('.progress');
const currentTimeEl = document.querySelector('.time.current');
const totalTimeEl = document.querySelector('.time.total');

// Asegúrate de tener esta variable disponible en el HTML
// const albumCanciones = [...]; // definida desde el template

// Actualiza la información en el reproductor
function updateFooter(cancion) {
  trackName.textContent = cancion.nombre;
  artistName.textContent = cancion.artista;
  albumArt.src = cancion.portada;
}

// Cargar y reproducir la canción actual
function playCurrentTrack() {
  const cancion = albumCanciones[currentTrack];
  audioPlayer.src = cancion.archivo;
  audioPlayer.play();
  isPlaying = true;
  updateFooter(cancion);
  updatePlayButtonIcon();
}

// Cambia el icono del botón de play/pausa
function updatePlayButtonIcon() {
  if (isPlaying) {
    playBtn.classList.add('pause');
    bigPlayBtn.classList.add('pause');
  } else {
    playBtn.classList.remove('pause');
    bigPlayBtn.classList.remove('pause');
  }
}

// Event Listeners
playBtn.addEventListener('click', () => {
  if (audioPlayer.src === '') {
    playCurrentTrack();
  } else if (audioPlayer.paused) {
    audioPlayer.play();
    isPlaying = true;
  } else {
    audioPlayer.pause();
    isPlaying = false;
  }
  updatePlayButtonIcon();
});

bigPlayBtn.addEventListener('click', () => {
  currentTrack = 0;
  playCurrentTrack();
});

siguienteBtn.addEventListener('click', () => {
  currentTrack = (currentTrack + 1) % albumCanciones.length;
  playCurrentTrack();
});

atrasBtn.addEventListener('click', () => {
  currentTrack = (currentTrack - 1 + albumCanciones.length) % albumCanciones.length;
  playCurrentTrack();
});

// Actualizar barra de progreso
audioPlayer.addEventListener('timeupdate', () => {
  const current = audioPlayer.currentTime;
  const duration = audioPlayer.duration;

  if (!isNaN(duration)) {
    const progressPercent = (current / duration) * 100;
    progressBar.value = progressPercent;

    // Actualizar tiempos
    currentTimeEl.textContent = formatTime(current);
    totalTimeEl.textContent = formatTime(duration);
  }
});

// Buscar en la barra de progreso
progressBar.addEventListener('input', () => {
  if (audioPlayer.duration) {
    const newTime = (progressBar.value / 100) * audioPlayer.duration;
    audioPlayer.currentTime = newTime;
  }
});

// Formatear tiempo en minutos:segundos
function formatTime(time) {
  const minutes = Math.floor(time / 60);
  const seconds = Math.floor(time % 60).toString().padStart(2, '0');
  return `${minutes}:${seconds}`;
}

// Cuando termina la canción, pasa a la siguiente
audioPlayer.addEventListener('ended', () => {
  currentTrack = (currentTrack + 1) % albumCanciones.length;
  playCurrentTrack();
});

