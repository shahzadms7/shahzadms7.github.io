// Shahzad MS Portfolio — nav toggle + project filter
document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  var filterBtns = document.querySelectorAll('.filter-btn');
  var cards = document.querySelectorAll('.project-full');
  if (filterBtns.length) {
    filterBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        filterBtns.forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        var f = btn.getAttribute('data-filter');
        var groups = document.querySelectorAll('.project-group');
        if (f === 'all') {
          groups.forEach(function (g) { g.style.display = ''; });
          cards.forEach(function (c) { c.style.display = ''; });
        } else {
          groups.forEach(function (g) {
            g.style.display = (g.id === f) ? '' : 'none';
          });
        }
      });
    });
  }
});
