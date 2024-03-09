FROM ubuntu:latest
LABEL authors="howard"

ENTRYPOINT ["top", "-b"]