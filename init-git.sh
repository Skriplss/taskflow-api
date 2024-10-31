#!/bin/bash

# TaskFlow API - Git Initialization Script
# This script initializes Git repository with proper branching strategy

set -e  # Exit on error

echo "Initializing Git repository..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}Error: Git is not installed${NC}"
    echo "Please install Git first: https://git-scm.com/downloads"
    exit 1
fi

# Check if already a Git repository
if [ -d ".git" ]; then
    echo -e "${YELLOW}Git repository already exists${NC}"
    read -p "Do you want to reinitialize? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
    rm -rf .git
fi

# Initialize Git repository
echo -e "${BLUE}Initializing Git repository...${NC}"
git init
echo -e "${GREEN}✓ Git repository initialized${NC}"

# Configure Git (optional)
echo ""
read -p "Configure Git user? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter your name: " git_name
    read -p "Enter your email: " git_email
    git config user.name "$git_name"
    git config user.email "$git_email"
    echo -e "${GREEN}✓ Git user configured${NC}"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo -e "${BLUE}Creating .gitignore...${NC}"
    cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
.env
venv/
*.db
.pytest_cache/
.coverage
htmlcov/
.idea/
.vscode/
*.swp
EOF
    echo -e "${GREEN}✓ .gitignore created${NC}"
fi

# Initial commit on main branch
echo -e "${BLUE}Creating initial commit...${NC}"
git add .
git commit -m "feat: initial commit - Task Management API

- FastAPI backend with PostgreSQL
- JWT authentication
- Task CRUD operations
- Docker support
- Comprehensive tests
- CI/CD with GitHub Actions"
echo -e "${GREEN}✓ Initial commit created on main branch${NC}"

# Create develop branch
echo -e "${BLUE}Creating develop branch...${NC}"
git branch develop
echo -e "${GREEN}✓ develop branch created${NC}"

# Switch to develop
git checkout develop
echo -e "${GREEN}✓ Switched to develop branch${NC}"

# Summary
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Git repository initialized${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Branch structure:${NC}"
echo "  • main    - Production-ready code"
echo "  • develop - Development branch (current)"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo ""
echo "1. Create remote repository on GitHub"
echo ""
echo "2. Add remote and push:"
echo "   ${YELLOW}git remote add origin <your-repo-url>${NC}"
echo "   ${YELLOW}git push -u origin main${NC}"
echo "   ${YELLOW}git push -u origin develop${NC}"
echo ""
echo "3. Create feature branch:"
echo "   ${YELLOW}git checkout -b feature/your-feature${NC}"
echo ""
echo "4. After changes:"
echo "   ${YELLOW}git add .${NC}"
echo "   ${YELLOW}git commit -m 'feat: description'${NC}"
echo "   ${YELLOW}git push origin feature/your-feature${NC}"

