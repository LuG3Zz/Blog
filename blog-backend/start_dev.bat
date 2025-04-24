@echo off
echo 启动开发环境服务器...
set ENVIRONMENT=development
./venv/Scripts/activate.PS1
python run.py --env=development
