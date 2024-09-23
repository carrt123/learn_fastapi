# 使用 Python 官方镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到容器中的工作目录
COPY . .

# 安装依赖
RUN pip install -r requirements.txt

# 暴露应用运行的端口
EXPOSE 8000

# 启动命令
CMD ["python", "app.py"]
