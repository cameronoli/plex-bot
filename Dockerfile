FROM python:3.10
WORKDIR /usr/src/app/secrets/bot-tokens
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY bot.py .
COPY classes/ ./classes/
EXPOSE 80
CMD ["python", "bot.py"]