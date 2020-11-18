FROM python:3.8.5

COPY . /equipment_portal /equipment_portal /
COPY . /requirements.txt /

RUN pip install -r requirements.txt

EXPOSE 8000


CMD ["uvicorn", "equipment_portal.main:app", "--port", "8000"]
