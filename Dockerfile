FROM python:3.10
WORKDIR /app
RUN pip install flask
RUN pip install --no-cache-dir --upgrade -r python-dotenv
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]