# Пост-деплой инструкция

## ✅ Деплой завершен!

Код успешно загружен в репозиторий: https://github.com/TimurSama/th_demo

## Следующие шаги

### 1. Настройка GitHub Secrets (ОБЯЗАТЕЛЬНО)

Для работы GitHub Actions необходимо добавить секрет:

1. Перейдите в репозиторий: https://github.com/TimurSama/th_demo
2. Откройте **Settings** → **Secrets and variables** → **Actions**
3. Нажмите **New repository secret**
4. Добавьте:
   - **Name**: `TELEGRAM_BOT_TOKEN`
   - **Value**: `8591869020:AAFnlsirUwd3TKMibAWDE209OBwVU40ZEjo`
5. Нажмите **Add secret**

После этого GitHub Actions автоматически начнет собирать данные рынка каждый час.

### 2. Проверка GitHub Actions

1. Перейдите в раздел **Actions** вашего репозитория
2. Убедитесь, что workflow "Collect Market Data" виден
3. Можно запустить вручную: **Actions** → **Collect Market Data** → **Run workflow**

### 3. Локальный запуск бота

На вашем компьютере:

```bash
# Установка зависимостей
pip install -r requirements.txt

# Инициализация базы данных
python main.py
# Нажмите Ctrl+C после инициализации

# Добавление администратора
# Получите ваш User ID через @userinfobot
python scripts/add_admin.py <ваш_user_id>

# Запуск бота
python main.py
```

### 4. Тестирование бота

1. Откройте вашего бота в Telegram
2. Отправьте `/start`
3. Проверьте все функции:
   - ✅ GET THE PULSE
   - ✅ Subscription Level
   - ✅ Referral System
   - ✅ Giveaways
   - ✅ Application (Mini App)

### 5. Настройка Mini App (опционально)

Если хотите использовать Mini App:

1. Разверните веб-приложение на сервере с HTTPS
2. Обновите `TELEGRAM_WEBAPP_URL` в `.env`
3. В [@BotFather](https://t.me/BotFather):
   - `/mybots` → выберите бота → Bot Settings → Menu Button
   - Укажите URL вашего веб-приложения

## Важные файлы

- ✅ `.env` - НЕ попал в репозиторий (в .gitignore) - это правильно!
- ✅ Все исходные коды загружены
- ✅ GitHub Actions workflow настроен
- ✅ Документация включена

## Проверка деплоя

Откройте репозиторий и убедитесь, что все файлы на месте:
- https://github.com/TimurSama/th_demo

## Полезные ссылки

- **Репозиторий**: https://github.com/TimurSama/th_demo
- **Быстрый старт**: см. QUICKSTART.md
- **Настройка GitHub**: см. GITHUB_SETUP.md
- **Развертывание**: см. DEPLOYMENT.md

## Troubleshooting

### GitHub Actions не работает?
- Проверьте, что секрет `TELEGRAM_BOT_TOKEN` добавлен
- Проверьте логи в разделе Actions
- Убедитесь, что workflow файл существует

### Бот не отвечает?
- Проверьте, что `.env` файл существует локально
- Убедитесь, что токен правильный
- Проверьте, что бот запущен (`python main.py`)

### Ошибки при клонировании?
```bash
git clone https://github.com/TimurSama/th_demo
cd th_demo
python scripts/setup_env.py
```

