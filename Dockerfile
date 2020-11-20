FROM python:3.8.5

COPY . /erudite
COPY . /requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5010

CMD ["uvicorn", "erudite.main:app", "--host", "0.0.0.0", "--port", "5010"]
