document.addEventListener('DOMContentLoaded', () => {
  const playBtn     = document.querySelector('.play-album');
  const audioPlayer = document.querySelector('.audio-player');

  playBtn.addEventListener('click', () => {
    // 1) buscamos la primera fila que no sea separadora
    const row = document.querySelector('tbody tr[data-src]');
    if (!row) return;

    // 2) leemos la URL
    const src = row.dataset.src;
    if (!src) return;

    // 3) la asignamos al audio y lanzamos la reproducción
    audioPlayer.src = src;
    audioPlayer.play();
  });
});
