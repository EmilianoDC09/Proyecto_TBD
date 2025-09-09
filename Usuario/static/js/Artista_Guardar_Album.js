// Artista_Guardar_Sencillo.js
document.addEventListener('DOMContentLoaded', () => {
  console.log('▶ JS de preview cargado');
  const previewBtn    = document.getElementById('previewBtn');
  const albumInput    = document.getElementById('nombre_album');
  const portadaInput  = document.getElementById('portada');
  const imgPreview    = document.getElementById('preview-img');
  const titlePreview  = document.getElementById('preview-title');
  const previewList   = document.getElementById('preview-list');

  if (!previewBtn) {
    console.error('❌ No se encontró el botón #previewBtn');
    return;
  }

  previewBtn.addEventListener('click', e => {
    e.preventDefault();
    console.log('✔ Click en Guardar');

    // 1) Actualiza título
    const titulo = albumInput.value.trim() || 'Nombre álbum';
    titlePreview.textContent = titulo;

    // 2) Muestra portada
    if (portadaInput.files[0]) {
      const reader = new FileReader();
      reader.onload = ev => {
        imgPreview.src = ev.target.result;
        imgPreview.style.display = 'block';
        console.log('✔ Portada cargada');
      };
      reader.readAsDataURL(portadaInput.files[0]);
    } else {
      imgPreview.style.display = 'none';
      console.log('⚠ No hay portada seleccionada');
    }

    // 3) Lista canciones
    previewList.innerHTML = '';
    document.querySelectorAll('.song-entry').forEach((entry, i) => {
      const inp = entry.querySelector('input[name="cancion_nombre"]');
      const val = inp ? inp.value.trim() : '';
      if (val) {
        const li = document.createElement('li');
        li.textContent = val;
        previewList.appendChild(li);
        console.log(`♫ Canción ${i+1}: ${val}`);
      }
    });
  });
});
