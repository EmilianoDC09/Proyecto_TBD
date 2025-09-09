document.addEventListener('DOMContentLoaded', () => {
  const scrollDiv = document.querySelector('.artwork-scroll');
  const SCROLL_FACTOR = 0.6; // ajusta entre 0.1 (muy lento) y 1 (sin cambio)

  scrollDiv.addEventListener('wheel', e => {
    const { scrollTop, scrollHeight, clientHeight } = scrollDiv;
    const delta = e.deltaY * SCROLL_FACTOR;  // <-- aquí redujimos la velocidad

    const atTop    = scrollTop === 0 && delta < 0;
    const atBottom = scrollTop + clientHeight >= scrollHeight && delta > 0;

    if (!atTop && !atBottom) {
      scrollDiv.scrollTop += delta;
      e.preventDefault();
    }
  }, { passive: false });

  
});