# TokenHunter

**TokenHunter** — крипто-система наблюдения за рынком (market pulse scanner), работающая через Telegram-бот и Telegram Mini App.

## Описание

TokenHunter — это автономная система для:
- Автоматического сбора и сравнения торговых пар с нескольких бирж (multi-exchange)
- Подписочной модели доступа
- Реферальной системы
- Розыгрышей
- Админ-управления через Telegram
- Визуального Mini App в стиле современной «Матрицы»

## Технологии

- **Python 3.11+**
- **python-telegram-bot** — Telegram Bot API
- **ccxt** — интеграция с криптобиржами
- **SQLite** — локальное хранилище данных
- **Flask** — веб-сервер для Mini App
- **GitHub Actions** — автоматический сбор данных (cron)

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/TimurSama/th_demo
cd th_demo
```

**Репозиторий**: https://github.com/TimurSama/th_demo

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env`:
```bash
python scripts/setup_env.py
```

Или создайте вручную файл `.env` с содержимым:
```
TELEGRAM_BOT_TOKEN=8591869020:AAFnlsirUwd3TKMibAWDE209OBwVU40ZEjo
TELEGRAM_WEBAPP_URL=https://your-domain.com/webapp
```

**Примечание**: Токен уже настроен в скрипте setup_env.py. Обновите только `TELEGRAM_WEBAPP_URL` после развертывания веб-приложения.

6. Инициализируйте базу данных:
```bash
python main.py
```

## Запуск

### Telegram Bot
```bash
python main.py
```

### Web App (Mini App)
```bash
python run_webapp.py
```

### Сбор данных рынка (вручную)
```bash
python scripts/collect_market_data.py
```

## Структура проекта

```
tokenhuner2/
├── bot/                    # Telegram Bot
│   ├── bot.py             # Главный файл бота
│   ├── handlers.py        # Обработчики команд и callback
│   └── admin_handlers.py  # Админ-команды
├── database/              # Модели базы данных
│   └── models.py
├── services/              # Бизнес-логика
│   ├── market_collector.py
│   ├── subscription_service.py
│   └── referral_service.py
├── webapp/                # Telegram Mini App
│   ├── app.py            # Flask приложение
│   └── templates/
│       └── index.html    # Главная страница
├── scripts/               # Скрипты
│   └── collect_market_data.py
├── .github/workflows/     # GitHub Actions
│   └── collect_market_data.yml
├── config.py             # Конфигурация
├── main.py               # Точка входа
└── requirements.txt      # Зависимости
```

## Функциональность

### Telegram Bot

#### Команды пользователя:
- `/start` — начало работы с ботом (поддержка реферальных ссылок)

#### Меню:
- **GET THE PULSE** — получить последние данные рынка
- **Subscription Level** — просмотр уровней подписки
- **Referral System** — реферальная система
- **Giveaways** — розыгрыши
- **Application** — открыть Mini App

#### Админ-команды:
- `/admin_stats` — статистика системы
- `/admin_post <title> <content>` — создать новость
- `/admin_giveaway_start <title> <prize> <prize_type> <days>` — запустить розыгрыш
- `/admin_giveaway_end <giveaway_id>` — завершить розыгрыш
- `/admin_broadcast <message>` — массовая рассылка

### Telegram Mini App

Визуальный интерфейс с разделами:
- **Dashboard** — общая статистика и статус
- **Market & Signals** — данные рынка и сигналы
- **Profile** — личный кабинет
- **Giveaways** — активные розыгрыши
- **News & Updates** — новости проекта

## Уровни подписки

- **FREE** — Market pulse каждые 4 часа, ограниченные сигналы
- **PRO** — Market pulse каждые 2 часа, расширенные сигналы
- **PREMIUM** — Market pulse каждый час, полный доступ к сигналам

## Реферальная система

Пользователи могут приглашать других через персональную реферальную ссылку. Система отслеживает количество приглашённых пользователей.

## Автоматический сбор данных

GitHub Actions настроен на автоматический сбор данных рынка каждый час. Для работы необходимо:
1. Добавить `TELEGRAM_BOT_TOKEN` в Secrets репозитория (см. GITHUB_SETUP.md)
2. GitHub Actions автоматически будет собирать данные каждый час

Подробная инструкция: см. [GITHUB_SETUP.md](GITHUB_SETUP.md)

## Стиль общения

TokenHunter использует стиль общения в духе «Матрицы»:
- "The network is watching."
- "Signal detected."
- "You are inside the grid."
- "Data stream updated."
- "Choose your level of access."

## Разработка

Код модульный, с разделением бизнес-логики и UI. Готов к расширению:
- Интеграция платежей
- Подключение кошельков
- Автоматическая торговля

## Быстрый старт

См. [QUICKSTART.md](QUICKSTART.md) для быстрой настройки за 5 минут.

## Настройка GitHub

Инструкция по настройке GitHub Actions и секретов: [GITHUB_SETUP.md](GITHUB_SETUP.md)

## Репозиторий

GitHub: https://github.com/TimurSama/th_demo

