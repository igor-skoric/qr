
  let timer;
  const header = document.getElementById('main-header');

  function showHeader() {
    header.classList.remove('opacity-0', 'pointer-events-none');
  }

  function hideHeader() {
    header.classList.add('opacity-0', 'pointer-events-none');
  }

  function resetTimer() {
    showHeader();
    clearTimeout(timer);
    timer = setTimeout(hideHeader, 5000);  // 5 sekundi
  }

  // Desktop: miš i tastatura
  document.addEventListener('mousemove', resetTimer);
  document.addEventListener('keydown', resetTimer);

  // Mobilni: dodir i klik
  document.addEventListener('touchstart', resetTimer);
  document.addEventListener('click', resetTimer);

  // Pokreni prvi put
  resetTimer();
