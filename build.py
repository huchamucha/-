#!/usr/bin/env python3
"""Build the КА-Строй standalone site.

Reads page bodies (page_*.html) from the project root, wraps each one with the
shared head/header/footer, copies static assets, and writes the result to
``dist/``. The output directory is a self-contained static site that can be
uploaded to any hosting (FTP, Reg.ru, GitHub Pages, S3, etc.).

Usage:
    python3 build.py
"""
import datetime
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, 'dist')

# ── Site URL ────────────────────────────────────────────────────────────────
# Used for sitemap.xml and robots.txt.  Change to the production domain once
# the site is deployed (e.g. 'https://ka-stroy54.ru').
SITE_URL = 'https://ka-stroy54.ru'

# ── OG image (shared across all pages) ──────────────────────────────────────
OG_IMAGE = SITE_URL.rstrip('/') + '/img/og-cover.jpg'

HEAD = '''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="ru" href="{canonical}">
<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="КА-Строй">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="''' + OG_IMAGE + '''">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="''' + OG_IMAGE + '''">
<!-- Security -->
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN">
<meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=(), payment=()">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https://api.web3forms.com; frame-src https://yandex.ru https://api-maps.yandex.ru; object-src 'none'; base-uri 'self'; form-action 'self' https://api.web3forms.com;">
<meta name="referrer" content="strict-origin-when-cross-origin">
<!-- Favicons -->
<link rel="icon" href="img/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="img/favicon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="img/apple-touch-icon.png">
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#1a1c20">
<!-- Preconnect -->
<link rel="dns-prefetch" href="https://api.web3forms.com">
<link rel="preconnect" href="https://api.web3forms.com" crossorigin>
<link rel="dns-prefetch" href="https://yandex.ru">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
'''

HEADER = '''<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="index.html">
      <img class="brand__logo" src="img/logo.png" alt="КА-Строй" width="330" height="202">
      <span class="brand__name">КА<b>-</b>СТРОЙ</span>
    </a>
    <button class="nav-toggle" aria-label="Меню"><span></span></button>
    <nav class="nav" aria-label="Главное меню">
      <a href="index.html">Главная</a>
      <a href="about.html">О компании</a>
      <a href="asfalt_nsk.html">Прайс-лист</a>
      <a href="arenda_techniki_nsk.html">Аренда техники</a>
      <a href="calculator.html">Калькулятор</a>
      <a href="gallery.html">Галерея работ</a>
      <a href="news.html">Новости</a>
      <a href="contacts.html">Контакты</a>
    </nav>
    <div class="header-call">
      <a class="header-call__phone" href="tel:+73833110202" aria-label="Позвонить в КА-Строй">
        <span class="header-call__icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.02-.24c1.12.37 2.32.57 3.57.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.24 1.02l-2.21 2.2z"/></svg>
        </span>
        <span class="header-call__text">
          <strong>+7 (383) 311-02-02</strong>
          <small>Ежедневно с 9:00 до 18:00</small>
        </span>
      </a>
      <button type="button" class="header-call__btn" data-callback-open>Заказать звонок</button>
    </div>
  </div>
</header>
'''

