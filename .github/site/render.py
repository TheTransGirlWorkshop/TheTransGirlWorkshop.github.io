from html import escape
from pathlib import Path
import json
import re
import sys


SOURCE = Path(__file__).resolve().parent
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else SOURCE.parent.parent
CONFIG = json.loads((Path(sys.argv[2]) if len(sys.argv) > 2 else SOURCE / 'catalogue.json').read_text(encoding='utf-8'))
TEMPLATES = json.loads((SOURCE / 'articles.json').read_text(encoding='utf-8'))
HOME = CONFIG['home']
ORIGIN = 'https://thetransgirlworkshop.com'
GITHUB = 'https://github.com/TheTransGirlWorkshop'
RELEASES = f'{GITHUB}/TheTransGirlWorkshop.github.io/releases'
NINTH = 'https://the-ninth-life-three.vercel.app'
DISCORD = 'https://discord.gg/jWqy4XeeCW'
LABEL = 'The Trans Girl Workshop'
CATEGORIES = {
    'games': ('Games', 'Independent games made by the Workshop. Find requirements, screenshots and where to play.'),
    'tools': ('Tools', 'Utilities for game communities, Discord servers and players.'),
    'software': ('Software', 'Desktop software and utilities from the Workshop.'),
    'servers': ('Servers', 'Explore the multiplayer communities we’re building and find their official channels.'),
    'assets': ('Assets', 'Themes and digital resources published by the Workshop.'),
    'launcher': ('Launcher', 'Install Workshop Launcher for Windows to access your Workshop games and updates.'),
    'vrc-worlds': ('VRC Worlds', 'Social spaces made for VRChat. Explore the venues and find their official community links.'),
}
PRODUCTS = CONFIG['products']
P = {item['slug']: item for item in PRODUCTS}
SITEMAP = []


def link(label, href, cls=''):
    return f'<a{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} href="{escape(href, quote=True)}">{escape(label)}</a>'


def path(item):
    return '/launcher/' if item['slug'] == 'launcher' else '/projects/' + item['slug']


def symbol(label):
    return {'Search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4 4"/>',
            'Account': '<circle cx="12" cy="8" r="3.5"/><path d="M4.5 20v-2c0-5 15-5 15 0v2"/>',
            'Store': '<path d="M4 8h16l1 12H3L4 8Z"/><path d="M9 9V6a3 3 0 0 1 6 0v3"/>'}[label]


def icon_link(label, href, extra=''):
    return f'<a href="{href}" class="utility"{extra}><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">{symbol(label)}</svg><span>{label}</span></a>'


def header(active):
    nav = ''.join(f'<a href="/{slug}/"{" aria-current=\"page\"" if active == slug else ""}>{title}</a>'
                  for slug, (title, _) in CATEGORIES.items())
    return f'''<a class="market-skip" href="#main">Skip to content</a>
<header class="market-header">
  <div class="market-wrap market-top">
    <a class="market-brand" href="/" aria-label="{LABEL} home"><img src="/assets/tgw-mark.webp" width="42" height="42" alt=""><span>The Trans Girl <strong>Workshop</strong></span></a>
    <nav class="market-utilities" aria-label="Site tools">
      {icon_link('Store', '/store/')}{icon_link('Search', '/store/#search', ' data-open-search')}{icon_link('Account', '/account/')}
      {link('Support', '/support', 'utility market-support')}
    </nav>
  </div>
  <nav class="market-wrap market-nav" aria-label="Product categories">{nav}</nav>
</header>'''


def footer(home=False):
    facebook = link('Facebook', 'https://www.facebook.com/TheTransGirlWorkshop/') if home else ''
    return f'''<footer class="market-footer"><div class="market-wrap market-footer-grid">
<div><a class="market-brand" href="/"><img src="/assets/tgw-mark.webp" width="42" height="42" alt=""><span>The Trans Girl <strong>Workshop</strong></span></a><p>Independent games, software and online communities.</p></div>
<div><h2>Workshop</h2>{link('Store', '/store/')}{link('Launcher', '/launcher/')}{link('Account and library', '/account/')}{link('News', '/news/')}</div>
<div><h2>Community</h2>{link('Discord', DISCORD)}{link('YouTube', 'https://www.youtube.com/@TheTransGirlWorkshop')}{link('GitHub', GITHUB)}{link('itch.io', 'https://the-trans-girl-workshop.itch.io/')}{link('Game Jolt', 'https://gamejolt.com/@TheTransGirlWorkshop')}{facebook}</div>
<div><h2>Help and legal</h2>{link('Customer support', '/support')}{link('Contact the Workshop', 'mailto:contact@thetransgirlworkshop.com')}{link('TrapDoor privacy', '/legal/trapdoor/privacy.html')}{link('TrapDoor terms', '/legal/trapdoor/terms.html')}</div>
</div><div class="market-wrap market-copyright">© 2026 {LABEL}</div></footer>
<dialog class="search-dialog" aria-labelledby="quick-search-title"><form action="/store/" method="get">
<div class="section-heading"><h2 id="quick-search-title">Search the Workshop</h2><button class="plain-button" type="button" data-close-search aria-label="Close search">×</button></div>
<label for="quick-search">Product or category</label><input id="quick-search" name="q" type="search" autocomplete="off">
<ul class="search-suggestions" data-suggestions></ul><button class="button primary" type="submit">Search catalogue</button></form></dialog>'''


