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

// Open architecture disclosures for direct links from engagement stories.
function revealArchitecture(){
 const id=location.hash.slice(1);
 if(!id.startsWith('architecture-')) return;
 const panel=document.getElementById(id);
 if(panel instanceof HTMLDetailsElement) panel.open=true;
}
window.addEventListener('hashchange',revealArchitecture);
revealArchitecture();

(() => {
 const normalize = text => text.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'');
 const search = document.getElementById('career-search');
 const groups = [...document.querySelectorAll('.career-group')];
 const records = [...document.querySelectorAll('.evidence-record')].map(el=>({el,text:normalize(el.textContent)}));
 if(search) search.addEventListener('input',()=>{
  const q=normalize(search.value).trim().split(/\s+/).filter(Boolean);let shown=0;
  for(const {el,text} of records){el.hidden=!q.every(w=>text.includes(w));if(!el.hidden)shown++;}
  for(const group of groups){group.hidden=![...group.querySelectorAll('.evidence-record')].some(el=>!el.hidden);if(q.length&&!group.hidden)group.open=true;}
  document.getElementById('career-count').textContent=`${shown} of ${records.length} source records match`;
 });
 function reveal(){
  const el=document.getElementById(location.hash.slice(1));
  if(!el)return;
  let parent=el;
  while(parent){parent.hidden=false;if(parent instanceof HTMLDetailsElement)parent.open=true;parent=parent.parentElement;}
 }
 window.addEventListener('hashchange',reveal);reveal();
 const asearch=document.getElementById('architecture-search');
 if(asearch)asearch.addEventListener('input',()=>{
  const q=normalize(asearch.value).trim().split(/\s+/).filter(Boolean);
  document.querySelectorAll('.architecture-view').forEach(el=>el.hidden=!q.every(w=>normalize(el.textContent).includes(w)));
 });
})();