FOOTER = '''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col">
        <div class="footer-brand"><img class="brand__logo" src="img/logo.png" alt="КА-Строй" width="330" height="202"><span class="brand__name">КА<b>-</b>СТРОЙ</span></div>
        <p>ООО ИСК «КА-Строй» — производство асфальта, строительство и ремонт дорог, благоустройство и аренда спецтехники в Новосибирске и Новосибирской области.</p>
        <p style="margin-top:10px"><b style="color:#fff">Член АСОНО</b> · СРО-С-284-21062017 · реестр №2360</p>
      </div>
      <div class="footer-col">
        <h4>Меню</h4>
        <ul>
          <li><a href="index.html">Главная</a></li>
          <li><a href="about.html">О компании</a></li>
          <li><a href="asfalt_nsk.html">Материалы и асфальт</a></li>
          <li><a href="arenda_techniki_nsk.html">Аренда техники</a></li>
          <li><a href="calculator.html">Калькулятор</a></li>
          <li><a href="gallery.html">Наши работы</a></li>
          <li><a href="news.html">Новости</a></li>
          <li><a href="contacts.html">Контакты</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Телефоны</h4>
        <p>Офис<br><a href="tel:+73833110202" style="color:#fff;font-weight:700">+7 (383) 311-02-02</a></p>
        <p style="margin-top:10px">Аренда спецтехники<br><a href="tel:+79039356049">+7 903 935 60 49</a><br><a href="tel:+79137224955">+7 913 722-49-55</a></p>
        <p style="margin-top:10px">Материалы<br><a href="tel:+79231504297">+7 923 150 42 97</a></p>
        <p style="margin-top:10px">Производство работ<br><a href="tel:+79139174541">+7 913 917 45 41</a></p>
      </div>
      <div class="footer-col">
        <h4>Адрес и почта</h4>
        <p>г. Новосибирск,<br>ул. 1-ая Грузинская, 32/1<br>630040</p>
        <p style="margin-top:10px"><a href="mailto:ka-stroy54@bk.ru" style="color:#fff;font-weight:700">ka-stroy54@bk.ru</a></p>
        <p style="margin-top:10px">Пн–Пт: 9:00–18:00<br>Сб–Вс: по договорённости</p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2020–{year} ООО ИСК «КА-Строй». Все права защищены.</span>
      <span>Сайт носит информационный характер и не является публичной офертой (ст. 437 ГК РФ).</span>
      <span><a href="privacy.html" style="color:var(--text-3);text-decoration:underline">Политика конфиденциальности</a></span>
    </div>
  </div>
</footer>
<div class="callback-modal" data-callback-modal hidden>
  <div class="callback-modal__overlay" data-callback-close></div>
  <div class="callback-modal__card" role="dialog" aria-modal="true" aria-labelledby="callback-title">
    <button class="callback-modal__close" type="button" data-callback-close aria-label="Закрыть">×</button>
    <h3 id="callback-title">Заказать звонок</h3>
    <p class="callback-modal__desc">Перезвоним в течение 15 минут в рабочее время (ежедневно 9:00–18:00).</p>
    <form action="https://api.web3forms.com/submit" method="POST" data-callback-form>
      <input type="hidden" name="access_key" value="cd4f2ebd-5553-4446-9f51-a14d2d561a80">
      <input type="hidden" name="subject" value="КА-Строй — заказ обратного звонка">
      <input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" style="display:none">
      <label class="callback-modal__field">
        <span>Ваше имя</span>
        <input type="text" name="Имя" required placeholder="Как к вам обращаться" autocomplete="name">
      </label>
      <label class="callback-modal__field">
        <span>Телефон</span>
        <input type="tel" name="Телефон" required placeholder="+7 (___) ___-__-__" autocomplete="tel" inputmode="tel">
      </label>
      <button type="submit" class="callback-modal__submit">Заказать звонок</button>
      <div class="callback-modal__status" role="status"></div>
      <p class="callback-modal__hint">Нажимая «Заказать звонок», вы соглашаетесь на обработку персональных данных в соответствии с <a href="privacy.html" style="color:var(--text-2);text-decoration:underline">политикой конфиденциальности</a>.</p>
    </form>
  </div>
</div>
<script src="js/main.js" defer></script>
{jsonld}
</body>
</html>
'''

