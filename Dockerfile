#syntax=docker/dockerfile:experimental
FROM python:3.11

# need this to install dependencies using our ssh key from github
RUN apt update
RUN apt install ffmpeg libsm6 libxext6 openssh-client -y
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

# install dependent packages
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN rm requirements.txt

# install jupyter here, keep out of requirements
RUN pip install jupyter>=1.0.0
