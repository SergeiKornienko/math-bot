```markdown
# Math Bot

Математический бот-калькулятор для Telegram, VK Max и Web.
Построен вокруг вычислительного ядра на Python с точной десятичной арифметикой.

## Быстрый старт (Termux / Android)

**Требования:** Termux из F-Droid, git.

```bash
git clone <repo-url>
cd math-bot
source setup.sh
```

Скрипт устанавливает системные пакеты, создаёт виртуальное окружение,
выставляет переменные для Android и устанавливает все Python-зависимости.
Wheel-файлы кэшируются в ~/.pip-wheels для быстрой переустановки.

· Первая установка: ~20 мин (компиляция Rust-пакетов)
· Повторная: ~2 мин (из кэша)

Активация окружения

Вручную:

```bash
source .venv/bin/activate
```

Автоматически (рекомендуется):

```bash
pkg install direnv
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
source ~/.zshrc
cd math-bot
direnv allow
```

Переменные окружения (только Termux)

Выставляются автоматически через setup.sh. Для ручной установки:

```bash
export CARGO_BUILD_TARGET=aarch64-linux-android
export ANDROID_API_LEVEL=$(getprop ro.build.version.sdk 2>/dev/null || echo "34")
export ANDROID_NDK_HOME=/data/data/com.termux/files/usr
```

---

Структура проекта

```
math-bot/
├── core/                   # Вычислительное ядро
│   ├── exceptions.py       # Иерархия исключений
│   ├── tokenizer.py        # Разбор строки на токены
│   ├── parser.py           # Алгоритм сортировочной станции
│   └── evaluator.py        # Вычисление постфиксной записи
├── interfaces/             # Точки входа
│   ├── tg_bot/             # Telegram бот
│   ├── vk_bot/             # VK / Max бот
│   └── web/                # FastAPI веб-интерфейс
├── tests/                  # Тесты pytest
├── pyproject.toml          # Конфигурация и зависимости
├── requirements-lock.txt   # Точные версии (генерируется setup.sh)
├── setup.sh                # Скрипт настройки окружения
└── README.md
```

---

Инструменты разработки

Инструмент Назначение Команда
pytest Запуск тестов pytest tests/ -v
pytest-cov Покрытие тестами pytest --cov=core tests/
flake8 Линтер flake8 core/ tests/
mypy Проверка типов mypy core/
black Форматтер black .

Требования к коду:

· Покрытие тестами > 95%
· Все функции с аннотациями типов
· Код проходит flake8 без ошибок
· Длина строки 79 символов
· Код отформатирован black

---

Зависимости

Основные:

· fastapi >= 0.115.0 — веб-фреймворк
· uvicorn — ASGI-сервер
· pydantic >= 2.10 — валидация данных
· python-telegram-bot >= 21.0 — Telegram API
· vkbottle >= 4.3 — VK API
· supabase >= 2.3 — клиент БД
· structlog — структурированное логирование
· httpx — асинхронный HTTP
· jinja2 — шаблонизатор

Для разработки:

· pytest, pytest-cov, pytest-asyncio — тестирование
· mypy >= 1.11 — проверка типов
· black >= 24.0 — форматтер
· flake8 >= 7.0 — линтер

---

Почему первая установка долгая

Два пакета написаны на Rust и компилируются из исходников под Android:

Пакет Назначение Время
pydantic-core Движок валидации pydantic ~10 мин
ast-serialize Сериализация AST для mypy ~5 мин

Это происходит один раз. Результат кэшируется в ~/.pip-wheels/.

---

CI/CD

GitHub Actions при каждом push в main:

1. Линтинг (flake8)
2. Проверка типов (mypy)
3. Тесты с покрытием > 95%

Деплой на Render только после зелёного пайплайна.

---

База данных и деплой

· База данных: Supabase (PostgreSQL)
· Хостинг: Render (Web Service + Worker + Cron Job)
· Пинг: Render Cron Job каждые 10 минут стучится в /health

Переменные окружения (задаются в дашборде Render):

Переменная Назначение
SUPABASE_URL URL базы данных
SUPABASE_KEY Service role key
TG_BOT_TOKEN Токен Telegram бота
VK_BOT_TOKEN Токен сообщества VK

---

Настройка нового устройства

```bash
# 1. Установить Termux из F-Droid
# 2. Установить git
pkg install git

# 3. Клонировать и настроить
git clone <repo-url>
cd math-bot
source setup.sh

# 4. (Опционально) автоактивация venv
pkg install direnv
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
source ~/.zshrc
direnv allow
```

---

Частые вопросы

В: Почему F-Droid, а не Play Store?
О: Версия из Play Store устарела. F-Droid содержит актуальную версию с поддержкой Rust.

В: Как ускорить переустановку?
О: setup.sh кэширует wheel-файлы в ~/.pip-wheels. Повторная установка идёт из кэша.

В: Что делать если getprop не найден?
О: Выставьте API level вручную: export ANDROID_API_LEVEL=34 (подставьте свою версию Android).

В: Как обновить зависимости?
О: Удалите requirements-lock.txt, очистите кэш rm -rf ~/.pip-wheels/math* и запустите source setup.sh заново.

```

---


