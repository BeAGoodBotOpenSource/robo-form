# Builds a Production or Development Docker image
FROM python:3.11
WORKDIR /app


######## This is Production Environment setting. Comment for Development Environment      ####       Runs with: docker run -p 8000:80 groovy-music-app
ADD . /app
RUN pip install --upgrade pip
RUN pip install gevent
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD gunicorn --bind 0.0.0.0:80 --timeout 120 --workers 3 --worker-class gevent server:app


#--------------------------------------------------
######## Uncomment for Development Environment (Never commit!)     ####      Runs with: docker run -p 8000:80 -v $(pwd):/app groovy-music-app
# COPY . .
# RUN pip install --no-cache-dir -r requirements.txt
# ENV FLASK_APP=server.py
# EXPOSE 80
# CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]



