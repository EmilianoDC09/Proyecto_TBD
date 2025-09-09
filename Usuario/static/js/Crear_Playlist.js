document.addEventListener('DOMContentLoaded', () => {
    const btnNew       = document.getElementById('btn-new-playlist');
    const entryForm    = document.querySelector('.new-playlist-entry');
    const saveBtn      = document.getElementById('save-playlist');
    const nameInput    = document.getElementById('new-playlist-name');
    const listContainer= document.getElementById('playlist-list');
  
    // alternar visibilidad del formulario
    btnNew.addEventListener('click', () => {
      entryForm.classList.toggle('hidden');
      nameInput.focus();
    });
  
    // al guardar, añadimos un mini-contenedor en la parte superior
    saveBtn.addEventListener('click', () => {
      const val = nameInput.value.trim();
      if (!val) return;
  
      // crear el elemento
      const item = document.createElement('div');
      item.className = 'playlist-item';
      item.innerHTML = `
        <img src="../img/playlist-placeholder.png" alt="Imagen playlist">
        <span class="playlist-name">${val}</span>
      `;
      // insertar arriba
      listContainer.prepend(item);
  
      // limpiar form y mantenerlo abajo
      nameInput.value = '';
    });
  });
  