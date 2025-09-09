// controles.js

class AudioPlayer {
  constructor(options) {
    this.audio        = document.querySelector(options.audioSelector);
    this.playBtn      = document.querySelector(options.playBtnSelector);
    this.prevBtn      = document.querySelector(options.prevBtnSelector);
    this.nextBtn      = document.querySelector(options.nextBtnSelector);
    this.shuffleBtn   = document.querySelector(options.shuffleBtnSelector);
    this.trackNameEl  = document.querySelector('.track-name');
    this.artistNameEl = document.querySelector('.artist-name');
    this.albumArtEl   = document.querySelector('.album-art img');

    // NUEVAS referencias para progreso
    this.currentTimeEl = document.querySelector('.time.current');
    this.totalTimeEl   = document.querySelector('.time.total');
    this.progressBar   = document.querySelector('.progress');

    this.playlist     = options.playlist;
    this.currentIndex = 0;
    this.isShuffle    = false;

    this._loadTrack();
    this._bindEvents();
  }

  // Helper para formatear MM:SS
  _formatTime(sec) {
    const m = Math.floor(sec / 60).toString().padStart(2, '0');
    const s = Math.floor(sec % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  }

  _bindEvents() {
    this.playBtn.addEventListener('click', () => this.togglePlay());
    this.prevBtn.addEventListener('click', () => this.prevTrack());
    this.nextBtn.addEventListener('click', () => this.nextTrack());
    this.shuffleBtn.addEventListener('click', () => this.toggleShuffle());
    this.audio.addEventListener('ended', () => this.nextTrack());

    // Actualizar barra y tiempo cada vez que avanza el audio
    this.audio.addEventListener('timeupdate', () => {
      const cur = this.audio.currentTime;
      this.currentTimeEl.textContent = this._formatTime(cur);
      this.progressBar.value = cur;
    });

    // Al hacer seek en la barra
    this.progressBar.addEventListener('input', () => {
      this.audio.currentTime = this.progressBar.value;
    });
  }

  _loadTrack() {
    const track = this.playlist[this.currentIndex];
    this.audio.src                   = track.src;
    this.trackNameEl.textContent     = track.title;
    this.artistNameEl.textContent    = track.artist;
    this.albumArtEl.src              = track.art;

    // Cuando cargue metadatos (para saber duración)
    this.audio.addEventListener('loadedmetadata', () => {
      const dur = this.audio.duration;
      this.totalTimeEl.textContent = this._formatTime(dur);
      // Ajustamos el rango de la barra al número de segundos
      this.progressBar.min   = 0;
      this.progressBar.max   = dur;
      this.progressBar.value = 0;
    }, { once: true });

    // Actualiza estado visual de botones
    this.playBtn.classList.remove('playing');
    this.shuffleBtn.classList.toggle('shuffle-active', this.isShuffle);
  }

  togglePlay() {
    if (this.audio.paused) {
      this.audio.play();
    } else {
      this.audio.pause();
    }
    this.playBtn.classList.toggle('playing');
  }

  prevTrack() {
    if (this.isShuffle) {
      // en modo shuffle, prev no hace nada
      return;
    }
    this.currentIndex = (this.currentIndex - 1 + this.playlist.length) % this.playlist.length;
    this._loadTrack();
    this.audio.play();
    this.playBtn.classList.add('playing');
  }

  nextTrack() {
    if (this.isShuffle) {
      this.currentIndex = this._randomIndex();
    } else {
      this.currentIndex = (this.currentIndex + 1) % this.playlist.length;
    }
    this._loadTrack();
    this.audio.play();
    this.playBtn.classList.add('playing');
  }

  toggleShuffle() {
    this.isShuffle = !this.isShuffle;
    this.shuffleBtn.classList.toggle('shuffle-active', this.isShuffle);
  }

  _randomIndex() {
    let idx;
    do {
      idx = Math.floor(Math.random() * this.playlist.length);
    } while (idx === this.currentIndex && this.playlist.length > 1);
    return idx;
  }
}

