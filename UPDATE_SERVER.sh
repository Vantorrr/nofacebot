#!/bin/bash
# Quick update script for Timeweb server

echo "🔄 Updating from GitHub..."
git pull origin main

echo "📝 Updating .env file..."
sed -i 's/ADMIN_ID=/ADMIN_IDS=/g' .env

echo "🔄 Restarting bot..."
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build

echo "✅ Done! Both admins (8141463258, 849348909) are now active"
docker-compose -f docker-compose.prod.yml logs -f --tail=50
