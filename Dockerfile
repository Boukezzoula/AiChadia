FROM python:3.10
WORKDIR /app
COPY requirements.txt .
#RUN pip install flask
#RUN pip install --no-cache-dir --upgrade -r python-dotenv
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]
