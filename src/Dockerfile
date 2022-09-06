FROM apache/spark-py:v3.3.0

user root

# copy the code
COPY . /app

# Install Python dependencies
RUN python3 -m pip install --upgrade pip && \
    pip3 install poetry && \
    poetry config virtualenvs.create false && \
    cd /app && \
    poetry install --no-dev

# Set the working directory
WORKDIR /app

user spark