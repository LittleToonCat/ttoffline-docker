FROM ubuntu:16.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    libfreetype6 \
    libgl1-mesa-glx \
    libharfbuzz0b \
    libx11-6 \
    python3 \
    python3-pip \
  && rm -rf /var/lib/apt/lists/*

# Install requests module for the updater script.
RUN python3 -m pip install requests

COPY updater.py /updater.py

# AppImages can't be mounted inside Docker containers, so we have
# to extract them and run them.
ENV APPIMAGE_EXTRACT_AND_RUN 1

EXPOSE 7198
CMD python3 /updater.py && ./offline --dedicated
