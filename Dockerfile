FROM python:3.11-slim
COPY . /app/
WORKDIR /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--reload", "--log-level=DEBUG", "src:create_app()"]