PAGES = {
    'index.html': {
        'title': 'КА-Строй — дорожное строительство в Новосибирске | асфальт, ремонт дорог, аренда техники',
        'description': 'КА-Строй — производство асфальта, строительство и ремонт дорог, благоустройство, аренда спецтехники в Новосибирске. Собственный АБЗ, член АСОНО, работа по 44-ФЗ и 223-ФЗ.',
        'body': 'page_index.html',
    },
    'about.html': {
        'title': 'О компании — ООО ИСК «КА-Строй» в Новосибирске',
        'description': 'ООО ИСК «КА-Строй» с 2020 года: член АСОНО (СРО-С-284-21062017), собственный АБЗ, парк техники, более 14 контрактов по 44-ФЗ за год.',
        'body': 'page_about.html',
    },
    'asfalt_nsk.html': {
        'title': 'Асфальт и материалы для дорожного строительства — КА-Строй Новосибирск',
        'description': 'Производство и продажа асфальтобетонной смеси Б-II от 5000 ₽/т, ЩПС, песка, щебня. Асфальтирование дорог под ключ от 500 ₽/м². Доставка по Новосибирску и НСО.',
        'body': 'page_asfalt.html',
    },
    'service-construction.html': {
        'title': 'Строительство дорог в Новосибирске — КА-Строй',
        'description': 'Строительство автомобильных дорог под ключ: геодезия, земляное полотно, основание, асфальтобетонное покрытие. Свой АБЗ, парк техники, лаборатория. Работа по 44-ФЗ.',
        'body': 'page_service_construction.html',
    },
    'service-repair.html': {
        'title': 'Ремонт дорог в Новосибирске — ямочный, картами, фрезерование — КА-Строй',
        'description': 'Ремонт дорог в Новосибирске и НСО: ямочный ремонт, ремонт картами, фрезерование, восстановление верхнего слоя. Свой асфальт, выезд на следующий день. От 850 ₽/м².',
        'body': 'page_service_repair.html',
    },
    'service-landscaping.html': {
        'title': 'Благоустройство территорий — дворы, парковки, тротуары — КА-Строй',
        'description': 'Благоустройство дворов, парковок, тротуаров и площадок в Новосибирске. Демонтаж, водоотвод, бортовой камень, асфальт или плитка, разметка, МАФ. От 1 200 ₽/м².',
        'body': 'page_service_landscaping.html',
    },
    'arenda_techniki_nsk.html': {
        'title': 'Аренда спецтехники в Новосибирске — КА-Строй',
        'description': 'Аренда экскаваторов, катков, асфальтоукладчиков, погрузчиков, грейдеров в Новосибирске. Промокод «САЙТ КА-СТРОЙ» — скидка −10%.',
        'body': 'page_arenda.html',
    },
    'calculator.html': {
        'title': 'Калькулятор стоимости работ и материалов — КА-Строй',
        'description': 'Онлайн-калькулятор стоимости асфальтирования, материалов (асфальт Б-II, ЩПС, песок) и аренды спецтехники.',
        'body': 'page_calculator.html',
    },
    'gallery.html': {
        'title': 'Галерея наших работ — КА-Строй Новосибирск',
        'description': 'Реальные объекты КА-Строй: асфальтирование, ремонт автодорог, благоустройство в Новосибирске и Новосибирской области (ТУАД, МКУ «Дзержинка» и др.).',
        'body': 'page_gallery.html',
    },
    'news.html': {
        'title': 'Новости компании КА-Строй',
        'description': 'Новости и пресс-релизы компании КА-Строй: участие в нацпроектах, новые контракты, развитие производства.',
        'body': 'page_news.html',
    },
    'contacts.html': {
        'title': 'Контакты КА-Строй в Новосибирске — телефон, адрес офиса',
        'description': 'Контакты КА-Строй: офис +7 (383) 311-02-02, аренда техники, материалы, производство работ. Адрес: г. Новосибирск, ул. 1-ая Грузинская, 32/1.',
        'body': 'page_contacts.html',
    },
}

# ── Sitemap metadata ───────────────────────────────────────────────────────
# priority: 0.0–1.0 (importance relative to other pages on the site)
# changefreq: how often the page content is expected to change
SITEMAP_META = {
    'index.html':                   {'priority': '1.0', 'changefreq': 'weekly'},
    'about.html':                   {'priority': '0.8', 'changefreq': 'monthly'},
    'asfalt_nsk.html':              {'priority': '0.9', 'changefreq': 'weekly'},
    'service-construction.html':    {'priority': '0.8', 'changefreq': 'monthly'},
    'service-repair.html':          {'priority': '0.8', 'changefreq': 'monthly'},
    'service-landscaping.html':     {'priority': '0.8', 'changefreq': 'monthly'},
    'arenda_techniki_nsk.html':     {'priority': '0.9', 'changefreq': 'weekly'},
    'calculator.html':              {'priority': '0.7', 'changefreq': 'monthly'},
    'gallery.html':                 {'priority': '0.6', 'changefreq': 'monthly'},
    'news.html':                    {'priority': '0.7', 'changefreq': 'weekly'},
    'contacts.html':                {'priority': '0.8', 'changefreq': 'yearly'},
}