def metadata(url, title, summary, image, kind='WebPage'):
    social = image or '/assets/studio-share.jpg'
    schema = {'@context': 'https://schema.org', '@type': kind, 'name': title, 'url': ORIGIN + url,
              'description': summary, 'publisher': {'@type': 'Organization', 'name': LABEL, 'url': ORIGIN},
              'image': ORIGIN + social}
    if kind == 'WebSite':
        schema['publisher'].update({
            'logo': ORIGIN + '/assets/tgw-mark.webp',
            'sameAs': [
                GITHUB, 'https://www.youtube.com/@TheTransGirlWorkshop', DISCORD,
                'https://the-trans-girl-workshop.itch.io/', 'https://gamejolt.com/@TheTransGirlWorkshop',
                'https://www.facebook.com/TheTransGirlWorkshop/',
            ],
        })
    schema_json = json.dumps(schema).replace('<', r'\u003c')
    return f'''<title>{escape(title)} | {LABEL}</title>
<meta name="description" content="{escape(summary, quote=True)}">
<link rel="canonical" href="{ORIGIN}{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{LABEL}">
<meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(summary, quote=True)}">
<meta property="og:url" content="{ORIGIN}{url}"><meta property="og:image" content="{ORIGIN}{social}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{schema_json}</script>'''


def write(url, title, summary, content, *, active='', filename=None, image=None, kind='WebPage', legacy=False, index=True):
    output = ROOT / (filename or (url.strip('/') + '/index.html' if url != '/' else 'index.html'))
    output.parent.mkdir(parents=True, exist_ok=True)
    robots = '' if index else '<meta name="robots" content="noindex">'
    legacy_style = '<link rel="stylesheet" href="/workshop.css">' if legacy else ''
    output.write_text(f'''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#10101a">{metadata(url, title, summary, image, kind)}{robots}
<link rel="icon" href="/assets/tgw-mark.webp" type="image/webp">{legacy_style}
<link rel="stylesheet" href="/marketplace.css"><script src="/marketplace.js" defer></script>
</head><body class="market">{header(active)}{content}{footer(url == '/') }</body></html>
''', encoding='utf-8', newline='\n')
    if index:
        SITEMAP.append(url)


def media(item, *, compact=False, priority=False, cover=False):
    art = item['cover'] if cover and 'cover' in item else item['art']
    if not art:
        return f'<div class="type-art" data-type="{item["slug"]}" aria-hidden="true"><span>{escape(item["name"])}</span></div>'
    responsive = '' 
    if art in {'ninth-life', 'statepulse', 'obscura-feature'}:
        responsive = f' srcset="/assets/{art}-compact.webp 640w, /assets/{art}.webp 1440w" sizes="{"(max-width: 680px) 100vw, 38vw" if compact else "(max-width: 760px) 100vw, 72vw"}"'
    return (f'<img src="/assets/{art}.webp"{responsive} alt="{escape(item["alt"])}" '
            f'{"fetchpriority=\"high\"" if priority else "loading=\"lazy\""} decoding="async">')


def card(item, cover=False):
    data = ' '.join([item['name'], item['summary'], item['kind'], item['status'], item['price'],
                     *(CATEGORIES[group][0] for group in item['groups'])])
    amount = item['amount'] if item['amount'] is not None else ''
    price = f'<strong class="card-price">{escape(item["price"])}</strong>' if item['price'] else ''
    return f'''<article class="market-card" data-entry data-name="{escape(item['name'], quote=True)}" data-groups="{' '.join(item['groups'])}" data-price="{amount}" data-search="{escape(data, quote=True)}">
<a href="{path(item)}" class="card-link"><div class="card-media">{media(item, compact=True, cover=cover)}</div>
<div class="card-body"><div class="card-meta"><span>{escape(item['kind'])}</span><span>{escape(item['status'])}</span></div>
<h3>{escape(item['name'])}</h3><p>{escape(item['summary'])}</p><div class="card-end">{price}<span class="card-arrow" aria-hidden="true">↗</span></div></div></a></article>'''


