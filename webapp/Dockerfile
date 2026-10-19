from python:3.13-slim
workdir /webapp
copy requirement.txt .
run pip install -r requirement.txt
copy . .
expose 8000
cmd ["python", "app.py"]