.DEFAULT_GOAL := firmware

ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
ZMK_IMAGE ?= zmkfirmware/zmk-build-arm:stable
ZMK_VOLUME ?= temper-zmkstudio-build
UPDATE ?= 0

.PHONY: firmware
firmware:
	@docker info >/dev/null 2>&1 || { echo "Start Docker Desktop before running make firmware." >&2; exit 1; }
	@mkdir -p "$(ROOT)/firmware"
	docker run --rm \
		--env HOME=/workspace --env CCACHE_DIR=/workspace/.ccache --env UPDATE="$(UPDATE)" \
		--mount "type=volume,source=$(ZMK_VOLUME),target=/workspace" \
		--mount "type=bind,source=$(ROOT),target=/config,readonly" \
		--mount "type=bind,source=$(ROOT)/firmware,target=/output" \
		--workdir /workspace \
		"$(ZMK_IMAGE)" python3 /config/scripts/build-firmware.py
	@printf '\nFirmware ready in:\n  %s\n' "$(ROOT)/firmware"
