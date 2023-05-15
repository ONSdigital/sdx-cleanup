FROM eu.gcr.io/ons-sdx-ci/sdx-gcp:1.2.1
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "./run.py"]