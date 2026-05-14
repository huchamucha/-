#!/usr/bin/env python3
"""Build the КА-Строй site. Wraps each page body with shared header/footer/layout."""
import os, re
 
ROOT = os.path.dirname(os.path.abspath(__file__))
 
HEAD = '''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" type="image/png" href="img/logo.png">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
'''
 
HEADER = '''<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="index.html">
      <img class="brand__logo" src="img/logo.png" alt="КА-Строй">
      <span class="brand__name">КА<b>-</b>СТРОЙ</span>
    </a>
    <button class="nav-toggle" aria-label="Меню"><span></span></button>
    <nav class="nav" aria-label="Главное меню">
      <a href="index.html">Главная</a>
      <a href="about.html">О компании</a>
      <a href="asfalt_nsk.html">Асфальт</a>
      <a href="arenda_techniki_nsk.html">Аренда техники</a>
      <a href="calculator.html">Калькулятор</a>
      <a href="gallery.html">Работы</a>
      <a href="news.html">Новости</a>
      <a class="nav-cta" href="contacts.html">Контакты</a>
    </nav>
  </div>
</header>
'''
 
FOOTER = '''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col">
        <div class="footer-brand"><img class="brand__logo" src="img/logo.png" alt="КА-Строй"><span class="brand__name">КА<b>-</b>СТРОЙ</span></div>
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
    </div>
  </div>
</footer>
<script src="js/main.js"></script>
</body>
</html>
'''
 
PAGES = {
  'index.html': {
    'title': 'КА-Строй — дорожное строительство в Новосибирске | асфальт, ремонт дорог, аренда техники',
    'description': 'КА-Строй — производство асфальта, строительство и ремонт дорог, благоустройство, аренда спецтехники в Новосибирске. Собственный АБЗ, член АСОНО, работа по 44-ФЗ и 223-ФЗ.',
    'body': 'page_index.html'
  },
  'about.html': {
    'title': 'О компании — ООО ИСК «КА-Строй» в Новосибирске',
    'description': 'ООО ИСК «КА-Строй» с 2020 года: член АСОНО (СРО-С-284-21062017), собственный АБЗ, парк техники, более 14 контрактов по 44-ФЗ за год.',
    'body': 'page_about.html'
  },
  'asfalt_nsk.html': {
    'title': 'Асфальт и материалы для дорожного строительства — КА-Строй Новосибирск',
    'description': 'Производство и продажа асфальтобетонной смеси Б-II от 5000 ₽/т, ЩПС, песка, щебня. Асфальтирование дорог под ключ от 500 ₽/м². Доставка по Новосибирску и НСО.',
    'body': 'page_asfalt.html'
  },
  'arenda_techniki_nsk.html': {
    'title': 'Аренда спецтехники в Новосибирске — КА-Строй',
    'description': 'Аренда экскаваторов, катков, асфальтоукладчиков, погрузчиков, грейдеров в Новосибирске. Промокод «САЙТ КА-СТРОЙ» — скидка −10%.',
    'body': 'page_arenda.html'
  },
  'calculator.html': {
    'title': 'Калькулятор стоимости работ и материалов — КА-Строй',
    'description': 'Онлайн-калькулятор стоимости асфальтирования, материалов (асфальт Б-II, ЩПС, песок) и аренды спецтехники.',
    'body': 'page_calculator.html'
  },
  'gallery.html': {
    'title': 'Галерея наших работ — КА-Строй Новосибирск',
    'description': 'Реальные объекты КА-Строй: асфальтирование, ремонт автодорог, благоустройство в Новосибирске и Новосибирской области (ТУАД, МКУ «Дзержинка» и др.).',
    'body': 'page_gallery.html'
  },
  'news.html': {
    'title': 'Новости компании КА-Строй',
    'description': 'Новости и пресс-релизы компании КА-Строй: участие в нацпроектах, новые контракты, развитие производства.',
    'body': 'page_news.html'
  },
  'contacts.html': {
    'title': 'Контакты КА-Строй в Новосибирске — телефон, адрес офиса',
    'description': 'Контакты КА-Строй: офис +7 (383) 311-02-02, аренда техники, материалы, производство работ. Адрес: г. Новосибирск, ул. 1-ая Грузинская, 32/1.',
    'body': 'page_contacts.html'
  }
}
 
def main():
    bodies_dir = os.path.join(ROOT, '_partials')
    for out, meta in PAGES.items():
        body_path = os.path.join(bodies_dir, meta['body'])
        with open(body_path, encoding='utf-8') as f:
            body = f.read()
        html = HEAD.format(title=meta['title'], description=meta['description'])
        html += HEADER
        html += body
        html += FOOTER.format(year=2026)
        with open(os.path.join(ROOT, out), 'w', encoding='utf-8') as f:
            f.write(html)
        print('Built', out)
 
if __name__ == '__main__':
    main()