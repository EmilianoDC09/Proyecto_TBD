document.addEventListener('DOMContentLoaded', () => {
    const searchInput  = document.getElementById('searchInput');
    const genreButtons = document.querySelectorAll('.genero-btn');
    const confirmBtn   = document.getElementById('confirmarBtn');
  
    // Filtrado en tiempo real
    searchInput.addEventListener('input', () => {
      const filter = searchInput.value.trim().toLowerCase();
      genreButtons.forEach(btn => {
        const name = btn.dataset.name;
        btn.style.display = name.includes(filter) ? 'flex' : 'none';
      });
    });
  
    // Multi-selección (toggle escala de grises)
    genreButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        btn.classList.toggle('selected');
      });
    });
  
    // Redirección “Listo”
    confirmBtn.addEventListener('click', () => {
      // Pon aquí la URL que corresponda:
      window.location.href = 'pagina-siguiente.html';
    });
  });
  