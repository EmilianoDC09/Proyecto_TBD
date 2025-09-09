// PreviewFormData.js
document.addEventListener('DOMContentLoaded', () => {
  const previewBtn = document.getElementById('previewBtn');
  const form       = document.getElementById('nuevaMusicaForm');

  previewBtn.addEventListener('click', e => {
    e.preventDefault();
    console.log('🔍 Preview click — preparando envío');

    const data = new FormData(form);

    console.log('--- FormData entries ---');
    for (let [key, val] of data.entries()) {
      if (val instanceof File) {
        console.log(key, val.name, `(${val.size} bytes)`);
      } else {
        console.log(key, val);
      }
    }

    // ahora listamos cada duración
    const allDur = data.getAll('cancion_duracion');
    allDur.forEach((d,i) => {
      console.log(`cancion_duracion[${i}]: ${d}`);
    });
  });
});
