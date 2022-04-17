FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update && apk upgrade

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
WORKDIR /life-beyond-dreams
COPY ./src /life-beyond-dreams

EXPOSE 8000
CMD ["uvicorn", "api:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