# ── Breadcrumb mapping for JSON-LD ─────────────────────────────────────────
BREADCRUMBS = {
    'index.html': [('Главная', 'index.html')],
    'about.html': [('Главная', 'index.html'), ('О компании', 'about.html')],
    'asfalt_nsk.html': [('Главная', 'index.html'), ('Прайс-лист', 'asfalt_nsk.html')],
    'service-construction.html': [('Главная', 'index.html'), ('Услуги', 'asfalt_nsk.html'), ('Строительство дорог', 'service-construction.html')],
    'service-repair.html': [('Главная', 'index.html'), ('Услуги', 'asfalt_nsk.html'), ('Ремонт дорог', 'service-repair.html')],
    'service-landscaping.html': [('Главная', 'index.html'), ('Услуги', 'asfalt_nsk.html'), ('Благоустройство', 'service-landscaping.html')],
    'arenda_techniki_nsk.html': [('Главная', 'index.html'), ('Аренда техники', 'arenda_techniki_nsk.html')],
    'calculator.html': [('Главная', 'index.html'), ('Калькулятор', 'calculator.html')],
    'gallery.html': [('Главная', 'index.html'), ('Галерея работ', 'gallery.html')],
    'news.html': [('Главная', 'index.html'), ('Новости', 'news.html')],
    'contacts.html': [('Главная', 'index.html'), ('Контакты', 'contacts.html')],
}


def build_jsonld(page: str) -> str:
    """Return a <script type="application/ld+json"> block with Schema.org data."""
    base = SITE_URL.rstrip('/')

    org = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": base + "/#organization",
        "name": "ООО ИСК «КА-Строй»",
        "alternateName": "КА-Строй",
        "url": base,
        "logo": base + "/img/logo.png",
        "image": base + "/img/og-cover.jpg",
        "description": "Производство асфальта, строительство и ремонт дорог, "
                       "благоустройство, аренда спецтехники в Новосибирске.",
        "telephone": "+7 (383) 311-02-02",
        "email": "ka-stroy54@bk.ru",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "ул. 1-ая Грузинская, 32/1",
            "addressLocality": "Новосибирск",
            "addressRegion": "Новосибирская область",
            "postalCode": "630040",
            "addressCountry": "RU",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 55.1197,
            "longitude": 82.9255,
        },
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday",
                              "Thursday", "Friday"],
                "opens": "09:00",
                "closes": "18:00",
            },
        ],
        "sameAs": [
            "https://yandex.ru/maps/org/ka_stroy/94561180941/",
            "https://2gis.ru/novosibirsk/firm/70000001063534704",
        ],
        "priceRange": "₽₽",
        "areaServed": {
            "@type": "GeoCircle",
            "geoMidpoint": {
                "@type": "GeoCoordinates",
                "latitude": 55.0084,
                "longitude": 82.9357,
            },
            "geoRadius": "150000",
        },
    }

    # BreadcrumbList
    crumbs = BREADCRUMBS.get(page, [('Главная', 'index.html')])
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": base + '/' + url,
            }
            for i, (name, url) in enumerate(crumbs)
        ],
    }

    # Service schema for service pages
    SERVICES = {
        'service-construction.html': {
            "name": "Строительство дорог под ключ",
            "description": "Полный цикл строительства автомобильных дорог: "
                           "земляное полотно, основание из ЩПС и щебня, "
                           "укладка асфальтобетонного покрытия в 1–2 слоя, "
                           "геодезия, лабораторный контроль и сдача объекта по акту.",
            "serviceType": "Строительство дорог",
            "url": base + "/service-construction.html",
        },
        'service-repair.html': {
            "name": "Ремонт дорог и дорожных покрытий",
            "description": "Ремонт автомобильных дорог: ямочный ремонт, "
                           "ремонт картами, фрезерование старого покрытия, "
                           "устройство выравнивающего и верхнего слоя асфальтобетона, "
                           "заливка швов и трещин.",
            "serviceType": "Ремонт дорог",
            "url": base + "/service-repair.html",
        },
        'service-landscaping.html': {
            "name": "Благоустройство территорий",
            "description": "Благоустройство дворов, парковок, тротуаров и площадок: "
                           "устройство бортового камня, асфальтобетонного покрытия, "
                           "организация поверхностного водоотвода, озеленение.",
            "serviceType": "Благоустройство",
            "url": base + "/service-landscaping.html",
        },
    }

    if page == 'index.html':
        website = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "КА-Строй",
            "url": base,
            "inLanguage": "ru",
        }
        data = [org, website, breadcrumb]
    elif page in SERVICES:
        svc_info = SERVICES[page]
        service = {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": svc_info["name"],
            "description": svc_info["description"],
            "serviceType": svc_info["serviceType"],
            "url": svc_info["url"],
            "provider": {
                "@type": "LocalBusiness",
                "@id": base + "/#organization",
            },
            "areaServed": {
                "@type": "AdministrativeArea",
                "name": "Новосибирская область",
            },
            "availableChannel": {
                "@type": "ServiceChannel",
                "serviceUrl": base + "/contacts.html",
                "servicePhone": "+7 (383) 311-02-02",
            },
        }
        data = [org, breadcrumb, service]
    else:
        data = [org, breadcrumb]

    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    return f'<script type="application/ld+json">{blob}</script>'


