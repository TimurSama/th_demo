# Структура проекта TokenHunter

## Обзор

TokenHunter — модульная крипто-система наблюдения за рынком с Telegram Bot и Mini App интерфейсом.

## Архитектура

```
tokenhuner2/
├── bot/                          # Telegram Bot модуль
│   ├── __init__.py              # Экспорт handlers
│   ├── bot.py                   # Главный файл бота
│   ├── handlers.py              # Пользовательские handlers
│   └── admin_handlers.py        # Админ-команды
│
├── database/                     # Модели базы данных
│   ├── __init__.py              # Экспорт моделей
│   └── models.py                # SQLite модели и схемы
│
├── services/                     # Бизнес-логика
│   ├── __init__.py              # Экспорт сервисов
│   ├── market_collector.py     # Сбор данных с бирж (ccxt)
│   ├── subscription_service.py  # Управление подписками
│   └── referral_service.py     # Реферальная система
│
├── webapp/                       # Telegram Mini App
│   ├── __init__.py
│   ├── app.py                   # Flask приложение
│   └── templates/
│       └── index.html           # Главная страница (Matrix стиль)
│
├── scripts/                      # Утилиты и скрипты
│   ├── __init__.py
│   ├── collect_market_data.py  # Сбор данных рынка
│   └── add_admin.py            # Добавление администратора
│
├── .github/workflows/            # GitHub Actions
│   └── collect_market_data.yml  # Автоматический сбор данных
│
├── data/                         # База данных (создается автоматически)
│   └── tokenhunter.db           # SQLite база данных
│
├── config.py                     # Конфигурация приложения
├── main.py                       # Точка входа (бот)
├── run_webapp.py                 # Запуск веб-приложения
├── requirements.txt              # Python зависимости
├── README.md                     # Основная документация
├── SETUP.md                      # Инструкция по настройке
└── .env                          # Переменные окружения (не в git)
```

## Модули

### bot/
Telegram Bot реализация с использованием `python-telegram-bot`.

- **bot.py**: Инициализация и запуск бота
- **handlers.py**: Обработчики команд и callback'ов для пользователей
- **admin_handlers.py**: Админ-команды для управления системой

### database/
Модели данных и работа с SQLite.

- **models.py**: Определение таблиц и моделей (User, Referral, MarketSnapshot, Signal, Giveaway, News)

### services/
Бизнес-логика, отделенная от UI.

- **market_collector.py**: Сбор данных с криптобирж через ccxt
- **subscription_service.py**: Управление уровнями подписки
- **referral_service.py**: Реферальная система

### webapp/
Flask приложение для Telegram Mini App.

- **app.py**: REST API endpoints для Mini App
- **templates/index.html**: Визуальный интерфейс в стиле Matrix

## Потоки данных

1. **Сбор данных рынка**:
   - GitHub Actions (cron) → `scripts/collect_market_data.py` → `services/market_collector.py` → `database/models.py`

2. **Пользовательский запрос**:
   - Telegram → `bot/handlers.py` → `services/*.py` → `database/models.py`

3. **Mini App запрос**:
   - Browser → `webapp/app.py` → `database/models.py`

## Расширяемость

Проект спроектирован для легкого расширения:

- **Платежи**: Добавить модуль в `services/payment_service.py`
- **Кошельки**: Добавить модуль в `services/wallet_service.py`
- **Автотрейдинг**: Добавить модуль в `services/trading_service.py`

Все новые сервисы должны следовать паттерну разделения бизнес-логики и UI.

