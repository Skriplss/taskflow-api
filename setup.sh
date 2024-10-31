#!/bin/bash

# TaskFlow API - Setup Script
# This script sets up the development environment

set -e  # Exit on error

echo "Setting up TaskFlow API..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python 3.11+ is installed
echo -e "${BLUE}Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
REQUIRED_VERSION="3.11"

if (( $(echo "$PYTHON_VERSION < $REQUIRED_VERSION" | bc -l) )); then
    echo -e "${YELLOW}Warning: Python $REQUIRED_VERSION or higher is recommended${NC}"
    echo "You have Python $PYTHON_VERSION"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ Pip upgraded${NC}"

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r requirements.txt > /dev/null 2>&1
pip install -r requirements-dev.txt > /dev/null 2>&1
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Install pre-commit hooks
echo -e "${BLUE}Installing pre-commit hooks...${NC}"
pre-commit install > /dev/null 2>&1
echo -e "${GREEN}✓ Pre-commit hooks installed${NC}"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    cp .env.example .env
    
    # Generate secret key
    SECRET_KEY=$(openssl rand -hex 32)
    
    # Update .env with generated secret key
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your-secret-key-here-change-in-production-use-openssl-rand-hex-32/$SECRET_KEY/" .env
    else
        # Linux
        sed -i "s/your-secret-key-here-change-in-production-use-openssl-rand-hex-32/$SECRET_KEY/" .env
    fi
    
    echo -e "${GREEN}✓ .env file created with generated SECRET_KEY${NC}"
    echo -e "${YELLOW}⚠ Please review and update .env file with your settings${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Summary
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setup completed successfully${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo ""
echo "1. Update .env file with your database credentials"
echo "2. Start PostgreSQL database"
echo ""
echo "   ${YELLOW}With Docker:${NC}"
echo "   docker-compose -f docker-compose.dev.yml up"
echo ""
echo "   ${YELLOW}Or locally:${NC}"
echo "   source venv/bin/activate"
echo "   alembic upgrade head"
echo "   uvicorn app.main:app --reload"
echo ""
echo "3. Visit http://localhost:8000/docs"