def minify_css(css: str) -> str:
    """CSS minification: remove comments, collapse whitespace, trim around tokens."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    css = re.sub(r'\n+', '\n', css)
    lines = []
    for line in css.split('\n'):
        stripped = line.strip()
        if stripped:
            lines.append(stripped)
    css = ' '.join(lines)
    css = re.sub(r'\s*([{}:;,>~+!])\s*', r'\1', css)
    css = re.sub(r';\s*}', '}', css)
    css = re.sub(r'\s*\(\s*', '(', css)
    css = re.sub(r'\s*\)\s*', ')', css)
    css = re.sub(r'\s+', ' ', css)
    return css.strip()


def minify_js(js: str) -> str:
    """Basic JS minification: remove single-line comments, collapse whitespace.

    Preserves string literals and regex patterns as much as possible.
    """
    lines = js.split('\n')
    out = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('//'):
            continue
        out.append(stripped)
    result = ' '.join(out)
    result = re.sub(r' {2,}', ' ', result)
    return result.strip()


def mark_active(html: str, current_page: str) -> str:
    """Add ``is-active`` to the header nav link pointing at ``current_page``.

    Avoids relying on JavaScript for the active highlight so the correct item
    is highlighted even with JS disabled and during the first paint. The change
    is confined to the ``<nav class="nav">…</nav>`` block, so the brand link
    and footer menu are intentionally left alone.
    """
    nav_match = re.search(r'<nav class="nav"[^>]*>.*?</nav>', html, flags=re.DOTALL)
    if not nav_match:
        return html

    nav_block = nav_match.group(0)
    pattern = re.compile(
        r'<a\b(?P<attrs>[^>]*?\bhref="' + re.escape(current_page) + r'"[^>]*)>'
    )

    def repl(match: re.Match) -> str:
        attrs = match.group('attrs')
        m = re.search(r'\bclass="([^"]*)"', attrs)
        if m:
            classes = m.group(1).split()
            if 'is-active' in classes:
                return match.group(0)
            classes.append('is-active')
            new_attrs = re.sub(
                r'\bclass="[^"]*"',
                'class="' + ' '.join(classes) + '"',
                attrs,
                count=1,
            )
        else:
            new_attrs = attrs.rstrip() + ' class="is-active"'
        return f'<a{new_attrs}>'

    new_nav = pattern.sub(repl, nav_block, count=1)
    return html[:nav_match.start()] + new_nav + html[nav_match.end():]


def copy_tree(src: str, dst: str) -> None:
    """Recursively copy a directory, replacing the destination if it exists."""
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def build() -> None:
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    # Static assets — minify CSS and JS
    css_dir = os.path.join(DIST, 'css')
    js_dir = os.path.join(DIST, 'js')
    os.makedirs(css_dir, exist_ok=True)
    os.makedirs(js_dir, exist_ok=True)

    with open(os.path.join(ROOT, 'style.css'), encoding='utf-8') as f:
        raw_css = f.read()
    minified_css = minify_css(raw_css)
    with open(os.path.join(css_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(minified_css)
    savings_css = 100 - len(minified_css) * 100 // len(raw_css)
    print(f'Minified CSS: {len(raw_css)} → {len(minified_css)} bytes (−{savings_css}%)')

    with open(os.path.join(ROOT, 'main.js'), encoding='utf-8') as f:
        raw_js = f.read()
    minified_js = minify_js(raw_js)
    with open(os.path.join(js_dir, 'main.js'), 'w', encoding='utf-8') as f:
        f.write(minified_js)
    savings_js = 100 - len(minified_js) * 100 // len(raw_js)
    print(f'Minified JS:  {len(raw_js)} → {len(minified_js)} bytes (−{savings_js}%)')

    copy_tree(os.path.join(ROOT, 'img'), os.path.join(DIST, 'img'))

    # Copy favicon.ico to the site root (browsers request /favicon.ico)
    shutil.copy2(os.path.join(ROOT, 'img', 'favicon.ico'),
                 os.path.join(DIST, 'favicon.ico'))

    year = datetime.datetime.now().year
    base = SITE_URL.rstrip('/')

    for out_name, meta in PAGES.items():
        body_path = os.path.join(ROOT, meta['body'])
        with open(body_path, encoding='utf-8') as f:
            body = f.read()
        canonical = base + '/' + out_name
        jsonld = build_jsonld(out_name)
        html = HEAD.format(
            title=meta['title'],
            description=meta['description'],
            canonical=canonical,
        )
        html += HEADER
        html += body
        html += FOOTER.format(year=year, jsonld=jsonld)
        html = mark_active(html, out_name)
        with open(os.path.join(DIST, out_name), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'Built dist/{out_name}')

    # ── Generate sitemap.xml ─────────────────────────────────────────────────
    generate_sitemap()
    print('Built dist/sitemap.xml')

    # ── Generate robots.txt ──────────────────────────────────────────────────
    generate_robots()
    print('Built dist/robots.txt')

    # ── Generate manifest.json (PWA) ─────────────────────────────────────────
    generate_manifest()
    print('Built dist/manifest.json')

    # ── Generate 404 page ────────────────────────────────────────────────────
    generate_404(year)
    print('Built dist/404.html')

    # ── Generate privacy policy ──────────────────────────────────────────────
    generate_privacy(year, base)
    print('Built dist/privacy.html')

    print(f'\nDone. Static site is in: {DIST}')
    print('Preview locally: python3 -m http.server -d dist 8080')


def generate_sitemap() -> None:
    """Generate a sitemap.xml with all public pages, priorities and changefreq.

    Uses the W3C date format (YYYY-MM-DD) for <lastmod> and adheres to the
    Sitemaps 0.9 protocol (https://www.sitemaps.org/protocol.html).
    """
    today = datetime.date.today().isoformat()  # YYYY-MM-DD
    base = SITE_URL.rstrip('/')

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        '        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9',
        '                            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">',
    ]

    # Order: main page first, then by descending priority, then alphabetically
    ordered = sorted(
        PAGES.keys(),
        key=lambda p: (
            0 if p == 'index.html' else 1,
            -float(SITEMAP_META.get(p, {}).get('priority', '0.5')),
            p,
        ),
    )

    for page in ordered:
        meta = SITEMAP_META.get(page, {'priority': '0.5', 'changefreq': 'monthly'})
        loc = f'{base}/{page}'
        lines.append('  <url>')
        lines.append(f'    <loc>{loc}</loc>')
        lines.append(f'    <lastmod>{today}</lastmod>')
        lines.append(f'    <changefreq>{meta["changefreq"]}</changefreq>')
        lines.append(f'    <priority>{meta["priority"]}</priority>')
        lines.append('  </url>')

    lines.append('</urlset>')
    lines.append('')  # trailing newline

    with open(os.path.join(DIST, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def generate_robots() -> None:
    """Generate a robots.txt with rules for major crawlers.

    Includes:
    - Universal rules (User-agent: *)
    - Yandex-specific directives (Host, Clean-param)
    - Sitemap reference
    - Disallow for service/internal paths
    """
    base = SITE_URL.rstrip('/')

    content = f"""# robots.txt — {base}
# Автоматически сгенерировано build.py

# ── Общие правила для всех роботов ──────────────────────────────────────────
User-agent: *
Allow: /

# Запретить индексацию служебных и внутренних страниц
Disallow: /test-api.html
Disallow: /test-embed.html
Disallow: /dist/
Disallow: /*.py$
Disallow: /node_modules/
Disallow: /.git/

# ── Яндекс ──────────────────────────────────────────────────────────────────
User-agent: Yandex
Allow: /
Disallow: /test-api.html
Disallow: /test-embed.html

# Предпочтительное зеркало
Host: {base}

# Удалять UTM- и рекламные параметры из URL при индексации
Clean-param: utm_source&utm_medium&utm_campaign&utm_content&utm_term
Clean-param: yclid&gclid&fbclid&from

# ── Google ──────────────────────────────────────────────────────────────────
User-agent: Googlebot
Allow: /
Disallow: /test-api.html
Disallow: /test-embed.html

# Разрешить индексацию изображений
User-agent: Googlebot-Image
Allow: /img/

# ── Sitemap ─────────────────────────────────────────────────────────────────
Sitemap: {base}/sitemap.xml
"""

    with open(os.path.join(DIST, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(content)


def generate_manifest() -> None:
    """Generate a PWA manifest.json."""
    manifest = {
        "name": "КА-Строй — дорожное строительство",
        "short_name": "КА-Строй",
        "description": "Производство асфальта, строительство и ремонт дорог в Новосибирске",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#1a1c20",
        "theme_color": "#1a1c20",
        "lang": "ru",
        "icons": [
            {
                "src": "img/favicon-192.png",
                "sizes": "192x192",
                "type": "image/png",
            },
            {
                "src": "img/favicon-512.png",
                "sizes": "512x512",
                "type": "image/png",
            },
        ],
    }
    with open(os.path.join(DIST, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def generate_404(year: int) -> None:
    """Generate a custom 404 page."""
    base = SITE_URL.rstrip('/')
    html = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Страница не найдена — КА-Строй</title>
<meta name="robots" content="noindex,nofollow">
<link rel="icon" href="img/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="img/favicon-192.png">
<link rel="stylesheet" href="css/style.css">
<meta name="theme-color" content="#1a1c20">
</head>
<body>
<div style="min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:40px 20px">
  <div>
    <div style="font-size:120px;font-weight:900;color:var(--orange);line-height:1">404</div>
    <h1 style="font-size:28px;color:#fff;margin:20px 0 12px">Страница не найдена</h1>
    <p style="color:var(--text-2);font-size:16px;margin-bottom:32px;max-width:440px">Такой страницы не существует или она была удалена.<br>Проверьте адрес или вернитесь на главную.</p>
    <a class="btn btn--primary" href="index.html">На главную</a>
  </div>
</div>
</body>
</html>'''
    with open(os.path.join(DIST, '404.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def generate_privacy(year: int, base: str) -> None:
    """Generate the privacy policy page."""
    canonical = base + '/privacy.html'
    jsonld = build_jsonld('privacy.html')
    html = HEAD.format(
        title='Политика конфиденциальности — КА-Строй',
        description='Политика обработки персональных данных ООО ИСК «КА-Строй». '
                    'Информация о сборе, хранении и использовании данных.',
        canonical=canonical,
    )
    html += HEADER
    html += f'''
<section class="page-hero">
  <div class="container page-hero__inner">
    <div class="breadcrumbs"><a href="index.html">Главная</a><span>›</span>Политика конфиденциальности</div>
    <span class="eyebrow">Документ</span>
    <h1 class="page-hero__title">Политика <b>конфиденциальности</b></h1>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="text-block" style="max-width:860px">
      <h2 class="h3" style="margin-bottom:14px">1. Общие положения</h2>
      <p>Настоящая Политика конфиденциальности определяет порядок обработки и защиты персональных данных пользователей сайта <a href="{base}" style="color:var(--orange)">{base}</a> (далее — Сайт), принадлежащего ООО ИСК «КА-Строй» (далее — Оператор).</p>
      <p>Оператор: ООО ИСК «КА-Строй», г. Новосибирск, ул. 1-ая Грузинская, 32/1, 630040.<br>E-mail: <a href="mailto:ka-stroy54@bk.ru" style="color:var(--orange)">ka-stroy54@bk.ru</a>, тел. +7 (383) 311-02-02.</p>

      <h2 class="h3" style="margin:28px 0 14px">2. Какие данные мы собираем</h2>
      <p>Через формы обратной связи и заказа звонка на Сайте мы можем запрашивать:</p>
      <ul style="margin:10px 0 10px 20px;color:var(--text-2);list-style:disc">
        <li>Имя (как к вам обращаться)</li>
        <li>Номер телефона</li>
        <li>Адрес электронной почты (при наличии)</li>
        <li>Текст сообщения / комментарий</li>
      </ul>
      <p>Мы не собираем данные банковских карт, паспортные данные и иную чувствительную информацию через Сайт.</p>

      <h2 class="h3" style="margin:28px 0 14px">3. Цели обработки</h2>
      <p>Персональные данные обрабатываются исключительно для:</p>
      <ul style="margin:10px 0 10px 20px;color:var(--text-2);list-style:disc">
        <li>Обратной связи с пользователем (звонок, письмо)</li>
        <li>Подготовки коммерческого предложения или сметы</li>
        <li>Улучшения качества обслуживания</li>
      </ul>

      <h2 class="h3" style="margin:28px 0 14px">4. Передача данных третьим лицам</h2>
      <p>Отправка форм осуществляется через сервис <b style="color:#fff">Web3Forms</b>. Данные передаются на серверы Web3Forms для пересылки на e-mail Оператора. Мы не передаём ваши данные иным третьим лицам, за исключением случаев, предусмотренных законодательством РФ.</p>

      <h2 class="h3" style="margin:28px 0 14px">5. Хранение и защита данных</h2>
      <p>Персональные данные хранятся на электронной почте Оператора и удаляются по завершении цели обработки или по запросу субъекта данных. Оператор принимает необходимые организационные и технические меры для защиты данных от несанкционированного доступа.</p>

      <h2 class="h3" style="margin:28px 0 14px">6. Права пользователя</h2>
      <p>Вы вправе:</p>
      <ul style="margin:10px 0 10px 20px;color:var(--text-2);list-style:disc">
        <li>Запросить информацию о хранящихся данных</li>
        <li>Потребовать их изменения или удаления</li>
        <li>Отозвать согласие на обработку</li>
      </ul>
      <p>Для этого направьте запрос на <a href="mailto:ka-stroy54@bk.ru" style="color:var(--orange)">ka-stroy54@bk.ru</a> или позвоните по тел. +7 (383) 311-02-02.</p>

      <h2 class="h3" style="margin:28px 0 14px">7. Файлы cookie</h2>
      <p>Сайт может использовать файлы cookie для корректной работы и сбора анонимной статистики посещаемости. Вы можете отключить cookie в настройках браузера.</p>

      <h2 class="h3" style="margin:28px 0 14px">8. Изменения</h2>
      <p>Оператор оставляет за собой право обновлять настоящую Политику. Актуальная версия всегда доступна на данной странице.</p>
      <p style="margin-top:20px;color:var(--text-3)">Дата последнего обновления: {datetime.date.today().strftime("%d.%m.%Y")}</p>
    </div>
  </div>
</section>
'''
    html += FOOTER.format(year=year, jsonld=jsonld)
    with open(os.path.join(DIST, 'privacy.html'), 'w', encoding='utf-8') as f:
        f.write(html)


if __name__ == '__main__':
    build()
