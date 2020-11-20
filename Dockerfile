FROM python:3.8.5

COPY . /erudite
COPY ./requirements.txt /

RUN pip install -r requirements.txt

EXPOSE 5010

WORKDIR /erudite/erudite

CMD ["uvicorn", "main:app", "--port", "5010"]
