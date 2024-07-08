FROM python:3.12-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /library_managment_system

COPY requirements.txt req.txt

RUN pip install -r req.txt

COPY . /library_managment_system

EXPOSE 8000


RUN chmod +x /library_managment_system/entrypoint.sh

ENTRYPOINT ["/library_managment_system/entrypoint.sh"]