// Carousel.js
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.carousel-wrapper').forEach(wrapper => {
      const carousel = wrapper.querySelector('.carousel');
      const btnLeft  = wrapper.querySelector('.arrow.left');
      const btnRight = wrapper.querySelector('.arrow.right');
      if (!carousel || !btnLeft || !btnRight) return;
  
      // Calcula padding horizontal del wrapper
      const style    = getComputedStyle(wrapper);
      const padLeft  = parseFloat(style.paddingLeft)  ||  0;
      const padRight = parseFloat(style.paddingRight) ||  0;
  
      // Ancho visible real para desplazar (p. ej. 8 tarjetas)
      const visibleWidth = wrapper.clientWidth - padLeft - padRight;
  
      btnLeft.addEventListener('click', () => {
        carousel.scrollBy({ left: -visibleWidth, behavior: 'smooth' });
      });
      btnRight.addEventListener('click', () => {
        carousel.scrollBy({ left:  visibleWidth, behavior: 'smooth' });
      });
    });
  });
  