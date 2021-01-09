FROM python:3

ADD . /TikTokBlaster

RUN apt update
RUN apt install ffmpeg -y
RUN pip install -r /TikTokBlaster/requirements.txt

RUN mkdir -p /output/tmp


ENTRYPOINT ["sh", "/TikTokBlaster/src/run.sh"]

# CMD python /TikTokBlaster/src/main.py --hash-tag $HASHTAG --count 1
