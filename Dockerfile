FROM hrblackgom/h-image:v1
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./ /Collectors
RUN chmod 0777 /Collectors/start.sh

RUN python3.6 -m pip install pip --upgrade && \
    pip install -r /Collectors/requirements.txt

ADD ./Utils/crontab /etc/cron.d/hello-cron
RUN chmod 0644 /etc/cron.d/hello-cron

# Cron 실행
CMD cron -f
