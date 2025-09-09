// Duracion_AudioSencillo.js
document.addEventListener('DOMContentLoaded', () => {
  const fileInput      = document.getElementById('cancion');
  const nameSpan       = document.getElementById('cancion-name');
  const durationSpan   = document.getElementById('cancion-duracion');
  const hiddenDuration = document.getElementById('cancion_duracion');

  function formatTime(sec) {
    const m = Math.floor(sec / 60).toString().padStart(2, '0');
    const s = Math.floor(sec % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  }

  fileInput.addEventListener('change', e => {
    const file = e.target.files[0];
    if (!file) {
      nameSpan.textContent     = '';
      durationSpan.textContent = '';
      hiddenDuration.value     = '';
      return;
    }

    nameSpan.textContent = file.name;

    const audio = document.createElement('audio');
    audio.preload = 'metadata';
    audio.src     = URL.createObjectURL(file);

    audio.addEventListener('loadedmetadata', () => {
      const dur = audio.duration;
      durationSpan.textContent = formatTime(dur);
      hiddenDuration.value     = dur.toFixed(2);
      URL.revokeObjectURL(audio.src);
    });
  });
});
