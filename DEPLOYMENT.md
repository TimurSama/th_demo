# Инструкция по развертыванию TokenHunter

## Локальный запуск

### Шаг 1: Подготовка окружения

```bash
# Клонирование репозитория
git clone https://github.com/TimurSama/th_demo
cd th_demo

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt
```

### Шаг 2: Настройка конфигурации

```bash
# Создание .env файла (токен уже настроен)
python scripts/setup_env.py
```

Токен бота: `8591869020:AAFnlsirUwd3TKMibAWDE209OBwVU40ZEjo`

### Шаг 3: Инициализация базы данных

```bash
python main.py
```

Нажмите `Ctrl+C` после инициализации базы данных.

### Шаг 4: Добавление администратора

```bash
# Получите ваш User ID через @userinfobot
python scripts/add_admin.py <ваш_user_id>
```

### Шаг 5: Запуск бота

```bash
python main.py
```

Бот готов к работе!

## Развертывание на сервере

### Вариант 1: Systemd (Linux)

Создайте файл `/etc/systemd/system/tokenhunter.service`:

```ini
[Unit]
Description=TokenHunter Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/th_demo
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Запуск:
```bash
sudo systemctl enable tokenhunter
sudo systemctl start tokenhunter
sudo systemctl status tokenhunter
```

### Вариант 2: Docker (рекомендуется)

Создайте `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Создайте `docker-compose.yml`:

```yaml
version: '3.8'

services:
  bot:
    build: .
    volumes:
      - ./data:/app/data
      - ./.env:/app/.env
    restart: always
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
```

Запуск:
```bash
docker-compose up -d
```

### Вариант 3: Heroku

1. Установите Heroku CLI
2. Создайте `Procfile`:
```
worker: python main.py
```
3. Деплой:
```bash
heroku create your-app-name
heroku config:set TELEGRAM_BOT_TOKEN=8591869020:AAFnlsirUwd3TKMibAWDE209OBwVU40ZEjo
git push heroku main
```

## Развертывание Mini App

### Требования

- Сервер с HTTPS (обязательно для Telegram Mini App)
- Python 3.11+
- Flask

### Шаг 1: Настройка веб-сервера

```bash
# Установка зависимостей (если еще не установлены)
pip install -r requirements.txt
```

### Шаг 2: Запуск веб-приложения

```bash
python run_webapp.py
```

Или с использованием gunicorn (рекомендуется для продакшена):

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 webapp.app:app
```

### Шаг 3: Настройка Nginx (опционально)

Создайте конфигурацию `/etc/nginx/sites-available/tokenhunter`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Шаг 4: Настройка SSL (обязательно)

Используйте Let's Encrypt:

```bash
sudo certbot --nginx -d your-domain.com
```

### Шаг 5: Обновление .env

Обновите `TELEGRAM_WEBAPP_URL` в `.env`:
```
TELEGRAM_WEBAPP_URL=https://your-domain.com
```

### Шаг 6: Настройка Menu Button в BotFather

1. Откройте [@BotFather](https://t.me/BotFather)
2. `/mybots` → выберите вашего бота
3. Bot Settings → Menu Button
4. Укажите URL: `https://your-domain.com`

## GitHub Actions настройка

1. Перейдите в https://github.com/TimurSama/th_demo
2. Settings → Secrets and variables → Actions
3. Добавьте секрет:
   - Name: `TELEGRAM_BOT_TOKEN`
   - Value: `8591869020:AAFnlsirUwd3TKMibAWDE209OBwVU40ZEjo`

GitHub Actions автоматически будет собирать данные рынка каждый час.

## Мониторинг

### Логи бота

Логи выводятся в консоль. Для сохранения в файл:

```bash
python main.py >> bot.log 2>&1
```

### Проверка работы

1. Откройте бота в Telegram
2. Отправьте `/start`
3. Проверьте все функции
4. Используйте `/admin_stats` для проверки статистики

## Обновление

```bash
git pull origin main
pip install -r requirements.txt
# Перезапустите бота
```

## Резервное копирование

Важные файлы для бэкапа:
- `data/tokenhunter.db` - база данных
- `.env` - конфигурация

```bash
# Создание бэкапа
tar -czf backup_$(date +%Y%m%d).tar.gz data/ .env
```

## Troubleshooting

### Бот не отвечает
- Проверьте логи: `tail -f bot.log`
- Убедитесь, что токен правильный
- Проверьте интернет-соединение

### База данных не создается
- Проверьте права доступа к папке `data/`
- Убедитесь, что путь в `.env` правильный

### Mini App не открывается
- Убедитесь, что используется HTTPS
- Проверьте настройки Menu Button в BotFather
- Проверьте консоль браузера на ошибки

### GitHub Actions не работает
- Проверьте, что секрет добавлен правильно
- Проверьте логи в разделе Actions
- Убедитесь, что workflow файл существует

