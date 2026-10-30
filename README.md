# КА-Строй + LM Studio local AI

Это репозиторий сайта ООО ИСК «КА-Строй» и локального AI-модуля под LM Studio.

Что сделано:
- сохранён исходный статический сайт в корне репозитория;
- добавлена локальная Python-обвязка для LM Studio/OpenAI-compatible API;
- добавлен тестовый сценарий для запуска модели через LM Studio;
- подготовлена документация для локального запуска и проверки.

Структура:

```text
.
├── app.py                 # Flask API, который вызывает LM Studio
├── lmstudio_client.py     # HTTP-клиент к /v1/chat/completions
├── test_lmstudio.py       # быстрый smoke test
├── requirements.txt       # зависимости
├── .env.example           # переменные окружения
├── build.py               # сборка статического сайта в dist/
├── page_*.html            # body-части страниц
├── style.css              # стили сайта
├── main.js                # frontend JS
├── img/                   # статические ресурсы
├── README.md              # документация
└── dist/                  # создаётся build.py
```

Коротко про новую задачу:
- сайт остаётся как основной проект;
- отдельный backend готов для локального LLM через LM Studio;
- можно быстро проверять промпты, парсить JSON и прототипировать AI-часть без Ollama/PowerShell-порчей.

## Быстрый старт

1. Установи LM Studio.
2. Загрузите модель (например, Qwen 2.5 7B/14B или любую подходящую локальную модель).
3. Включите Local Server в LM Studio.
4. Обычно это даст endpoint:
   - `http://localhost:1234/v1/chat/completions`
   - `Authorization: Bearer lm-studio`
5. Создай виртуальное окружение и установи зависимости:

```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

6. Запусти API:

```bash
python app.py
```

7. Проверь health:

```bash
curl http://localhost:5000/api/health
```

8. Проверь AI:

```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Напиши одно слово: ok"}'
```

## Переменные окружения

Скопируй `.env.example` в `.env` и настрой:

```env
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_API_KEY=lm-studio
LMSTUDIO_MODEL=local-model
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

## Пример ответа API

```json
{
  "ok": true,
  "model": "local-model",
  "response": "ok"
}
```

## Тестовый сценарий

```bash
python test_lmstudio.py
```

Этот скрипт отправляет простой запрос в LM Studio и печатает результат.

## Сборка статического сайта

Если нужно собрать статический сайт:

```bash
python build.py
```

После сборки:

```bash
python -m http.server -d dist 8080
```

## Важно

- LM Studio endpoint может отличаться по модели и настройкам.
- Подтягивай актуальное имя модели из интерфейса LM Studio.
- В коде можно переопределить model через `.env` или HTTP-параметры.

## Почему это решение сейчас

Проблемы с Ollama на Windows (порты, запуск сервера, конфликт процессов) резко усложняют локальные тесты. LM Studio даёт более стабильный OpenAI-совместимый API и быстрее приводит проект к рабочему состоянию.

Сайт и AI-слой разделены: frontend/site продолжает жить отдельно, а AI-логика запускается локально и тестируется независимо.
