// PreviewFormData_Sencillo.js
document.addEventListener('DOMContentLoaded', () => {
  const previewBtn = document.getElementById('previewBtn');
  const form       = document.getElementById('nuevaMusicaForm');

  previewBtn.addEventListener('click', e => {
    e.preventDefault();
    console.log('🔍 PreviewFormData — preparando envío');

    const data = new FormData(form);
    for (let [key, val] of data.entries()) {
      if (val instanceof File) {
        console.log(key, val.name, `(${val.size} bytes)`);
      } else {
        console.log(key, val);
      }
    }

    // duración única
    const dur = data.get('cancion_duracion');
    if (dur) {
      console.log(`cancion_duracion: ${dur} s`);
    }
  });
});
