FROM python

WORKDIR /sliya/
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 9715
VOLUME /sliya/

# ENTRYPOINT [ "python"]
CMD [ "python", "-m", "sliya" ]
