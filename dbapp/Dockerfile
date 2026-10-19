from python:3.13-slim
workdir /dbapp
copy requirement.txt .
run pip install -r requirement.txt
copy . .
expose 8001
cmd ["python", "app.py"]