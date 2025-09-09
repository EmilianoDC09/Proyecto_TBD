// Artista_CancionDinamica.js
document.addEventListener('DOMContentLoaded', () => {
  const addBtn    = document.getElementById('addSongBtn');
  const songsCont = document.getElementById('songsContainer');
  const wrapper   = document.querySelector('.songs-wrapper');

  function attachDurationListener(entry) {
    const fileInput     = entry.querySelector('.song-file-input');
    const durationInput = entry.querySelector('.song-duration');
    fileInput.addEventListener('change', e => {
      const file = e.target.files[0];
      if (!file) return;
      const url   = URL.createObjectURL(file);
      const audio = new Audio(url);
      audio.addEventListener('loadedmetadata', () => {
        const sec = Math.floor(audio.duration);
        const m   = String(Math.floor(sec/60)).padStart(2,'0');
        const s   = String(sec%60).padStart(2,'0');
        durationInput.value = `${m}:${s}`;
        URL.revokeObjectURL(url);
      });
    });
  }

  // inicial
  attachDurationListener(songsCont.querySelector('.song-entry'));

  addBtn.addEventListener('click', () => {
    const template = songsCont.querySelector('.song-entry');
    const clone    = template.cloneNode(true);

    // limpia valores
    clone.querySelector('input[name="cancion_nombre"]').value   = '';
    clone.querySelector('input[name="cancion_archivo"]').value   = '';
    clone.querySelector('.song-duration').value                 = '';

    attachDurationListener(clone);
    songsCont.appendChild(clone);

    // scroll al fondo
    wrapper.scrollTop = wrapper.scrollHeight;
  });
});
