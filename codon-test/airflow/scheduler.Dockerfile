FROM apache/airflow:latest
USER root
RUN apt update
CMD [ "airflow", "scheduler" ]