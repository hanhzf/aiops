#!/usr/bin/env python3
"""
Project bootstrapping script that creates the initial project structure and files.
Run this script to initialize a new project with the basic structure and file templates.
"""

import os
import stat
from pathlib import Path
import shutil

class ProjectBootstrapper:
    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)
        
    def create_directory_structure(self):
        """Create the entire directory structure for the project."""
        directories = [
            # Main source directories
            "src/app",
            "src/app/api/middleware",
            "src/app/config",
            "src/app/handlers",
            "src/app/services",
            "src/app/repositories",
            "src/app/models",
            "src/app/schemas",
            "src/app/infrastructure",
            "src/app/utils",
            # Test directories
            "tests/integration",
            "tests/unit/handlers",
            "tests/unit/services",
            "tests/unit/repositories",
            # Docker directory
            "docker",
        ]
        
        for directory in directories:
            (self.base_dir / directory).mkdir(parents=True, exist_ok=True)
            # Add __init__.py to all Python directories
            if directory.startswith(("src", "tests")):
                (self.base_dir / directory / "__init__.py").touch()

    def create_file(self, path: Path, content: str):
        """Create a file with the given content."""
        path.write_text(content)
        if path.suffix in ['.sh', '.py']:
            # Make scripts executable
            path.chmod(path.stat().st_mode | stat.S_IEXEC)

    def create_dockerfile(self):
        content = """FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/

CMD ["python", "-m", "src.app.main"]
"""
        self.create_file(self.base_dir / "Dockerfile", content)

    def create_makefile(self):
        content = """# Makefile for project management

.PHONY: install test lint clean build run

install:
	pip install -r requirements.txt

test:
	pytest tests/

lint:
	flake8 src/ tests/
	black src/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +

build:
	docker build -t myapp .

run:
	docker run -p 8000:8000 myapp
"""
        self.create_file(self.base_dir / "Makefile", content)

    def create_main_app(self):
        content = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from .config.config import load_config
from .infrastructure.database import init_db
from .infrastructure.logger import setup_logging

app = FastAPI(title="Intelligent Order and Report System")

# Load configuration
config = load_config()

# Setup logging
setup_logging(config)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    await init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
        self.create_file(self.base_dir / "src" / "app" / "main.py", content)

    def create_routes(self):
        content = """from fastapi import APIRouter, Depends, File, UploadFile
from typing import List

from ..handlers.chat import ChatHandler
from ..handlers.file import FileHandler
from ..handlers.order import OrderHandler
from ..handlers.report import ReportHandler
from ..schemas.chat import ChatCreate, ChatResponse
from ..schemas.file import FileResponse
from ..schemas.order import OrderCreate, OrderResponse
from ..schemas.report import ReportCreate, ReportResponse

router = APIRouter()

# File routes
@router.post("/files/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    file_handler: FileHandler = Depends()
):
    return await file_handler.upload_file(file)

# Chat routes
@router.post("/chats", response_model=ChatResponse)
async def create_chat(
    chat: ChatCreate,
    chat_handler: ChatHandler = Depends()
):
    return await chat_handler.create_chat(chat)

# Order routes
@router.post("/orders", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    order_handler: OrderHandler = Depends()
):
    return await order_handler.create_order(order)

# Report routes
@router.post("/reports", response_model=ReportResponse)
async def create_report(
    report: ReportCreate,
    report_handler: ReportHandler = Depends()
):
    return await report_handler.create_report(report)
"""
        self.create_file(self.base_dir / "src" / "app" / "api" / "routes.py", content)

    def create_config(self):
        content = """import os
from pathlib import Path
import yaml
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    \"\"\"Load configuration from YAML file and environment variables.\"\"\"
    # Load base config from YAML
    config_path = Path(__file__).parent / "settings.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Override with environment variables
    config["database"] = {
        "host": os.getenv("DATABASE_HOST", config["database"]["host"]),
        "port": int(os.getenv("DATABASE_PORT", config["database"]["port"])),
        "username": os.getenv("DATABASE_USER", config["database"]["username"]),
        "password": os.getenv("DATABASE_PASS", config["database"]["password"]),
        "database": os.getenv("DATABASE_NAME", config["database"]["database"]),
    }
    
    return config
"""
        self.create_file(self.base_dir / "src" / "app" / "config" / "config.py", content)

        # Create settings.yaml
        settings_content = """database:
  host: localhost
  port: 5432
  username: postgres
  password: postgres
  database: agent

storage:
  type: aliyun_oss
  bucket: app-files
  endpoint: oss-cn-hangzhou.aliyuncs.com
  access_key_id: your_access_key
  access_key_secret: your_access_secret

logging:
  level: INFO
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  file: app.log
"""
        self.create_file(self.base_dir / "src" / "app" / "config" / "settings.yaml", settings_content)

    def create_requirements(self):
        content = """fastapi>=0.68.0
uvicorn>=0.15.0
python-multipart>=0.0.5
SQLAlchemy>=1.4.23
asyncpg>=0.24.0
pyyaml>=5.4.1
aliyun-oss2>=2.15.0
pytest>=6.2.5
pytest-asyncio>=0.16.0
pytest-cov>=2.12.1
black>=21.7b0
flake8>=3.9.2
"""
        self.create_file(self.base_dir / "requirements.txt", content)

    def create_readme(self):
        content = """# Intelligent Order and Report System

A FastAPI-based system for intelligent order processing and report generation.

## Setup

1. Install dependencies:
```bash
make install
```

2. Run tests:
```bash
make test
```

3. Build and run with Docker:
```bash
make build
make run
```

## Project Structure

```
.
├── src/                 # Source code
├── tests/              # Test files
├── docker/             # Docker configuration
├── Dockerfile          # Docker build file
├── Makefile           # Build automation
└── requirements.txt    # Python dependencies
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

- Use `make lint` to check code style
- Use `make test` to run tests
- Use `make clean` to clean up generated files
"""
        self.create_file(self.base_dir / "README.md", content)

    def run(self):
        """Run the bootstrapping process."""
        print("Creating project structure...")
        self.create_directory_structure()
        
        print("Creating core files...")
        self.create_dockerfile()
        self.create_makefile()
        self.create_main_app()
        self.create_routes()
        self.create_config()
        self.create_requirements()
        self.create_readme()
        
        print("Project initialized successfully!")

if __name__ == "__main__":
    bootstrapper = ProjectBootstrapper()
    bootstrapper.run()