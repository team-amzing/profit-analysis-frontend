FROM nginx
MAINTAINER cot12@aber.ac.uk


COPY start.sh /

RUN apt update
RUN apt -y install procps
RUN chmod 777 /star.sh

#expose the web server port to outside the container
EXPOSE 80/tcp

ENTRYPOINT ["bash","/start.sh"]
