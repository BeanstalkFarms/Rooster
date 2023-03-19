FROM python:3.9.15-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl

# Install Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# Add Rust to the PATH environment variable
ENV PATH="/root/.cargo/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y gcc
ADD requirements.txt  ./
RUN mkdir -p /install
RUN pip3 install --prefix=/install -r requirements.txt

FROM python:3.9.15-slim
COPY --from=builder /install /usr/local
RUN mkdir -p /app
WORKDIR /app
ADD . /app

EXPOSE 5001

ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENTRYPOINT ["waitress-serve", "--host=0.0.0.0", "--port=5001", "--call", "index:create_app"]
