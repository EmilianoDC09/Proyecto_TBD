// Agregar_playlist.js

document.addEventListener('DOMContentLoaded', function() {
  // 1) Toggle del menú principal al pulsar el botón "Más opciones"
  document.querySelectorAll('.mas-options-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      const menu = this.parentNode.querySelector('.dropdown-menu');
      menu.classList.toggle('show');
    });
  });

  // 2) Toggle del sub-menú de playlists al pulsar "Agregar a playlist"
  document.querySelectorAll('.dropdown-item[data-action="playlist"]').forEach(item => {
    item.addEventListener('click', function(e) {
      e.stopPropagation();
      // abrimos/cerreamos el playlist-menu
      const wrapper = this.closest('.options-wrapper');
      const sub = wrapper.querySelector('.playlist-menu');
      sub.classList.toggle('show');
    });
  });

  // 3) Cerrar ambos menús (principal y sub-menú) al hacer click fuera
  document.addEventListener('click', function() {
    document.querySelectorAll('.dropdown-menu.show').forEach(m => {
      m.classList.remove('show');
    });
    document.querySelectorAll('.playlist-menu.show').forEach(s => {
      s.classList.remove('show');
    });
  });
    // 4) Agregar una playlist al hacer click en "Agregar a playlist"
document.querySelectorAll('.dropdown-item[data-action="playlist"]').forEach(item => {
  item.addEventListener('click', function(e) {
    e.stopPropagation();
    const wrapper = this.closest('.options-wrapper');
    
    // 1) cerramos todos los sub-menús
    document.querySelectorAll('.playlist-menu.show')
            .forEach(sm => sm.classList.remove('show'));
    
    // 2) abrimos sólo el de este wrapper
    const sub = wrapper.querySelector('.playlist-menu');
    sub.classList.toggle('show');
  });
});
// …


});
