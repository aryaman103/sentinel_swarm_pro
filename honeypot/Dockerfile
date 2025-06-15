FROM alpine:latest

RUN apk add --no-cache tcpdump openssh \
    && mkdir /var/log/honeypot

VOLUME ["/var/log/honeypot"]

CMD ["sh", "-c", "tail -f /dev/null"]