#!/bin/bash

# 项目初始化脚本
# 用法: ./init_project.sh <project_name>

# 检查参数
if [ -z "$1" ]; then
    echo "Usage: ./init_project.sh <project_name>"
    exit 1
fi

PROJECT_NAME=$1
BASE_DIR=$(pwd)/$PROJECT_NAME

# 创建基础项目结构
echo "Creating project structure for $PROJECT_NAME..."

# 创建主目录
mkdir -p $BASE_DIR
cd $BASE_DIR

# 创建顶层文件
echo "Creating root files..."
touch Dockerfile
touch Makefile
touch README.md
touch requirements.txt
touch setup.py
touch tox.ini
touch .gitignore
touch .env.example

# 创建配置目录
echo "Creating config directory..."
mkdir -p config
touch config/__init__.py
touch config/config.yaml
touch config/config.prod.yaml
touch config/config.test.yaml

# 创建源代码目录结构
echo "Creating source code directory structure..."
mkdir -p src/app
cd src/app

# 创建Python包初始化文件
touch __init__.py
touch main.py
touch container.py

# 创建核心模块
mkdir -p core/base
touch core/__init__.py
touch core/exceptions.py
touch core/constants.py
touch core/base/__init__.py
touch core/base/repository.py
touch core/base/service.py
touch core/base/handler.py

# 创建模型目录
mkdir -p models
touch models/__init__.py
touch models/{chat,order,report}.py

# 创建schema目录
mkdir -p schemas
touch schemas/__init__.py
touch schemas/{chat,order,report}.py

# 创建handlers目录
mkdir -p handlers
touch handlers/__init__.py
touch handlers/{chat,order,report}.py

# 创建services目录
mkdir -p services
touch services/__init__.py
touch services/{chat,order,report}.py

# 创建repositories目录
mkdir -p repositories
touch repositories/__init__.py
touch repositories/{chat,order,report}.py

# 创建infrastructure目录
mkdir -p infrastructure
touch infrastructure/__init__.py
touch infrastructure/{database,redis,storage,events}.py

# 创建API相关目录
mkdir -p api/middleware
touch api/__init__.py
touch api/routes.py
touch api/deps.py
touch api/middleware/__init__.py

# 创建websocket目录
mkdir -p websocket
touch websocket/__init__.py
touch websocket/{connection,dispatcher,handlers}.py

# 创建AI模块目录
mkdir -p ai
touch ai/__init__.py
touch ai/{speech,ocr,nlp,sql_gen}.py

# 创建utils目录
mkdir -p utils
touch utils/__init__.py
touch utils/{logger,security,validators}.py

# 返回项目根目录
cd $BASE_DIR

# 创建测试目录结构
echo "Creating test directory structure..."
mkdir -p tests/{test_handlers,test_services,test_repositories}
touch tests/__init__.py
touch tests/conftest.py
touch tests/test_handlers/__init__.py
touch tests/test_services/__init__.py
touch tests/test_repositories/__init__.py

# 创建文档目录
echo "Creating documentation directory structure..."
mkdir -p docs/{api,architecture,deployment}

# 初始化git仓库
echo "Initializing git repository..."
git init

# 创建基础.gitignore文件
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Operating System
.DS_Store
Thumbs.db

# Project specific
.env
*.log
EOF

# 创建基础 requirements.txt
cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.1
dependency-injector==4.41.0
python-dotenv==1.0.0
PyYAML==6.0.1
websockets==12.0
redis==5.0.1
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.1
python-multipart==0.0.6
EOF

# 创建基础 Makefile
cat > Makefile << EOF
.PHONY: install test lint run clean build docker-build docker-run

install:
	pip install -r requirements.txt

test:
	pytest

lint:
	flake8 src tests
	mypy src tests

run:
	uvicorn src.app.main:app --reload

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete

build:
	python setup.py build

docker-build:
	docker build -t ${PROJECT_NAME} .

docker-run:
	docker run -p 8000:8000 ${PROJECT_NAME}
EOF

# 创建基础 setup.py
cat > setup.py << EOF
from setuptools import setup, find_packages

setup(
    name="${PROJECT_NAME}",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "sqlalchemy==2.0.23",
        "pydantic==2.5.1",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of your project",
    keywords="keywords",
    python_requires=">=3.8",
)
EOF

# 创建基础 Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# 创建README.md
cat > README.md << EOF
# ${PROJECT_NAME}

## Description
Add your project description here.

## Installation
\`\`\`bash
make install
\`\`\`

## Running the application
\`\`\`bash
make run
\`\`\`

## Running tests
\`\`\`bash
make test
\`\`\`

## Building Docker image
\`\`\`bash
make docker-build
make docker-run
\`\`\`
EOF

echo "Project structure created successfully!"
echo "Next steps:"
echo "1. Create and activate a virtual environment"
echo "2. Run 'make install' to install dependencies"
echo "3. Run 'make run' to start the development server"