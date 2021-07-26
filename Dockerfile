FROM python:3.9

WORKDIR /usr/app

COPY ./ ./

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python",  "main.py"]
CMD ["mycompany", "siem_ip", "port"]
