FROM python:3.11
WORKDIR /app
ADD requirements.txt .
ADD app app
RUN pip install -r requirements.txt
CMD ["hypercorn", "app/main:app"]
