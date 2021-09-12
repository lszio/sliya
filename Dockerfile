FROM python

WORKDIR /sliya/
# COPY ./requirements.txt ./requirements.txt
COPY . /sliya
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 9715
VOLUME /sliya/

CMD [ "python", "-m", "sliya" ]
