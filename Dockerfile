FROM nvidia/cuda:10.2-base

RUN apt-get update && apt-get install -y \
    software-properties-common
RUN add-apt-repository universe
RUN apt-get install -y \
    python3.7 \
    python3-pip \
    curl

# Copy the source, in case this is run as a remote job
COPY ./source /workspace/source
COPY ./test_data /workspace/test_data

# Required python packages for data loading
RUN pip3 install --upgrade pip && \
    pip3 install -r /workspace/source/requirements.txt && \
    pip3 install -e /workspace/source/nnUNet/