def section(title, items, dest='', dest_label='View all'):
    if not items:
        return ''
    cta = link(dest_label, dest, 'text-link') if dest else ''
    return f'<section class="market-section"><div class="section-heading"><h2>{title}</h2>{cta}</div><div class="market-grid">{"".join(card(P[key]) for key in items)}</div></section>'


def crumbs(label, parent='', parent_url=''):
    middle = f'<li>{link(parent, parent_url)}</li>' if parent else ''
    label = escape(label)
    return f'<nav class="market-crumbs" aria-label="Breadcrumb"><ol><li>{link("Home", "/")}</li>{middle}<li aria-current="page">{label}</li></ol></nav>'


def intro(label, headline, summary, actions=''):
    return f'<div class="page-intro"><p class="market-kicker">{label}</p><h1>{headline}</h1><p>{summary}</p>{actions}</div>'


FEATURE_LABELS = {'obscura-index': 'Explore the game', 'the-ninth-life': 'Explore the venue', 'statepulse-rp': 'View the server project'}
hero_items = [P[slug] for slug in HOME['carousel']]
slides = ''.join(f'''<article class="feature-slide" data-slide id="feature-{i}"{' hidden' if i else ''}>
<div class="feature-art">{media(product, priority=i == 0)}</div><div class="feature-copy">
<p class="market-kicker">{escape(product['kind'])}</p><h2>{escape(product['name'])}</h2><p>{escape(product['summary'])}</p>
<div class="feature-actions">{link(FEATURE_LABELS.get(product['slug'], 'Explore product'), path(product), 'button primary')}{link('Browse store', '/store/', 'button glass')}</div>
</div></article>''' for i, product in enumerate(hero_items))
slide_buttons = ''.join(f'''<button type="button" class="feature-choice" data-slide-to="{i}" aria-controls="feature-{i}" aria-pressed="{str(i == 0).lower()}">
<span class="choice-image">{media(product, compact=True)}</span><span><small>{escape(product['status'])}</small><strong>{escape(product['name'])}</strong></span></button>'''
                        for i, product in enumerate(hero_items))
home = f'''<main id="main" class="market-wrap">
<div class="discover-title brand-feature">
<div class="brand-feature-copy"><h1>{escape(HOME['heading'])}</h1>{link('Browse the catalogue', '/store/', 'text-link')}</div>
<picture class="brand-feature-art"><source media="(max-width: 670px)" srcset="/assets/tgw-banner-720.webp"><img src="/assets/tgw-banner.webp" width="1440" height="480" alt="" decoding="async"></picture>
</div>
<section class="feature" aria-label="Featured Workshop projects" data-carousel><div class="feature-stage" aria-live="off">{slides}</div>
<div class="feature-rail" hidden><div class="feature-choices">{slide_buttons}</div><div class="feature-controls"><button type="button" data-prev aria-label="Previous feature">←</button><button type="button" data-play aria-label="Pause rotation">Ⅱ</button><button type="button" data-next aria-label="Next feature">→</button></div></div>
</section>
<section class="market-section" id="projects"><div class="section-heading"><h2>Browse by category</h2></div><div class="category-shortcuts">
{''.join(link(title, f'/{slug}/') for slug, (title, _) in CATEGORIES.items())}</div></section>
{section('Featured from the Workshop', HOME['featured'], '/store/')}
<section class="launcher-spotlight"><div><p class="market-kicker">Free for Windows · Version 0.4.5</p><h2>Your Workshop library, in one place</h2><p>Sign in to buy and install available Workshop games, redeem access codes and receive updates.</p>{link('Explore Workshop Launcher', '/launcher/', 'button primary')}</div>
<img src="/assets/workshop-launcher-preview.webp" width="1080" height="720" alt="Workshop Launcher home screen" loading="lazy" decoding="async"></section>
{section('Released games and software', HOME['releases'], '/games/', 'Browse games')}
{section('In development', HOME['upcoming'], '/servers/', 'Explore servers')}
{section('VRChat showcase', HOME['worlds'], '/vrc-worlds/', 'Explore VRC Worlds')}
<section class="market-section update-strip"><div><h2>Workshop news</h2><p>Release notes for Workshop Launcher and development updates from the studio community.</p></div>{link('Read studio updates', '/news/', 'button outline')}</section>
</main>'''
write('/', 'Independent Games, Software & Digital Store', 'Explore independent games, tools, software, FiveM servers and VRChat worlds from The Trans Girl Workshop.', home, kind='WebSite')


