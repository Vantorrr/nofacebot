#!/bin/bash

# NOFACE.digital Bot - Production Deployment Script
echo "🚀 Deploying NOFACE.digital Bot..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed!${NC}"
    echo -e "${YELLOW}Installing Docker...${NC}"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Installing docker-compose...${NC}"
    pip3 install docker-compose
fi

# Create directories
echo -e "${BLUE}📁 Creating directories...${NC}"
mkdir -p data logs

# Set environment variables (if not already set)
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚙️ Creating .env file...${NC}"
    cat > .env << EOF
BOT_TOKEN=7876257761:AAHcoByiCBTGXUmFaLeTcDkUTSU2r8qDALU
ADMIN_ID=8141463258
EOF
fi

# Stop existing containers
echo -e "${YELLOW}🛑 Stopping existing containers...${NC}"
docker-compose -f docker-compose.prod.yml down

# Build and start the bot
echo -e "${BLUE}🔨 Building and starting the bot...${NC}"
docker-compose -f docker-compose.prod.yml up -d --build

# Check status
echo -e "${BLUE}🔍 Checking container status...${NC}"
docker-compose -f docker-compose.prod.yml ps

# Show logs
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo -e "${BLUE}📋 Viewing logs (Ctrl+C to exit):${NC}"
docker-compose -f docker-compose.prod.yml logs -f 