# Сайт ООО ИСК «КА-Строй»

Статический сайт компании (Новосибирск) — производство асфальта, дорожные работы, благоустройство, аренда спецтехники. Сайт собирается одним Python-скриптом и публикуется через любой обычный хостинг (FTP, S3, Netlify, Cloudflare Pages и т. п.).

## Структура репозитория

```
build.py              # сборка сайта в dist/
page_index.html       # body главной
page_about.html
page_asfalt.html      # «Прайс-лист»
page_arenda.html
page_calculator.html  # калькулятор полной сметы
page_gallery.html     # «Галерея работ»
page_news.html
page_contacts.html
style.css             # общие стили
main.js               # мобильное меню, форма Web3Forms
img/                  # логотип и фото галереи
dist/                 # результат сборки (создаётся build.py)
```

Каждый `page_*.html` — это только тело страницы. Общая шапка, подвал, мета-теги и подключение CSS/JS добавляются автоматически из `build.py`.

## Сборка

```bash
python3 build.py
```

Скрипт:
- очищает каталог `dist/`;
- копирует `style.css` в `dist/css/`, `main.js` в `dist/js/`, всё содержимое `img/` в `dist/img/`;
- собирает каждую страницу: `<head>` + `<header>` + тело `page_*.html` + `<footer>`;
- помечает класс `is-active` у пункта меню, соответствующего текущей странице;
- подставляет текущий год в копирайт футера.

Зависимостей нет — только стандартная библиотека Python 3.

## Локальный предпросмотр

```bash
python3 -m http.server -d dist 8080
```

Откройте `http://localhost:8080/`.

## Деплой

Сайт полностью статический. После сборки достаточно загрузить содержимое `dist/` в корень хостинга:

- **Обычный shared-хостинг** — загрузите все файлы из `dist/` по FTP/SFTP в корневую папку сайта (обычно `public_html/` или `www/`).
- **Netlify / Cloudflare Pages / Vercel** — укажите команду сборки `python3 build.py` и публикуемый каталог `dist`.
- **S3 / Yandex Object Storage** — синхронизируйте `dist/` с бакетом и включите статический хостинг (index document: `index.html`).
- **GitHub Pages** — соберите локально и закоммитьте `dist/` в ветку `gh-pages` (или используйте Action c `python3 build.py`).

Пути внутри собранных страниц — относительные (`css/style.css`, `js/main.js`, `img/...`), поэтому сайт работает в любой подпапке хостинга без изменений.

## Страницы

| URL | Заголовок в меню | Источник тела |
|-----|------------------|---------------|
| `index.html` | Главная | `page_index.html` |
| `about.html` | О компании | `page_about.html` |
| `asfalt_nsk.html` | Прайс-лист | `page_asfalt.html` |
| `arenda_techniki_nsk.html` | Аренда техники | `page_arenda.html` |
| `calculator.html` | Калькулятор | `page_calculator.html` |
| `gallery.html` | Галерея работ | `page_gallery.html` |
| `news.html` | Новости | `page_news.html` |
| `contacts.html` | Контакты | `page_contacts.html` |

## Изменение контента

- **Текст/блоки конкретной страницы** — `page_*.html`.
- **Шапка/футер/мета-теги** — константы `HEAD`, `HEADER`, `FOOTER` в `build.py`.
- **Список страниц, заголовки, описания** — словарь `PAGES` в `build.py`.
- **Общие стили** — `style.css`.
- **JS (моб. меню, форма)** — `main.js`.

После любых правок: `python3 build.py` → `dist/` обновлён → выкладываем на хостинг.

## Формы

Контактная форма на `contacts.html` и заявка на главной используют [Web3Forms](https://web3forms.com) с публичным `access_key`, лежащим в `main.js`. Сообщения уходят на e-mail, заданный в кабинете Web3Forms.
