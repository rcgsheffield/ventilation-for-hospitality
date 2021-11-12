FROM python:3.8-slim

# Install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./vent /opt/vent/vent

WORKDIR /opt/vent
ENTRYPOINT ["python", "-m", "vent"]
