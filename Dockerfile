FROM python:3.7-slim
WORKDIR /app
COPY ["requirements.txt", "main.py", "/app/"]
COPY ./calculate_deposit /app/calculate_deposit
RUN pip3 install -r /app/requirements.txt --no-cache-dir
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
