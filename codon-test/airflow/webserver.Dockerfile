FROM apache/airflow:latest
USER root
RUN apt update
USER airflow
RUN airflow db init 
WORKDIR /tmp
RUN curl -fsSLO https://exaloop.io/install.sh && bash install.sh
WORKDIR /home/airflow
RUN touch .bash_aliases && echo "export PATH=$HOME/.codon/bin:$PATH" > .bash_aliases && source .bashrc
WORKDIR /opt/airflow
EXPOSE 8080
CMD [ "airflow", "webserver" ]