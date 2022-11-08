FROM python:3.10-slim-bullseye
WORKDIR /microblog
COPY /microblog .
# COPY /app  /microblog/app/
# COPY /.flaskenv /.env /config.py /microblog.py /requirements.txt ./

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt  
# WORKDIR /tmp
# COPY --from=builder /tmp /tmp
ENTRYPOINT [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]