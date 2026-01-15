# Быстрый старт TokenHunter

## Минимальная настройка (5 минут)

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Создание .env файла
```bash
python scripts/setup_env.py
```

Токен бота уже настроен в скрипте. Файл `.env` будет создан автоматически.

### 3. Инициализация базы данных
```bash
python main.py
```

Это создаст базу данных. Нажмите `Ctrl+C` чтобы остановить бота после инициализации.

### 4. Добавление администратора

Получите ваш User ID:
1. Откройте [@userinfobot](https://t.me/userinfobot) в Telegram
2. Отправьте `/start`
3. Скопируйте ваш ID

Добавьте себя как администратора:
```bash
python scripts/add_admin.py <ваш_user_id>
```

### 5. Запуск бота
```bash
python main.py
```

Бот готов к работе! Откройте его в Telegram и отправьте `/start`.

## Настройка GitHub Actions (опционально)

Для автоматического сбора данных рынка:

1. Перейдите в https://github.com/TimurSama/th_demo
2. Settings → Secrets and variables → Actions
3. Добавьте секрет `TELEGRAM_BOT_TOKEN` со значением: `8591869020:AAEUFxvA4uo5Ct1j62gtE39wI-gdkZfFRmw`

Подробнее: см. [GITHUB_SETUP.md](GITHUB_SETUP.md)

## Настройка Mini App (опционально)

1. Разверните веб-приложение на сервере с HTTPS
2. Обновите `TELEGRAM_WEBAPP_URL` в `.env`
3. В [@BotFather](https://t.me/BotFather):
   - `/mybots` → выберите бота → Bot Settings → Menu Button
   - Укажите URL вашего веб-приложения

## Проверка работы

1. Откройте бота в Telegram
2. Отправьте `/start`
3. Проверьте все функции:
   - ✅ GET THE PULSE
   - ✅ Subscription Level
   - ✅ Referral System
   - ✅ Giveaways

## Админ-команды

После добавления себя как администратора:

- `/admin_stats` - статистика
- `/admin_post Update "Новое обновление"` - создать новость
- `/admin_giveaway_start "Premium Access" "30 days" "premium" 7` - запустить розыгрыш
- `/admin_broadcast Привет всем!` - массовая рассылка

## Troubleshooting

**Бот не отвечает?**
- Проверьте, что `.env` файл существует и содержит правильный токен
- Убедитесь, что бот запущен (`python main.py`)

**Ошибка базы данных?**
- Убедитесь, что папка `data/` существует
- Проверьте права доступа

**GitHub Actions не работает?**
- Проверьте, что секрет `TELEGRAM_BOT_TOKEN` добавлен в репозиторий
- Проверьте логи в разделе Actions

