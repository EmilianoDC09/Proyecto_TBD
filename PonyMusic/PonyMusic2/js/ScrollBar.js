const main = document.querySelector('.main-content');
  let hideScrollbarTimer;

  main.addEventListener('scroll', () => {
    // Siempre que estés desplazándote, asegúrate de que la clase está presente
    main.classList.add('show-scroll');

    // Cada vez que tú scroll ees, reiniciamos el temporizador
    clearTimeout(hideScrollbarTimer);
    hideScrollbarTimer = setTimeout(() => {
      // 1.5s después de que termines de hacer scroll, la quitamos
      main.classList.remove('show-scroll');
    }, 1500);
  });