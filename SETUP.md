# Инструкция по настройке TokenHunter

## Шаг 1: Получение Telegram Bot Token

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен

## Шаг 2: Настройка окружения

1. Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```

2. Отредактируйте `.env` файл:
```
TELEGRAM_BOT_TOKEN=ваш_токен_бота
TELEGRAM_WEBAPP_URL=https://ваш-домен.com/webapp
```

## Шаг 3: Установка зависимостей

```bash
pip install -r requirements.txt
```

## Шаг 4: Инициализация базы данных

```bash
python main.py
```

Это создаст базу данных и все необходимые таблицы.

## Шаг 5: Добавление администратора

Получите свой Telegram User ID (можно через [@userinfobot](https://t.me/userinfobot)) и выполните:

```bash
python scripts/add_admin.py <ваш_user_id>
```

## Шаг 6: Настройка Telegram Mini App

1. Разверните веб-приложение на вашем сервере (например, используя Flask)
2. Убедитесь, что приложение доступно по HTTPS
3. В [@BotFather](https://t.me/BotFather) выполните:
   - `/newapp` или `/mybots` → выберите вашего бота → Bot Settings → Menu Button
   - Укажите URL вашего веб-приложения

## Шаг 7: Запуск бота

```bash
python main.py
```

Бот должен запуститься и быть готов к работе.

## Шаг 8: Запуск веб-приложения (Mini App)

В отдельном терминале:

```bash
python run_webapp.py
```

## Шаг 9: Настройка GitHub Actions (опционально)

Для автоматического сбора данных рынка:

1. Перейдите в Settings → Secrets and variables → Actions вашего репозитория
2. Добавьте секрет `TELEGRAM_BOT_TOKEN` с токеном вашего бота
3. GitHub Actions будет автоматически собирать данные каждый час

## Тестирование

1. Откройте вашего бота в Telegram
2. Отправьте `/start`
3. Проверьте работу всех функций:
   - GET THE PULSE
   - Subscription Level
   - Referral System
   - Giveaways
   - Application (Mini App)

## Админ-команды

После добавления себя как администратора, вы можете использовать:

- `/admin_stats` - статистика системы
- `/admin_post <title> <content>` - создать новость
- `/admin_giveaway_start <title> <prize> <prize_type> <days>` - запустить розыгрыш
- `/admin_giveaway_end <giveaway_id>` - завершить розыгрыш
- `/admin_broadcast <message>` - массовая рассылка

## Troubleshooting

### Бот не отвечает
- Проверьте, что токен правильный в `.env`
- Убедитесь, что бот запущен (`python main.py`)

### База данных не создается
- Убедитесь, что папка `data/` существует и доступна для записи
- Проверьте права доступа к файлам

### Mini App не открывается
- Убедитесь, что веб-приложение доступно по HTTPS
- Проверьте настройки Menu Button в BotFather
- Проверьте консоль браузера на ошибки

### Ошибки при сборе данных рынка
- Проверьте интернет-соединение
- Убедитесь, что биржи доступны (не заблокированы)
- Проверьте логи на наличие ошибок API

