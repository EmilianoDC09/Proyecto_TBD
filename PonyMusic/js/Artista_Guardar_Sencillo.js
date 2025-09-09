// Artista_Guardar_Sencillo.js
document.addEventListener('DOMContentLoaded', () => {
  const saveBtn      = document.getElementById('previewBtn');
  const titleInput   = document.getElementById('nombre_cancion');
  const portadaInput = document.getElementById('portada');
  const imgPreview   = document.getElementById('preview-img');
  const titlePreview = document.getElementById('preview-title');

  saveBtn.addEventListener('click', e => {
    e.preventDefault();

    // 1) Título
    const title = titleInput.value.trim() || 'Nombre canción';
    titlePreview.textContent = title;

    // 2) Portada
    if (portadaInput.files && portadaInput.files[0]) {
      const reader = new FileReader();
      reader.onload = ev => {
        imgPreview.src = ev.target.result;
        imgPreview.style.display = 'block';
      };
      reader.readAsDataURL(portadaInput.files[0]);
    }
  });
});
