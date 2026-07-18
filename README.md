# MayakBot: RAG-экосистема Telegram-ботов

MayakBot — это микросервисная архитектура на базе Python, включающая в себя двух независимых Telegram-ботов, объединенных общим RAG-пайплайном (Retrieval-Augmented Generation). Проект генерирует контекстно-зависимые ответы, стилизованные под футуризм Владимира Маяковского.

## 🤖 Боты в экосистеме
* **Mayak   Mentor:** Суровый мотивационный бот, отвечающий хлесткой ритмичной прозой на жалобы о лени и выгорании.
* **Mayak Copywriter:** Бот-креатор для генерации коротких, пробивных рекламных слоганов под любой продукт.

## 🛠 Технологический стек
* **Язык:** Python 3.12+
* **Фреймворк:** aiogram 3 (Асинхронное взаимодействие с Telegram API)
* **LLM & RAG:** LangChain, OpenAI API (VseGPT)
* **Векторная БД:** ChromaDB (Локальное хранилище)
* **Эмбеддинги:** HuggingFace (`BAAI/bge-m3`)
* **Инфраструктура:** Docker, Docker Compose, uv (сверхбыстрый пакетный менеджер)

## 🏗 Архитектура проекта
* `data/` — Корпус текстов (`.jsonl`) и скомпилированная база данных ChromaDB.
* `notebooks/` — Jupyter-ноутбук для первичного парсинга и векторизации данных.
* `src/bots/` — Точки входа для запуска независимых ботов.
* `src/rag/` — Ядро проекта (инициализация LangChain, промптов и векторного поиска).
* `compose.yml` & `Dockerfile` — Конфигурации для контейнеризации.

## 🚀 Запуск проекта (Docker)

1. Клонируйте репозиторий:
```bash
git clone [https://github.com/Ruzik707/MayakBot.git](https://github.com/Ruzik707/MayakBot.git)
cd MayakBot
```

2. Создайте файл .env в корне проекта и добавьте ваши ключи:
```bash
MAYAKMENTOR_TOKEN=ваш_токен_бота_ментора
MAYAKCOPYWRITER_TOKEN=ваш_токен_бота_копирайтера
VSEGPT_API_KEY=ваш_ключ_от_vsegpt
```

3. Запустите сборку и деплой через Docker Compose:
```bash
docker compose up --build -d
```

## Пример работы (Mayak Mentor) 
<img width="560" height="586" alt="image" src="https://github.com/user-attachments/assets/c64cd1ab-07ee-49c9-9c74-41dbeee02613" />
