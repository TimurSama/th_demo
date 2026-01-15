# Настройка GitHub репозитория

## Шаг 1: Добавление секретов в GitHub

1. Перейдите в ваш репозиторий: https://github.com/TimurSama/th_demo
2. Откройте **Settings** → **Secrets and variables** → **Actions**
3. Нажмите **New repository secret**
4. Добавьте секрет:
   - **Name**: `TELEGRAM_BOT_TOKEN`
   - **Value**: `8591869020:AAFnlsirUwd3TKMibAWDE209OBwVU40ZEjo`

## Шаг 2: Настройка GitHub Actions

GitHub Actions автоматически настроен для:
- Сбора данных рынка каждый час (cron: `0 * * * *`)
- Ручного запуска через **Actions** → **Collect Market Data** → **Run workflow**

## Шаг 3: Проверка работы

1. После добавления секрета, GitHub Actions начнет работать автоматически
2. Проверьте статус в разделе **Actions** вашего репозитория
3. Данные будут собираться и сохраняться в `data/tokenhunter.db`

## Важные замечания

- Токен бота хранится в секретах GitHub и не попадет в код
- База данных будет коммититься в репозиторий (для синхронизации данных)
- Если нужно изменить расписание сбора данных, отредактируйте `.github/workflows/collect_market_data.yml`

## Получение User ID для админа

1. Откройте [@userinfobot](https://t.me/userinfobot) в Telegram
2. Отправьте `/start`
3. Скопируйте ваш User ID
4. Добавьте себя как администратора локально:
   ```bash
   python scripts/add_admin.py <ваш_user_id>
   ```

