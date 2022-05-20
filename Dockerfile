FROM zmkfirmware/zmk-build-arm:2.4

RUN mkdir -p /app/firmware

WORKDIR /app

COPY config config
COPY bin/build.sh ./

CMD ["./build.sh"]