filters = ''.join(f'<option value="{slug}">{title}</option>' for slug, (title, _) in CATEGORIES.items())
store = f'''<main id="main" class="market-wrap">
{crumbs('Store')}{intro('Workshop catalogue', escape(CONFIG['store_heading']), escape(CONFIG['store_intro']))}
<section class="market-section catalogue" aria-label="Product catalogue" data-catalogue>
<div class="catalogue-controls" hidden><label id="search">Search products<input name="q" type="search" autocomplete="off" placeholder="Search by title or keyword" data-filter-search></label>
<label>Category<select data-filter-group><option value="">All categories</option>{filters}</select></label>
<label>Sort by<select data-sort><option value="featured">Featured</option><option value="name-asc">Name A–Z</option><option value="name-desc">Name Z–A</option><option value="price-asc">Price low to high</option><option value="price-desc">Price high to low</option></select></label></div>
<p class="catalogue-status" data-results role="status"></p><div class="market-grid" data-cards>{''.join(card(item) for item in PRODUCTS)}</div>
<div class="market-panel" data-empty hidden><h2>No matching products</h2><p>Try a shorter search or choose another category.</p><button type="button" class="button outline" data-reset>Clear filters</button></div>
</section></main>'''
write('/store/', 'Store', 'Search the Workshop catalogue for independent games, Windows software, Discord tools, community servers and VRChat worlds.', store, kind='CollectionPage')


for slug, (title, description) in CATEGORIES.items():
    if slug == 'launcher':
        continue
    items = [item for item in PRODUCTS if slug in item['groups']]
    featured = items[0] if items else None
    category_hero = f'<div class="category-hero">{intro("Workshop catalogue", title, description)}<div class="category-art">{media(featured, priority=True) if featured else ""}</div></div>'
    heading = 'Published assets' if slug == 'assets' else f'Explore {title}'
    content = f'''<main id="main" class="market-wrap">{crumbs(title)}{category_hero}
<section class="market-section"><div class="section-heading"><h2>{heading}</h2>{link("Full catalogue", "/store/", "text-link")}</div>
<div class="market-grid">{"".join(card(item, cover=slug == "games") for item in items)}</div></section></main>'''
    image = f'/assets/{featured["art"]}.webp' if featured and featured['art'] else None
    write(f'/{slug}/', title, description, content, active=slug, image=image, kind='CollectionPage')


def content_note(title, body):
    if not body.strip():
        return ''
    return f'<section class="market-section market-panel prose"><h2>{escape(title)}</h2><p>{escape(body)}</p></section>'


LEGACY = {'obscura-index', 'trapdoor', 'launcher'}
for item in PRODUCTS:
    slug = item['slug']
    if slug in LEGACY:
        continue
    primary = (item['action'], item['url'])
    extra = [('Events', NINTH + '/events'), ('Member sign-in', NINTH + '/login')] if slug == 'the-ninth-life' else []
    body = content_note(item['detail_title'], item['detail'])
    cat = item['groups'][0]
    image = f'/assets/{item["art"]}.webp' if item['art'] else None
    actions = link(*primary, 'button primary') + ''.join(link(*action, 'button outline') for action in extra)
    content = f'''<main id="main" class="market-wrap">{crumbs(item['name'], CATEGORIES[cat][0], f'/{cat}/')}
<div class="category-hero">{intro(escape(item['kind']), escape(item['name']), escape(item['summary']), f'<div class="product-flags">{escape(item["status"])}{" · " + escape(item["price"]) if item["price"] else ""}</div><div class="product-actions">{actions}</div>')}
<div class="category-art">{media(item, priority=True)}</div></div>
{body}</main>'''
    write(path(item), item['name'], item['summary'], content, active=cat, image=image, filename=f'projects/{slug}.html')


def preserve_article(filename, url, title, summary, active='', image=None, addition='', replacements=()):
    content = TEMPLATES[filename]
    for old, new in replacements:
        assert old in content, old
        content = content.replace(old, new)
    if addition:
        content = content.replace('</main>', addition + '</main>')
    write(url, title, summary, content, active=active, filename=filename, image=image, legacy=True)


