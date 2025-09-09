// Duracion_Audio.js
document.addEventListener('DOMContentLoaded', () => {
  // formatea segundos a MM:SS
  function formatTime(sec) {
    const m = Math.floor(sec/60).toString().padStart(2,'0');
    const s = Math.floor(sec%60).toString().padStart(2,'0');
    return `${m}:${s}`;
  }

  // cada vez que cambie un input de audio
  document.body.addEventListener('change', e => {
    if (!e.target.classList.contains('song-file-input')) return;
    const fileInput     = e.target;
    const durationInput = fileInput.closest('.song-entry').querySelector('.song-duration');
    const file = fileInput.files[0];
    if (!file) {
      durationInput.value = '';
      return;
    }

    const url   = URL.createObjectURL(file);
    const audio = new Audio(url);
    audio.preload = 'metadata';
    audio.src     = url;

    audio.addEventListener('loadedmetadata', () => {
      durationInput.value = formatTime(audio.duration);
      URL.revokeObjectURL(url);
    });
  });
});
