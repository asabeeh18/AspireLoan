FROM python:3.9
COPY src /app/src
COPY build.sh /tmp/


RUN chmod -R +x /tmp/build.sh
RUN /bin/bash /tmp/build.sh
WORKDIR app/src

CMD [ "python", "main.py" ]