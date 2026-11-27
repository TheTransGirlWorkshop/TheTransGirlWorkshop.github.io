const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
const matchesQuery = (text, query) => {
  const content = text.toLowerCase();
  return query.toLowerCase().trim().split(/\s+/).every(term => content.includes(term));
};

const carousel = document.querySelector('[data-carousel]');
if (carousel) {
  const slides = [...carousel.querySelectorAll('[data-slide]')];
  const choices = [...carousel.querySelectorAll('[data-slide-to]')];
  const rail = carousel.querySelector('.feature-rail');
  const play = rail.querySelector('[data-play]');
  const stage = carousel.querySelector('.feature-stage');
  let current = 0;
  let timer;
  let playing = !reduceMotion.matches;
  let hovered = false;

  function advance(index, announce = false) {
    current = (index + slides.length) % slides.length;
    stage.setAttribute('aria-live', announce ? 'polite' : 'off');
    slides.forEach((slide, i) => {
      slide.hidden = i !== current;
      choices[i].setAttribute('aria-pressed', String(i === current));
    });
  }
  function updateClock() {
    clearInterval(timer);
    play.textContent = playing ? 'Ⅱ' : '▷';
    play.setAttribute('aria-label', playing ? 'Pause rotation' : 'Start rotation');
    const focused = carousel.contains(document.activeElement);
    if (playing && !hovered && !focused && !document.hidden) {
      timer = setInterval(() => advance(current + 1), 8500);
    }
  }
  function choose(index) {
    playing = false;
    updateClock();
    advance(index, true);
  }
  rail.hidden = false;
  choices.forEach((button, i) => button.addEventListener('click', () => choose(i)));
  rail.querySelector('[data-prev]').addEventListener('click', () => choose(current - 1));
  rail.querySelector('[data-next]').addEventListener('click', () => choose(current + 1));
  play.addEventListener('click', () => {
    playing = !playing;
    updateClock();
  });
  carousel.addEventListener('mouseenter', () => { hovered = true; updateClock(); });
  carousel.addEventListener('mouseleave', () => { hovered = false; updateClock(); });
  carousel.addEventListener('focusin', updateClock);
  carousel.addEventListener('focusout', () => setTimeout(updateClock, 0));
  document.addEventListener('visibilitychange', updateClock);
  reduceMotion.addEventListener('change', event => {
    if (event.matches) playing = false;
    updateClock();
  });
  updateClock();
}

const catalogue = document.querySelector('[data-catalogue]');
if (catalogue) {
  const search = catalogue.querySelector('[data-filter-search]');
  const group = catalogue.querySelector('[data-filter-group]');
  const sort = catalogue.querySelector('[data-sort]');
  const cardGrid = catalogue.querySelector('[data-cards]');
  const cards = [...cardGrid.children];
  const status = catalogue.querySelector('[data-results]');
  const empty = catalogue.querySelector('[data-empty]');
  const sorters = {
    'name-asc': (a, b) => a.dataset.name.localeCompare(b.dataset.name),
    'name-desc': (a, b) => b.dataset.name.localeCompare(a.dataset.name),
    'price-asc': (a, b) => comparePrices(a, b, 1),
    'price-desc': (a, b) => comparePrices(a, b, -1),
  };

  function comparePrices(a, b, direction) {
    if (a.dataset.price === '') return b.dataset.price === '' ? 0 : 1;
    if (b.dataset.price === '') return -1;
    return (Number(a.dataset.price) - Number(b.dataset.price)) * direction;
  }
  function filter() {
    let count = 0;
    for (const card of cards) {
      const correctGroup = !group.value || card.dataset.groups.split(' ').includes(group.value);
      card.hidden = !correctGroup || !matchesQuery(card.dataset.search, search.value);
      if (!card.hidden) count++;
    }
    status.textContent = count === 1 ? '1 product' : count + ' products';
    empty.hidden = count > 0;
  }
  function reorder() {
    const order = [...cards];
    if (sorters[sort.value]) order.sort(sorters[sort.value]);
    cardGrid.append(...order);
  }
  const params = new URLSearchParams(location.search);
  search.value = params.get('q') || '';
  const category = params.get('category');
  if ([...group.options].some(option => option.value === category)) group.value = category;
  catalogue.querySelector('.catalogue-controls').hidden = false;
  search.addEventListener('input', filter);
  group.addEventListener('change', filter);
  sort.addEventListener('change', reorder);
  catalogue.querySelector('[data-reset]').addEventListener('click', () => {
    search.value = '';
    group.value = '';
    sort.value = 'featured';
    filter();
    reorder();
    search.focus();
  });
  filter();
}

const dialog = document.querySelector('.search-dialog');
if (dialog && dialog.showModal) {
  const query = dialog.querySelector('input');
  const suggestions = dialog.querySelector('[data-suggestions]');
  let entries = [];
  let request;

  function suggest() {
    const results = query.value.trim()
      ? entries.filter(item => matchesQuery(item.name + ' ' + item.keywords, query.value))
      : [];
    suggestions.replaceChildren(...results.slice(0, 5).map(item => {
      const row = document.createElement('li');
      const anchor = document.createElement('a');
      anchor.href = item.url;
      anchor.textContent = item.name;
      row.append(anchor);
      return row;
    }));
  }
  document.querySelector('[data-open-search]').addEventListener('click', event => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    dialog.showModal();
    query.focus();
    request ||= fetch('/marketplace-index.json')
      .then(response => {
        if (!response.ok) throw new Error('Search index unavailable');
        return response.json();
      })
      .then(index => { entries = index; suggest(); })
      .catch(() => { request = undefined; });
  });
  dialog.querySelector('[data-close-search]').addEventListener('click', () => dialog.close());
  query.addEventListener('input', suggest);
}

if ('IntersectionObserver' in window && !reduceMotion.matches) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      observer.unobserve(entry.target);
      if (entry.boundingClientRect.top > 180 && !reduceMotion.matches) {
        entry.target.animate([{ opacity: 0.75, transform: 'translateY(12px)' },
          { opacity: 1, transform: 'translateY(0)' }], { duration: 320, easing: 'ease-out' });
      }
    }
  }, { threshold: 0.12 });
  document.querySelectorAll('.market-section, .launcher-spotlight').forEach(section => observer.observe(section));
}