for slug, filename, active in [
    ('obscura-index', 'projects/obscura-index.html', 'games'),
    ('trapdoor', 'projects/trapdoor.html', 'tools'),
    ('launcher', 'launcher/index.html', 'launcher'),
]:
    product = P[slug]
    replacements = [(f'{{{{{key}}}}}', escape(product[key])) for key in ('name', 'summary', 'status', 'price')
                    if f'{{{{{key}}}}}' in TEMPLATES[filename]]
    image = '/assets/' + product['art'] + '.webp' if product['art'] else None
    titles = {'launcher': 'Workshop Launcher for Windows', 'trapdoor': 'TrapDoor Discord Bot'}
    addition = content_note(product['detail_title'], product['detail'])
    if slug == 'launcher':
        addition += section('Available in Workshop Launcher', [item['slug'] for item in PRODUCTS if 'launcher' in item])
    preserve_article(filename, path(product), titles.get(slug, product['name']), product['summary'], active=active, image=image,
                     addition=addition, replacements=replacements)

preserve_article('support.html', '/support', 'Customer Support',
                 'Get TGW help with launcher installation, accounts, purchases, refunds, TrapDoor and community access.',
                 addition=content_note('Service update', CONFIG['support_update']))


write('/account/', 'Account & Library', 'Open the appropriate Workshop or Ninth Life account and get help with downloads, purchases and password recovery.',
      f'''<main id="main" class="market-wrap">{crumbs('Account')}{intro('Customer access', 'Account & Library', 'Choose where you signed up or made your purchase.')}
<div class="market-account market-section"><section class="market-panel prose"><h2>Workshop games</h2><p>Open Workshop Launcher and sign in to access your Workshop account, redeem an invitation or install a game from Library.</p>
{link('Get Workshop Launcher', '/launcher/', 'button primary')}<p>For a copy of purchase details or access help, {link('contact customer support', '/support')}.</p></section>
<section class="market-panel prose"><h2>The Ninth Life</h2><p>Sign in with Discord on the venue website for its member account and entitlements.</p>{link('Sign in to The Ninth Life', NINTH + '/login', 'button outline')}</section></div></main>''')
write('/news/', 'Workshop News', 'Find Workshop Launcher release notes, studio updates and project news from The Trans Girl Workshop.',
      f'''<main id="main" class="market-wrap">{crumbs('News')}{intro('Studio updates', 'Workshop news', escape(CONFIG['news_intro']))}
<div class="market-account market-section"><article class="market-panel prose"><h2>Workshop Launcher 0.4.5</h2><p>Read the release notes for the current Windows installer or browse previous versions.</p>{link('Read release notes', RELEASES + '/tag/launcher-v0.4.5', 'button primary')}</article>
<article class="market-panel prose"><h2>Development and community updates</h2><p>Find project announcements in the Workshop Discord and venue events on The Ninth Life website.</p>{link('Workshop Discord', DISCORD, 'button outline')} {link('Venue events', NINTH + '/events', 'button outline')}</article></div>{content_note("Studio update", CONFIG["news_update"])}</main>''')
write('/404', 'Page Not Found', 'Return to the Workshop catalogue or contact customer support.',
      f'''<main id="main" class="market-wrap">{intro('404', 'Page not found', 'This page may have moved. Browse the catalogue to find your product.')}{link('Browse the store', '/store/', 'button primary')}</main>''',
      filename='404.html', index=False)


sitemap = sorted(set(SITEMAP + ['/legal/trapdoor/privacy.html', '/legal/trapdoor/terms.html']))
(ROOT / 'sitemap.xml').write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'  <url><loc>{ORIGIN}{url}</loc></url>\n' for url in sitemap) + '</urlset>\n', encoding='utf-8')
(ROOT / 'marketplace-index.json').write_text(json.dumps([
    {'name': item['name'], 'url': path(item), 'keywords': ' '.join([item['kind'], item['summary'],
        *(CATEGORIES[group][0] for group in item['groups'])])}
    for item in PRODUCTS
], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

feed = [
    {**item['launcher'], 'Name': item['name'], 'Description': item['summary'],
     'Price': item['price'], 'Status': item['status']}
    for item in PRODUCTS if 'launcher' in item
]
(ROOT / 'launcher/catalog.json').write_text(
    json.dumps(feed, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n',
)
