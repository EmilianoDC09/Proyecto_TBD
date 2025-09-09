class VolumeControl {
    /**
     * @param {string} btnSelector    Selector del botón de volumen
     * @param {string} sliderSelector Selector del slider de volumen
     * @param {object} icons           Rutas a los iconos { on: '', off: '' }
     */
    constructor(btnSelector, sliderSelector, icons) {
      this.btn    = document.querySelector(btnSelector);
      this.slider = document.querySelector(sliderSelector);
      this.icons  = icons;
      this.audio  = document.querySelector('.audio-player'); // El <audio>
      this.lastVolume = Number(this.slider.value) / 100;
  
      this._bindEvents();
      this._updateIcon(this.slider.value);
      // Inicializar volumen real
      this.audio.volume = this.lastVolume;
    }
  
    _bindEvents() {
      // Al mover el slider
      this.slider.addEventListener('input', () => {
        const vol = Number(this.slider.value) / 100;
        if (vol > 0) this.lastVolume = vol;
        this.audio.volume = vol;
        this.audio.muted = false;
        this._updateIcon(this.slider.value);
      });
  
      // Al hacer click en el botón
      this.btn.addEventListener('click', () => {
        if (!this.audio.muted && this.audio.volume > 0) {
          // silenciar
          this.audio.muted = true;
          this.slider.value = 0;
        } else {
          // restaurar último volumen
          this.audio.muted = false;
          this.audio.volume = this.lastVolume;
          this.slider.value = this.lastVolume * 100;
        }
        this._updateIcon(this.slider.value);
      });
    }
  
    _updateIcon(volume) {
      const path = (Number(volume) === 0) ? this.icons.off : this.icons.on;
      this.btn.style.backgroundImage = `url('${path}')`;
    }
  }
  
  document.addEventListener('DOMContentLoaded', () => {
    new VolumeControl('.volume-icon', '.volume-slider', {
      on:  '../assets/icons/volumen.svg',
      off: '../assets/icons/mute.svg'
    });
  });
  