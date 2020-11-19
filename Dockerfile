FROM python:3.8.5

COPY . /equipment_portal /equipment_portal /
COPY . /requirements.txt /

RUN pip install -r requirements.txt

EXPOSE 5010


CMD ["uvicorn", "equipment_portal.main:app", "--host", "0.0.0.0", "--port", "5010"]
