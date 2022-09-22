FROM apache/spark-py:v3.3.0

ENV PYTHONPATH=/app
user root

# copy the code
ADD ./pipeline_twitter /app/pipeline_twitter
ADD ./requirements.txt /app/requirements.txt

# Install Python dependencies
RUN python3 -m pip install -r /app/requirements.txt

# Set the working directory
WORKDIR /app
