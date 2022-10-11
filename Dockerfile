FROM zmkfirmware/zmk-build-arm:2.4

WORKDIR /app

COPY config/west.yml config/west.yml

# West Init
RUN west init -l config
# West Update
RUN west update
# West Zephyr export
RUN west zephyr-export

COPY config config
COPY bin/build.sh ./

CMD ["./build.sh"]
