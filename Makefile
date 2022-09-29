.PHONY: clean

build: firmware/left.uf2 firmware/right.uf2

clean:
	rm ./firmware/*.uf2

firmware/left% firmware/right%: config/adv360.keymap
	docker run --rm -it --name zmk -v $(PWD)/firmware:/app/firmware -v $(PWD)/config:/app/config:ro zmk

docker:
	docker build --tag zmk .
