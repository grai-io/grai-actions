FROM python:3.10-alpine

COPY src/ src/
RUN pip3 install -r src/requirements.txt

ENTRYPOINT ["python3"]
CMD ["src/main.py"]