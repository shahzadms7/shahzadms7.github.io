(() => {
  const menu = document.querySelector('.menu-button');
  const nav = document.querySelector('.nav-links');
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('open', open);
  });
  nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    menu.setAttribute('aria-expanded', 'false'); nav.classList.remove('open');
  }));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && nav.classList.contains('open')) {
      nav.classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); menu.focus();
    }
  });
  const input = document.querySelector('#project-search');
  const cards = [...document.querySelectorAll('.project')];
  const filters = [...document.querySelectorAll('.filter[data-filter]')];
  let category = 'all';
  const normalize = value => value.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
  const index = cards.map(card => ({card, text: normalize(card.textContent)}));
  function filter() {
    const words = normalize(input.value).trim().split(/\s+/).filter(Boolean);
    let count = 0, technologyCount = 0;
    index.forEach(({card, text}) => {
      const show = (category === 'all' || card.dataset.category === category) && words.every(word => text.includes(word));
      card.hidden = !show;
      if(show) { if(card.classList.contains('technology')) technologyCount++; else count++; }
    });
    document.querySelector('#result-count').textContent = `${count} project families · ${technologyCount} technology domains`;
    document.querySelector('#no-results').hidden = count + technologyCount > 0;
  }
  input.addEventListener('input', filter);
  filters.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.filter;
    filters.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    filter();
  }));
  document.querySelector('#reset-search').addEventListener('click', () => {
    input.value = ''; category = 'all';
    filters.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.filter === 'all')));
    filter(); input.focus();
  });
  const expand = document.querySelector('#expand-projects');
  expand.addEventListener('click', () => {
    const visible = cards.filter(c => !c.hidden);
    const open = visible.some(c => !c.open);
    visible.forEach(c => c.open = open);
    expand.textContent = open ? 'Collapse visible details' : 'Expand visible details';
  });
  document.querySelector('#print-profile').addEventListener('click', () => window.print());
  filter();
})();
