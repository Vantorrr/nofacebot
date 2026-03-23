# 🚀 NOFACE.digital Bot - Production Deployment

## 🎯 Варианты хостинга

### 1. 🔥 VPS Сервер (РЕКОМЕНДУЕТСЯ)

**💰 Стоимость:** $3-5/месяц  
**🌍 Провайдеры:** DigitalOcean, Hetzner, Vultr, Contabo

#### Пошаговая установка:

```bash
# 1. Подключись к серверу
ssh root@your-server-ip

# 2. Обнови систему
apt update && apt upgrade -y

# 3. Клонируй репозиторий
git clone https://github.com/твой-username/nofacebot.git
cd nofacebot

# 4. Запусти автоматический деплой
./deploy.sh
```

### 2. ⚡ Railway.app (САМЫЙ ПРОСТОЙ)

1. **Регистрация:** [Railway.app](https://railway.app)
2. **Подключи GitHub:** Connect Repository
3. **Выбери репозиторий:** nofacebot
4. **Добавь переменные:**
   ```
   BOT_TOKEN=your_telegram_bot_token
   ADMIN_IDS=123456789
   CONTACT_USERNAME=pavel_xdev
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   ```
5. **Deploy!** 🎉

### 3. 🐳 Render.com

1. **Регистрация:** [Render.com](https://render.com)
2. **Create Web Service**
3. **Connect GitHub repo**
4. **Runtime:** Docker
5. **Добавь env vars:**
   ```
   BOT_TOKEN=your_telegram_bot_token
   ADMIN_IDS=123456789
   ```

## 🛠 Управление ботом

### Полезные команды:

```bash
# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f

# Перезапуск бота
docker-compose -f docker-compose.prod.yml restart

# Остановка бота
docker-compose -f docker-compose.prod.yml down

# Обновление бота
git pull
docker-compose -f docker-compose.prod.yml up -d --build

# Проверка статуса
docker-compose -f docker-compose.prod.yml ps
```

### Автообновление:

```bash
# Создай скрипт автообновления
cat > update.sh << 'EOF'
#!/bin/bash
cd /path/to/nofacebot
git pull
docker-compose -f docker-compose.prod.yml up -d --build
EOF

chmod +x update.sh

# Добавь в crontab (обновление каждый день в 3:00)
crontab -e
# Добавь строку:
# 0 3 * * * /path/to/nofacebot/update.sh
```

## 📊 Мониторинг

### Проверка здоровья бота:

```bash
# Статус контейнера
docker ps | grep nofacebot

# Использование ресурсов
docker stats nofacebot_prod

# Логи ошибок
docker-compose -f docker-compose.prod.yml logs | grep ERROR
```

### Настройка алертов:

1. **Telegram уведомления** - бот сам уведомит если упадет
2. **Email алерты** - настрой через cron
3. **Uptimerobot** - бесплатный мониторинг

## 🔒 Безопасность

### Базовая защита сервера:

```bash
# Обнови систему
apt update && apt upgrade -y

# Настрой firewall
ufw enable
ufw allow ssh
ufw allow 80
ufw allow 443

# Отключи root login (опционально)
sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl reload sshd
```

## 🆘 Устранение проблем

### Бот не запускается:

```bash
# Проверь логи
docker-compose -f docker-compose.prod.yml logs

# Проверь переменные окружения
cat .env

# Перезапусти с пересборкой
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build
```

### Нет места на диске:

```bash
# Очисти Docker
docker system prune -a

# Очисти логи
sudo truncate -s 0 /var/lib/docker/containers/*/*-json.log
```

## 🎉 Готово!

Твой бот теперь работает 24/7! 🚀

**Проверь что всё работает:**
1. Напиши боту `/start`
2. Попробуй заказать услугу
3. Проверь админ-панель

**💡 Совет:** Добавь домен и SSL сертификат для вебхуков если планируешь масштабироваться. 