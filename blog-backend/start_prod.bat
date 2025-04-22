@echo off
echo 启动生产环境服务器...
set ENVIRONMENT=production
python run.py --env=production
