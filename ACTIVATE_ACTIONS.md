# Активация GitHub Actions

## Проблема: Actions не показывают логи

Если файлы есть на GitHub, но в разделе Actions нет логов, это означает, что workflow еще не запускался.

## Решение: Активация GitHub Actions

### Шаг 1: Добавьте секрет TELEGRAM_BOT_TOKEN

1. Откройте репозиторий: https://github.com/TimurSama/th_demo
2. Перейдите в **Settings** → **Secrets and variables** → **Actions**
3. Нажмите **New repository secret**
4. Добавьте:
   - **Name**: `TELEGRAM_BOT_TOKEN`
   - **Value**: `8591869020:AAFnlsirUwd3TKMibAWDE209OBwVU40ZEjo`
5. Нажмите **Add secret**

### Шаг 2: Запустите workflow вручную

1. Откройте раздел **Actions** в репозитории
2. В левом меню выберите **Collect Market Data**
3. Нажмите **Run workflow** (справа вверху)
4. Выберите ветку: `main`
5. Нажмите **Run workflow**

### Шаг 3: Проверка результата

После запуска:
1. В разделе Actions появится запуск workflow
2. Нажмите на запуск, чтобы увидеть логи
3. Workflow должен выполниться за 1-2 минуты

## Автоматический запуск

После первого ручного запуска workflow будет запускаться автоматически:
- **Каждый час** (по расписанию cron)
- **При push** изменений в workflow файл или скрипт сбора данных

## Проверка workflow файла

Убедитесь, что файл `.github/workflows/collect_market_data.yml` существует и содержит:

```yaml
name: Collect Market Data

on:
  schedule:
    - cron: '0 * * * *'
  workflow_dispatch:
  push:
    branches:
      - main
```

## Troubleshooting

### Actions не видны в меню?

1. Убедитесь, что файл `.github/workflows/collect_market_data.yml` существует
2. Проверьте синтаксис YAML файла
3. Убедитесь, что файл закоммичен в ветку `main`

### Workflow не запускается?

1. Проверьте, что секрет `TELEGRAM_BOT_TOKEN` добавлен
2. Проверьте синтаксис workflow файла
3. Посмотрите ошибки в разделе Actions

### Ошибка при выполнении?

1. Откройте запуск workflow
2. Посмотрите логи каждого шага
3. Проверьте, что все зависимости установлены
4. Убедитесь, что токен правильный

## Быстрая проверка

Выполните локально для проверки скрипта:

```bash
# Установите зависимости
pip install -r requirements.txt

# Запустите скрипт сбора данных
python scripts/collect_market_data.py
```

Если скрипт работает локально, он должен работать и в GitHub Actions.

