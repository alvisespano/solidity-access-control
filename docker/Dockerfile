FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    wget unzip tar curl git tmux \
    && pip3 install pandas matplotlib matplotlib_venn \
    && rm -rf /var/lib/apt/lists/*

VOLUME ["/app/artifact"]

WORKDIR /app/artifact

COPY data-finder.py .
COPY extract-sol-from-json.py .
COPY json_file_list.txt .
COPY remove-sol-duplicates.py .
COPY sol_file_list.txt .

RUN git clone https://huggingface.co/datasets/Zellic/smart-contract-fiesta /app/artifact/smart-contract-fiesta/

CMD bash
